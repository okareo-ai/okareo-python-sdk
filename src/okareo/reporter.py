import os
import json
from okareo_api_client.models import (
    TestRunItem
)

class JSONReporter:
    """
    A simmple class to define a json reporter for output of results.
    This class assumes that it is being used within the context of the CLI.
    """
    def __init__(
        self, eval_runs: list[TestRunItem] = []
        ):
            self.eval_runs = eval_runs
    
    def log(self):
        """
        Logs the results of the evaluation runs into a file based on OKAREO_REPORT_DIR.
        """
        OKAREO_REPORT_DIR = os.environ["OKAREO_REPORT_DIR"]
        if len(self.eval_runs) == 0:
            raise ValueError("No evaluation runs to log.")
        
        if len(OKAREO_REPORT_DIR) > 0 and not os.path.exists(OKAREO_REPORT_DIR):
            os.makedirs(OKAREO_REPORT_DIR, exist_ok=True)
        
        try:
            for eval in self.eval_runs:
                eval_name = eval.name
                eval_dict = eval.to_dict()
                if OKAREO_REPORT_DIR is None or len(OKAREO_REPORT_DIR) == 0:
                    print(json.dumps(eval_dict, indent=2))
                    continue

                file_name = eval_name.replace(" ", "_")
                file_path = os.path.join(OKAREO_REPORT_DIR, f"{file_name}.json")
                with open(file_path, "w") as outfile: 
                    json.dump(eval_dict, outfile, indent=2)  

        except Exception as e:
            print(f"Unexpected result {e=}")
            raise

        return

