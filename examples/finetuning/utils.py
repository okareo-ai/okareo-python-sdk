# type: ignore
import json

import torch
from peft import (
    AutoPeftModelForCausalLM,
    LoraConfig,
    get_peft_model,
    prepare_model_for_kbit_training,
)
from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    BitsAndBytesConfig,
    TrainingArguments,
)
from trl import SFTTrainer

use_flash_attention = True

PROMPT_PREAMBLE = """### Instruction:
Given "Input", return a category under "Output" that is one of the following:

- pricing
- complaints
- returns

Return only one category that is most relevant to the question.
"""


def count_tokens(tokenizer, input_dict):
    input_string = json.dumps(input_dict)
    tokens = tokenizer.tokenize(input_string)
    return len(tokens)


def get_training_args(output_dir="phi-3-4k-mini", epochs=3):
    return TrainingArguments(
        output_dir=output_dir,
        num_train_epochs=epochs,
        per_device_train_batch_size=4,
        gradient_accumulation_steps=2,
        gradient_checkpointing=True,
        optim="paged_adamw_32bit",
        logging_steps=10,
        save_strategy="epoch",
        learning_rate=5e-4,
        bf16=True,
        tf32=True,
        max_grad_norm=0.3,
        warmup_ratio=0.03,
        lr_scheduler_type="constant",
        disable_tqdm=True,  # disable tqdm since with packing values are in correct
    )


# for unpatching flash attention from the following utils.py
# https://github.com/philschmid/deep-learning-pytorch-huggingface/blob/main/training/utils/llama_patch.py#L118
def unplace_flash_attn_with_attn():
    import importlib

    import transformers

    print("Reloading model + unpatching flash attention")
    importlib.reload(transformers.models.phi3.modeling_phi3)


def format_instruction_for_scenario(input_name="{input}"):
    return f"""{PROMPT_PREAMBLE}
### Input:
{input_name}

### Output:
{{result}}
"""


def format_instruction(sample):
    prompt = f"""{PROMPT_PREAMBLE}
### Input:
{sample['question']}

### Output:
"""
    if "category" in sample.keys():
        prompt += f"{sample['category']}\n"
    return prompt


def load_raw_data(data_file_paths):
    data_dict = {}
    for file_path in data_file_paths:
        data = []
        with open(file_path) as f:
            for line in f:
                data.append(json.loads(line))
            f.close()
        data_dict[file_path] = data
    return data_dict


def get_model_tokenizer_trainer(
    model_id, finetuned_model_name, dataset, epochs=3, target_modules=None
):
    # BitsAndBytesConfig int-4 config
    bnb_config = BitsAndBytesConfig(
        load_in_4bit=True,
        bnb_4bit_use_double_quant=True,
        bnb_4bit_quant_type="nf4",
        bnb_4bit_compute_dtype=torch.bfloat16,
    )

    # Load model and tokenizer
    model = AutoModelForCausalLM.from_pretrained(
        model_id,
        quantization_config=bnb_config,
        use_cache=False,
        use_flash_attention_2=use_flash_attention,
        device_map="auto",
    )
    model.config.pretraining_tp = 1

    tokenizer = AutoTokenizer.from_pretrained(model_id)
    tokenizer.pad_token = tokenizer.eos_token
    tokenizer.padding_side = "right"

    # get the number of tokens in each expected output json
    n_train_tokens = [count_tokens(tokenizer, s["sample"]) for s in dataset["train"]]

    max_seq_length = max(
        n_train_tokens
    )  # max sequence length for model and packing of the dataset

    print(f"Initializing with max_seq_length={max_seq_length}")

    model = prepare_model_for_kbit_training(model)

    # LoRA params
    alpha = 128
    r = 128

    peft_config_kwargs = {
        "lora_alpha": alpha,
        "lora_dropout": 0.1,
        "r": r,
        "bias": "all",
        "task_type": "CAUSAL_LM",
        "target_modules": target_modules if target_modules else [],
    }

    peft_config = LoraConfig(**peft_config_kwargs)

    # prepare model for training
    peft_model = get_peft_model(model, peft_config)

    args = get_training_args(output_dir=finetuned_model_name, epochs=epochs)

    trainer_kwargs = {
        "model": peft_model,
        "train_dataset": dataset["train"],
        "dataset_text_field": "sample",
        "peft_config": peft_config,
        "max_seq_length": max_seq_length,
        "tokenizer": tokenizer,
        "packing": True,
        "args": args,
    }

    trainer = SFTTrainer(**trainer_kwargs)

    return peft_model, tokenizer, trainer


def get_finetuned_model_tokenizer(finetuned_model_name):
    if use_flash_attention:
        # unpatch flash attention
        unplace_flash_attn_with_attn()

    # load base LLM model and tokenizer
    peft_model = AutoPeftModelForCausalLM.from_pretrained(
        finetuned_model_name,
        low_cpu_mem_usage=True,
        torch_dtype=torch.float16,
        bnb_4bit_compute_dtype=torch.float16,
        load_in_4bit=True,
    )
    tokenizer = AutoTokenizer.from_pretrained(finetuned_model_name)

    return peft_model, tokenizer
