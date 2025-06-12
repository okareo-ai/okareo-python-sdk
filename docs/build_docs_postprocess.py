import json
import os

BASE_DIR = "python-sdk"
DIR = f"{BASE_DIR}/okareo"

# Drop files that are not ready for documentation
DROP_FILES = [
    f"{DIR}/crewai_logger",
    f"{DIR}/litellm_logger",
    f"{DIR}/autogen_logger",
    f"{DIR}/reporter",
    f"{DIR}/callbacks",
    f"{DIR}/async_utils",
]

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
CATEGORY_PATH = f"docs/{DIR}/_category_.json"


def _rm_file(file_path: str) -> None:
    try:
        os.remove(file_path)
        print(f"Removed file: {file_path}")
    except FileNotFoundError:
        print(f"File {file_path} not found, skipping.")


def _clean_md_file(content: list[str], sidebar_position: int) -> list[str]:
    # Convert header order
    added_order = False
    new_content = []
    for line in content:
        if line.startswith("#### "):
            new_content.append("###" + line[4:])  # Convert H4 to H2
        elif line.startswith("title: okareo.okareo"):
            line = line.replace("okareo.okareo", "okareo")  # Fix title for okareo.md
        else:
            new_content.append(line)
            if line.startswith("---") and not added_order:
                new_content.append(f"sidebar_position: {sidebar_position}\n")
                added_order = True
    return new_content


def _create_category_json() -> None:
    # create a new _category_.json file to set ordering/label for the sidebar
    category_json = {
        "label": "Python SDK",
        "position": 10,
    }
    with open(CATEGORY_PATH, "w") as f:
        json.dump(category_json, f, indent=4)


def postprocess_md_files() -> None:
    # load each .md file in the DIR and convert the header order
    for i, item in enumerate(DESIRED_ORDER):
        md_file = f"docs/{item}.md"
        # if the file is in the DROP_FILES list, rm the file
        if item in DROP_FILES:
            _rm_file(md_file)
            continue
        else:
            try:
                with open(md_file) as f:
                    content = f.readlines()

                new_content = _clean_md_file(content, i + 1)

                with open(md_file, "w") as f:
                    f.writelines(new_content)
            except FileNotFoundError:
                print(f"File {md_file} not found, skipping.")

    _create_category_json()


if __name__ == "__main__":
    postprocess_md_files()
