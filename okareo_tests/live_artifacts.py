"""Records what a live test creates on the Okareo backend and deletes it afterwards.

Removal runs in dependency order: Runs first (deleting a Run also removes its datapoints), then Scenarios,
Targets and Drivers. Each removal goes through the SDK's generated API client and must answer 204; the
ones that do not come back as messages so the caller can fail with them.
"""

from functools import partial
from typing import Any, Callable, List, Tuple, Union
from uuid import UUID

from okareo.common import BASE_URL
from okareo_api_client import Client
from okareo_api_client.api.default import (
    delete_driver_model_v0_driver_driver_id_delete,
    delete_model_under_test_v0_models_under_test_mut_id_delete,
    delete_scenario_set_v0_scenario_sets_scenario_id_delete,
    delete_test_run_v0_test_runs_delete,
)
from okareo_api_client.types import Response, Unset

Id = Union[str, UUID, None, Unset]


def _uuid(value: Id) -> UUID:
    if isinstance(value, UUID):
        return value
    if isinstance(value, str):
        return UUID(value)
    raise ValueError(f"not an id: {value!r}")


class LiveArtifacts:
    def __init__(self, api_key: str) -> None:
        self.api_key = api_key
        self.client = Client(base_url=str(BASE_URL), raise_on_unexpected_status=True)
        self.runs: List[UUID] = []
        self.scenarios: List[Tuple[UUID, str]] = []
        self.targets: List[UUID] = []
        self.drivers: List[UUID] = []

    def run(self, run_id: Id) -> None:
        self.runs.append(_uuid(run_id))

    def scenario(self, scenario_id: Id, name: str) -> None:
        self.scenarios.append((_uuid(scenario_id), name))

    def target(self, mut_id: Id) -> None:
        self.targets.append(_uuid(mut_id))

    def driver(self, driver_id: Id) -> None:
        self.drivers.append(_uuid(driver_id))

    def remove_all(self) -> List[str]:
        """Delete everything recorded; return one message per removal that did not answer 204."""
        removals: List[Tuple[str, Callable[[], Response[Any]]]] = []
        if self.runs:
            removals.append(
                (
                    f"Runs {[str(r) for r in self.runs]}",
                    partial(
                        delete_test_run_v0_test_runs_delete.sync_detailed,
                        test_run_ids=self.runs,
                        client=self.client,
                        api_key=self.api_key,
                    ),
                )
            )
        for scenario_id, name in self.scenarios:
            removals.append(
                (
                    f"Scenario {scenario_id} ({name})",
                    partial(
                        delete_scenario_set_v0_scenario_sets_scenario_id_delete.sync_detailed,
                        scenario_id,
                        name=name,
                        client=self.client,
                        api_key=self.api_key,
                    ),
                )
            )
        for mut_id in self.targets:
            removals.append(
                (
                    f"Target {mut_id}",
                    partial(
                        delete_model_under_test_v0_models_under_test_mut_id_delete.sync_detailed,
                        mut_id,
                        client=self.client,
                        api_key=self.api_key,
                    ),
                )
            )
        for driver_id in self.drivers:
            removals.append(
                (
                    f"Driver {driver_id}",
                    partial(
                        delete_driver_model_v0_driver_driver_id_delete.sync_detailed,
                        driver_id,
                        client=self.client,
                        api_key=self.api_key,
                    ),
                )
            )

        failures = []
        for label, remove in removals:
            try:
                response = remove()
            except Exception as error:  # one failed removal must not stop the rest
                failures.append(f"{label}: {type(error).__name__}: {error}")
                continue
            if response.status_code != 204:
                failures.append(
                    f"{label}: answered {int(response.status_code)}: {response.content!r}"
                )
        return failures
