import json
import os
import sqlite3
from typing import Any, List, Optional

import autogen  # type: ignore

from okareo import Okareo


class AutogenLogger:
    def __init__(
        self,
        api_key: str,
        mut_name: str,
        tags: Optional[List[str]] = None,
        base_path: Optional[str] = None,
        db_name: str = "logs.db",
        table: str = "chat_completions",
    ) -> None:
        if base_path and len(base_path) > 0:
            self.okareo = Okareo(api_key, base_path=base_path)
        else:
            self.okareo = Okareo(api_key)

        self.registered_model = self.okareo.register_model(name=mut_name, tags=tags)
        self.mut_name = mut_name
        self.tags = tags
        self.db_name = db_name
        self.table = table

    def get_log(self) -> List[dict]:
        con = sqlite3.connect(self.db_name)
        query = f"SELECT * from {self.table}"
        cursor = con.execute(query)
        rows = cursor.fetchall()
        column_names = [description[0] for description in cursor.description]
        data = [dict(zip(column_names, row)) for row in rows]
        con.close()
        return data

    def __enter__(self) -> None:
        # start logging
        autogen.runtime_logging.start()
        print(
            f"[Okareo] Logging data points for autogen chat under mut_name '{self.mut_name}'."
        )

    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        # stop logging
        autogen.runtime_logging.stop()

        # get logs
        logs = self.get_log()
        for log in logs:
            self.log_success_event(log)

        # cleanup db
        if os.path.exists(self.db_name):
            os.remove(self.db_name)

        print(
            f"[Okareo] Logged {len(log)} data points from autogen chat. View data points at {self.registered_model.app_link}."
        )

    def log_success_event(self, log: Any) -> None:
        self.registered_model.add_data_point_async(
            input_obj=log["request"],
            input_datetime=log["start_time"],
            result_obj=json.dumps(
                {
                    "response": json.loads(log["response"]),
                    "source_name": log["source_name"],
                    "cost": log["cost"],
                    "invocation_id": log["invocation_id"],
                    "client_id": log["client_id"],
                    "wrapper_id": log["wrapper_id"],
                }
            ),
            result_datetime=log["end_time"],
            context_token=log["session_id"],
            tags=self.tags,
        )

    async def async_log_success_event(self, log: Any) -> None:
        self.registered_model.add_data_point_async(
            input_obj=log["request"],
            input_datetime=log["start_time"],
            result_obj=json.dumps(
                {
                    "response": json.loads(log["response"]),
                    "source_name": log["source_name"],
                    "cost": log["cost"],
                    "invocation_id": log["invocation_id"],
                    "client_id": log["client_id"],
                    "wrapper_id": log["wrapper_id"],
                }
            ),
            result_datetime=log["end_time"],
            context_token=log["session_id"],
            tags=self.tags,
        )
