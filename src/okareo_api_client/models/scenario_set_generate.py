from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.generation_tone import GenerationTone
from ..models.scenario_type import ScenarioType
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.scenario_data_poin_response import ScenarioDataPoinResponse
    from ..models.scenario_set_generate_checks_item_type_1 import ScenarioSetGenerateChecksItemType1
    from ..models.scenario_set_generate_generation_schema import ScenarioSetGenerateGenerationSchema


T = TypeVar("T", bound="ScenarioSetGenerate")


@_attrs_define
class ScenarioSetGenerate:
    """
    Attributes:
        name (str): Name of the generated scenario set
        number_examples (int): Number of examples to be generated for the scenario set
        project_id (Union[Unset, str]): ID for the project
        source_scenario_id (Union[Unset, str]): ID for the scenario set that the generated scenario set will use as a
            source. Will throw an exception if 'source_scenario_rows' is also provided.
        source_scenario_rows (Union[Unset, List['ScenarioDataPoinResponse']]): Rows for the scenario set that the
            generated scenario set will use as a source. Will throw an exception if 'source_scenario_id' is also provided.
        synonym_sets (Union[Unset, List[List[str]]]): 2D list used by the generator to determine synonyms. Used with the
            SYNONYMS generation type.
        save_generated_scenario (Union[Unset, bool]): Whether to save the generated scenarios. Defaults to True.
            Default: True.
        generation_type (Union[Unset, ScenarioType]): An enumeration. Default: ScenarioType.REPHRASE_INVARIANT.
        generation_tone (Union[Unset, GenerationTone]): An enumeration. Default: GenerationTone.NEUTRAL.
        generation_prompt (Union[Unset, str]): Prompt for the generator to use when generating scenarios. Only supported
            by CustomGenerator type.
        generation_schema (Union[Unset, ScenarioSetGenerateGenerationSchema]): Structured output schema for the
            generator to use when generating scenarios. Only supported by CustomGenerator type.
        pre_template (Union[Unset, str]): Template for pre-processing scenario before sending it to generator
        post_template (Union[Unset, str]): Template for post-processing scenario after generator before it's saved
        lock_result (Union[Unset, bool]): Whether to lock the result of the generated scenario. Used in the Custom
            Generator type.
        checks (Union[Unset, List[Union['ScenarioSetGenerateChecksItemType1', str]]]): List of check names or check
            configs to run on the generated scenarios
    """

    name: str
    number_examples: int
    project_id: Union[Unset, str] = UNSET
    source_scenario_id: Union[Unset, str] = UNSET
    source_scenario_rows: Union[Unset, List["ScenarioDataPoinResponse"]] = UNSET
    synonym_sets: Union[Unset, List[List[str]]] = UNSET
    save_generated_scenario: Union[Unset, bool] = True
    generation_type: Union[Unset, ScenarioType] = ScenarioType.REPHRASE_INVARIANT
    generation_tone: Union[Unset, GenerationTone] = GenerationTone.NEUTRAL
    generation_prompt: Union[Unset, str] = UNSET
    generation_schema: Union[Unset, "ScenarioSetGenerateGenerationSchema"] = UNSET
    pre_template: Union[Unset, str] = UNSET
    post_template: Union[Unset, str] = UNSET
    lock_result: Union[Unset, bool] = False
    checks: Union[Unset, List[Union["ScenarioSetGenerateChecksItemType1", str]]] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        from ..models.scenario_set_generate_checks_item_type_1 import ScenarioSetGenerateChecksItemType1

        name = self.name
        number_examples = self.number_examples
        project_id = self.project_id
        source_scenario_id = self.source_scenario_id
        source_scenario_rows: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.source_scenario_rows, Unset):
            source_scenario_rows = []
            for source_scenario_rows_item_data in self.source_scenario_rows:
                source_scenario_rows_item = source_scenario_rows_item_data.to_dict()

                source_scenario_rows.append(source_scenario_rows_item)

        synonym_sets: Union[Unset, List[List[str]]] = UNSET
        if not isinstance(self.synonym_sets, Unset):
            synonym_sets = []
            for synonym_sets_item_data in self.synonym_sets:
                synonym_sets_item = synonym_sets_item_data

                synonym_sets.append(synonym_sets_item)

        save_generated_scenario = self.save_generated_scenario
        generation_type: Union[Unset, str] = UNSET
        if not isinstance(self.generation_type, Unset):
            generation_type = self.generation_type.value

        generation_tone: Union[Unset, str] = UNSET
        if not isinstance(self.generation_tone, Unset):
            generation_tone = self.generation_tone.value

        generation_prompt = self.generation_prompt
        generation_schema: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.generation_schema, Unset):
            generation_schema = self.generation_schema.to_dict()

        pre_template = self.pre_template
        post_template = self.post_template
        lock_result = self.lock_result
        checks: Union[Unset, List[Union[Dict[str, Any], str]]] = UNSET
        if not isinstance(self.checks, Unset):
            checks = []
            for checks_item_data in self.checks:
                checks_item: Union[Dict[str, Any], str]

                if isinstance(checks_item_data, ScenarioSetGenerateChecksItemType1):
                    checks_item = checks_item_data.to_dict()

                else:
                    checks_item = checks_item_data

                checks.append(checks_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
                "number_examples": number_examples,
            }
        )
        if project_id is not UNSET:
            field_dict["project_id"] = project_id
        if source_scenario_id is not UNSET:
            field_dict["source_scenario_id"] = source_scenario_id
        if source_scenario_rows is not UNSET:
            field_dict["source_scenario_rows"] = source_scenario_rows
        if synonym_sets is not UNSET:
            field_dict["synonym_sets"] = synonym_sets
        if save_generated_scenario is not UNSET:
            field_dict["save_generated_scenario"] = save_generated_scenario
        if generation_type is not UNSET:
            field_dict["generation_type"] = generation_type
        if generation_tone is not UNSET:
            field_dict["generation_tone"] = generation_tone
        if generation_prompt is not UNSET:
            field_dict["generation_prompt"] = generation_prompt
        if generation_schema is not UNSET:
            field_dict["generation_schema"] = generation_schema
        if pre_template is not UNSET:
            field_dict["pre_template"] = pre_template
        if post_template is not UNSET:
            field_dict["post_template"] = post_template
        if lock_result is not UNSET:
            field_dict["lock_result"] = lock_result
        if checks is not UNSET:
            field_dict["checks"] = checks

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.scenario_data_poin_response import ScenarioDataPoinResponse
        from ..models.scenario_set_generate_checks_item_type_1 import ScenarioSetGenerateChecksItemType1
        from ..models.scenario_set_generate_generation_schema import ScenarioSetGenerateGenerationSchema

        d = src_dict.copy()
        name = d.pop("name")

        number_examples = d.pop("number_examples")

        project_id = d.pop("project_id", UNSET)

        source_scenario_id = d.pop("source_scenario_id", UNSET)

        source_scenario_rows = []
        _source_scenario_rows = d.pop("source_scenario_rows", UNSET)
        for source_scenario_rows_item_data in _source_scenario_rows or []:
            source_scenario_rows_item = ScenarioDataPoinResponse.from_dict(source_scenario_rows_item_data)

            source_scenario_rows.append(source_scenario_rows_item)

        synonym_sets = []
        _synonym_sets = d.pop("synonym_sets", UNSET)
        for synonym_sets_item_data in _synonym_sets or []:
            synonym_sets_item = cast(List[str], synonym_sets_item_data)

            synonym_sets.append(synonym_sets_item)

        save_generated_scenario = d.pop("save_generated_scenario", UNSET)

        _generation_type = d.pop("generation_type", UNSET)
        generation_type: Union[Unset, ScenarioType]
        if isinstance(_generation_type, Unset):
            generation_type = UNSET
        else:
            generation_type = ScenarioType(_generation_type)

        _generation_tone = d.pop("generation_tone", UNSET)
        generation_tone: Union[Unset, GenerationTone]
        if isinstance(_generation_tone, Unset):
            generation_tone = UNSET
        else:
            generation_tone = GenerationTone(_generation_tone)

        generation_prompt = d.pop("generation_prompt", UNSET)

        _generation_schema = d.pop("generation_schema", UNSET)
        generation_schema: Union[Unset, ScenarioSetGenerateGenerationSchema]
        if isinstance(_generation_schema, Unset):
            generation_schema = UNSET
        else:
            generation_schema = ScenarioSetGenerateGenerationSchema.from_dict(_generation_schema)

        pre_template = d.pop("pre_template", UNSET)

        post_template = d.pop("post_template", UNSET)

        lock_result = d.pop("lock_result", UNSET)

        checks = []
        _checks = d.pop("checks", UNSET)
        for checks_item_data in _checks or []:

            def _parse_checks_item(data: object) -> Union["ScenarioSetGenerateChecksItemType1", str]:
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    checks_item_type_1 = ScenarioSetGenerateChecksItemType1.from_dict(data)

                    return checks_item_type_1
                except:  # noqa: E722
                    pass
                return cast(Union["ScenarioSetGenerateChecksItemType1", str], data)

            checks_item = _parse_checks_item(checks_item_data)

            checks.append(checks_item)

        scenario_set_generate = cls(
            name=name,
            number_examples=number_examples,
            project_id=project_id,
            source_scenario_id=source_scenario_id,
            source_scenario_rows=source_scenario_rows,
            synonym_sets=synonym_sets,
            save_generated_scenario=save_generated_scenario,
            generation_type=generation_type,
            generation_tone=generation_tone,
            generation_prompt=generation_prompt,
            generation_schema=generation_schema,
            pre_template=pre_template,
            post_template=post_template,
            lock_result=lock_result,
            checks=checks,
        )

        scenario_set_generate.additional_properties = d
        return scenario_set_generate

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
