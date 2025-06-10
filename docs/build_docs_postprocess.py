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


def reorder_sidebar() -> None:
    with open(SIDEBAR_PATH, "r") as f:
        sidebar = json.load(f)

    # Find the category containing the items
    for category in sidebar.get("items", []):
        if category.get("label") == "okareo" and "items" in category:
            # Reorder items according to DESIRED_ORDER
            items_set = set(category["items"])
            reordered = [item for item in DESIRED_ORDER if item in items_set]
            # Optionally, append any items not in DESIRED_ORDER
            reordered += [item for item in category["items"] if item not in reordered]
            category["items"] = reordered
            break

    with open(SIDEBAR_PATH, "w") as f:
        json.dump(sidebar, f, indent=2)

def convert_header_order() -> None:
    # load each .md file in the DIR and convert the header order
    for item in DESIRED_ORDER:
        md_file = f"docs/{item}.md"
        try:
            with open(md_file, "r") as f:
                content = f.readlines()

            # Convert header order
            new_content = []
            for line in content:
                if line.startswith("#### "):
                    new_content.append("###" + line[4:])  # Convert H4 to H2
                else:
                    new_content.append(line)

            with open(md_file, "w") as f:
                f.writelines(new_content)
        except FileNotFoundError:
            print(f"File {md_file} not found, skipping.")

if __name__ == "__main__":
    reorder_sidebar()
    convert_header_order()
