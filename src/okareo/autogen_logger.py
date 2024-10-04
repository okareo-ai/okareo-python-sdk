
import json
import sqlite3
import autogen
from typing import Any, List, Optional

from okareo import Okareo

class AutogenLogger():  # type: ignore
    def __init__(
        self,
        api_key: str,
        mut_name: str,
        context_token: str,
        tags: Optional[List[str]] = None,
        base_path: Optional[str] = None,
        db_name: Optional[str] = "logs.db",
        table: Optional[str] = "chat_completions"
    ) -> None:
        if base_path and len(base_path) > 0:
            self.okareo = Okareo(api_key, base_path=base_path)
        else:
            self.okareo = Okareo(api_key)

        self.context_token = context_token
        self.registered_model = self.okareo.register_model(name=mut_name, tags=tags)
        self.tags = tags
        self.db_name = db_name
        self.table = table

    def get_log(self):
        con = sqlite3.connect(self.db_name)
        query = f"SELECT * from {self.table}"
        cursor = con.execute(query)
        rows = cursor.fetchall()
        column_names = [description[0] for description in cursor.description]
        data = [dict(zip(column_names, row)) for row in rows]
        con.close()
        return data

    def __enter__(self):
        autogen.runtime_logging.start()

    def __exit__(self, exc_type, exc_val, exc_tb):
        autogen.runtime_logging.stop()
        log = self.get_log()
        for i, l in enumerate(log):
            data_point = self.registered_model.add_data_point_async(
                input_obj = l["request"],
                input_datetime = l['start_time'],
                result_obj = json.dumps({
                    "response": json.loads(l["response"]),
                    "source_name": l["source_name"],
                    "cost": l["cost"],
                    "invocation_id": l["invocation_id"],
                    "client_id": l["client_id"],
                    "wrapper_id": l["wrapper_id"],
                    # "is_cached": l["is_cached"],
                }),
                result_datetime = l['end_time'],
                context_token = l["session_id"],
                tags = ["autogen-groupchat"]
            )
        print(f"Logged {len(log)} data points. View them at {self.registered_model.app_link}.")

    def log_success_event(
            self, log: Any
    ) -> None:
        self.registered_model.add_data_point_async(
            input_obj = log["request"],
            input_datetime = log['start_time'],
            result_obj = json.dumps({
                "response": json.loads(log["response"]),
                "source_name": log["source_name"],
                "cost": log["cost"],
                "invocation_id": log["invocation_id"],
                "client_id": log["client_id"],
                "wrapper_id": log["wrapper_id"],
                # "is_cached": log["is_cached"],
            }),
            result_datetime = log['end_time'],
            context_token = log["session_id"],
            tags = self.tags
        )

    async def async_log_success_event(
        self, log: Any
    ) -> None:
        self.registered_model.add_data_point_async(
            input_obj = log["request"],
            input_datetime = log['start_time'],
            result_obj = json.dumps({
                "response": json.loads(log["response"]),
                "source_name": log["source_name"],
                "cost": log["cost"],
                "invocation_id": log["invocation_id"],
                "client_id": log["client_id"],
                "wrapper_id": log["wrapper_id"],
                # "is_cached": log["is_cached"],
            }),
            result_datetime = log['end_time'],
            context_token = log["session_id"],
            tags = self.tags 
        )
