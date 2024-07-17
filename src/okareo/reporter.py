import json
import os

from okareo_api_client.models import TestRunItem


class JSONReporter:
    """
    A simple class to define a json reporter for output of results.
    This class assumes that it is being used within the context of the CLI.
    """

    def __init__(self, eval_runs: list[TestRunItem]):
        self.eval_runs = eval_runs

    def log(self) -> None:
        """
        Logs the results of the evaluation runs into a file based on OKAREO_REPORT_DIR.
        """
        if len(self.eval_runs) == 0:
            raise ValueError("No evaluation runs to log.")

        okareo_report_dir = os.getenv("OKAREO_REPORT_DIR")
        if (
            okareo_report_dir is not None
            and len(okareo_report_dir) > 0
            and not os.path.exists(okareo_report_dir)
        ):
            os.makedirs(okareo_report_dir, exist_ok=True)

        try:
            for eval_item in self.eval_runs:
                eval_dict = eval_item.to_dict()
                if okareo_report_dir is None or len(okareo_report_dir) == 0:
                    print(json.dumps(eval_dict, indent=2))
                    continue

                eval_file_name: str = eval_item.id
                if eval_item.name not in (None, ""):
                    eval_file_name = str(eval_item.name)
                file_name = eval_file_name.replace(" ", "_")
                file_path = os.path.join(okareo_report_dir, f"{file_name}.json")
                with open(file_path, "w") as outfile:
                    json.dump(eval_dict, outfile, indent=2)

        except Exception as e:
            print(f"Unexpected result {e=}")
            raise

        return
