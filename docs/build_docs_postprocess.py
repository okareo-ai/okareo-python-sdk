import json

BASE_DIR = "python-sdk"
DIR = f"{BASE_DIR}/okareo"

# Desired order for sidebar items
DESIRED_ORDER = [
    f"{DIR}/okareo",
    f"{DIR}/model_under_test",
    f"{DIR}/checks",
    f"{DIR}/autogen_logger",
    f"{DIR}/crewai_logger",
    f"{DIR}/litellm_logger",
    f"{DIR}/reporter",
    f"{DIR}/callbacks",
    f"{DIR}/async_utils",
]
SIDEBAR_PATH = f"docs/{BASE_DIR}/sidebar.json"
CATEGORY_PATH = f"docs/{BASE_DIR}/_category_.json"


def postprocess_md_files() -> None:
    # load each .md file in the DIR and convert the header order
    for i, item in enumerate(DESIRED_ORDER):
        md_file = f"docs/{item}.md"
        try:
            with open(md_file) as f:
                content = f.readlines()

            # Convert header order
            added_order = False
            new_content = []
            for line in content:
                if line.startswith("#### "):
                    new_content.append("###" + line[4:])  # Convert H4 to H2
                else:
                    new_content.append(line)
                    if line.startswith("---") and not added_order:
                        new_content.append(f"sidebar_position: {i+1}\n")
                        added_order = True

            with open(md_file, "w") as f:
                f.writelines(new_content)
        except FileNotFoundError:
            print(f"File {md_file} not found, skipping.")

    # create a new _category_.json file to set ordering/label for the sidebar
    category_json = {
        "label": "Python SDK",
        "position": 10,
    }
    with open(CATEGORY_PATH, "w") as f:
        json.dump(category_json, f, indent=4)


if __name__ == "__main__":
    postprocess_md_files()
