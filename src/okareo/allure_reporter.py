"""
Allure Report generator for Okareo evaluation results.

This module provides functionality to convert Okareo evaluation results
into Allure Report compatible JSON format for visualization and dashboarding.

Usage:
    from okareo import Okareo
    from okareo.allure_reporter import AllureReporter
    from okareo_api_client.models import FindTestDataPointPayload

    # Run your evaluation
    okareo = Okareo(api_key="...")
    model = okareo.register_model(name="my-model", ...)
    test_run = model.run_test(scenario=scenario, name="My Test")

    # Fetch detailed data points
    data_points = okareo.find_test_data_points(
        FindTestDataPointPayload(test_run_id=test_run.id, full=True)
    )

    # Generate Allure report
    reporter = AllureReporter(test_run=test_run, data_points=data_points)
    reporter.generate()

    # Then run (Allure 3): allure generate -o allure-report --open allure-results
"""

import hashlib
import json
import os
import uuid
from datetime import datetime
from typing import Any, Dict, List, Optional, Union

from okareo_api_client.models import TestRunItem
from okareo_api_client.models.full_data_point_item import FullDataPointItem
from okareo_api_client.models.test_data_point_item import TestDataPointItem
from okareo_api_client.types import UNSET, Unset


class AllureStatus:
    """Allure test status constants."""

    PASSED = "passed"
    FAILED = "failed"
    BROKEN = "broken"
    SKIPPED = "skipped"
    UNKNOWN = "unknown"


class AllureReporter:
    """
    Generates Allure Report compatible JSON files from Okareo evaluation results.

    Allure Report is an open-source test reporting framework that provides
    interactive HTML reports. This reporter converts Okareo's TestRunItem
    and data points into Allure's expected JSON format.

    Attributes:
        test_run: The Okareo TestRunItem containing evaluation metadata.
        data_points: List of data points (FullDataPointItem or TestDataPointItem).
        pass_threshold: Numeric threshold for check pass/fail determination (default: 0.5).
        output_dir: Directory to write Allure result files (default: ./allure-results).
        include_attachments: Whether to create attachment files for inputs/outputs.

    Example:
        ```python
        reporter = AllureReporter(
            test_run=test_run,
            data_points=data_points,
            pass_threshold=0.7,
            output_dir="./my-allure-results"
        )
        reporter.generate()
        ```
    """

    def __init__(
        self,
        test_run: TestRunItem,
        data_points: List[Union[FullDataPointItem, TestDataPointItem]],
        pass_threshold: float = 0.5,
        output_dir: Optional[str] = None,
        include_attachments: bool = True,
    ):
        """
        Initialize the AllureReporter.

        Args:
            test_run: The Okareo TestRunItem from an evaluation.
            data_points: List of data points from the evaluation.
            pass_threshold: Threshold for numeric checks (0.0-1.0). Values >= threshold pass.
            output_dir: Directory for Allure result files. Defaults to ALLURE_RESULTS_DIR
                       environment variable or "./allure-results".
            include_attachments: Whether to write attachment files for scenario data.
        """
        self.test_run = test_run
        self.data_points = data_points
        self.pass_threshold = pass_threshold
        self.output_dir = output_dir or os.getenv(
            "ALLURE_RESULTS_DIR", "./allure-results"
        )
        self.include_attachments = include_attachments
        self._container_uuid = str(uuid.uuid4())

    def generate(self) -> str:
        """
        Generate Allure result files from the Okareo evaluation.

        Creates:
        - A container file for the test run (suite-level metadata)
        - A result file for each data point (individual test cases)
        - Attachment files for scenario inputs/outputs (if enabled)
        - Environment properties file with evaluation metadata

        Returns:
            str: Path to the output directory containing Allure results.

        Raises:
            OSError: If unable to create output directory or write files.
        """
        os.makedirs(self.output_dir, exist_ok=True)

        # Generate container (test suite) file
        container = self._create_container()
        self._write_json(f"{self._container_uuid}-container.json", container)

        # Generate test result files for each data point
        test_uuids = []
        for dp in self.data_points:
            result = self._create_test_result(dp)
            test_uuids.append(result["uuid"])
            self._write_json(f"{result['uuid']}-result.json", result)

            # Create attachments for detailed data
            if self.include_attachments:
                self._write_attachments(result["uuid"], dp)

        # Update container with children UUIDs
        container["children"] = test_uuids
        self._write_json(f"{self._container_uuid}-container.json", container)

        # Write environment properties
        self._write_environment()

        # Write categories (for failure classification)
        self._write_categories()

        return self.output_dir

    def _create_container(self) -> Dict[str, Any]:
        """
        Create Allure container (test suite) from TestRunItem.

        The container represents the overall test run/suite and groups
        individual test results together.
        """
        name = self._get_value(self.test_run.name) or "Okareo Evaluation"
        start_time = self._get_value(self.test_run.start_time)
        end_time = self._get_value(self.test_run.end_time)

        return {
            "uuid": self._container_uuid,
            "name": name,
            "children": [],  # Will be populated with test UUIDs
            "befores": [],
            "afters": [],
            "start": self._to_millis(start_time) if start_time else None,
            "stop": self._to_millis(end_time) if end_time else None,
        }

    def _create_test_result(
        self, dp: Union[FullDataPointItem, TestDataPointItem]
    ) -> Dict[str, Any]:
        """
        Create Allure test result from a data point.

        Each data point becomes an individual test case in Allure.
        """
        test_uuid = str(uuid.uuid4())
        scenario_id = self._get_value(getattr(dp, "scenario_data_point_id", None)) or ""
        test_run_name = self._get_value(self.test_run.name) or "Evaluation"

        # Generate a unique history ID for each test (includes test run ID)
        history_id = self._generate_history_id(scenario_id, self.test_run.id)

        # Determine test status from checks
        status = self._determine_status(dp)
        status_details = self._get_status_details(dp)

        # Create test steps from checks
        steps = self._create_steps(dp)

        # Get timing information
        time_created = self._get_value(getattr(dp, "time_created", None))
        end_time = self._get_value(getattr(dp, "end_time", None))

        # Build test name - include run name for clarity in multi-run reports
        test_name = self._build_test_name(dp, scenario_id)
        # Include timestamp in full name to distinguish runs with same name
        start_time = self._get_value(self.test_run.start_time)
        time_suffix = ""
        if start_time:
            if hasattr(start_time, 'strftime'):
                time_suffix = f" ({start_time.strftime('%Y-%m-%d %H:%M')})"
            elif isinstance(start_time, str):
                time_suffix = f" ({start_time[:16]})"

        result = {
            "uuid": test_uuid,
            "historyId": history_id,
            "name": test_name,
            "fullName": f"{test_run_name}{time_suffix} :: {test_name}",
            "status": status,
            "stage": "finished",
            "steps": steps,
            "labels": self._create_labels(dp),
            "parameters": self._create_parameters(dp),
            "attachments": [],  # Will be populated if attachments enabled
            "start": self._to_millis(time_created) if time_created else None,
            "stop": self._to_millis(end_time) if end_time else None,
        }

        if status_details:
            result["statusDetails"] = status_details

        return result

    def _determine_status(
        self, dp: Union[FullDataPointItem, TestDataPointItem]
    ) -> str:
        """
        Map Okareo check results to Allure status.

        Status mapping:
        - broken: Has error_message (execution error)
        - failed: Any check below threshold
        - passed: All checks pass or no checks defined
        - skipped: Not used (Okareo doesn't have this concept)
        """
        # Check for execution errors
        error_message = self._get_value(getattr(dp, "error_message", None))
        if error_message:
            return AllureStatus.BROKEN

        # Get checks from data point
        checks = self._to_dict(getattr(dp, "checks", None))
        if not checks:
            return AllureStatus.PASSED

        # Evaluate each check against threshold
        for check_name, check_value in checks.items():
            if not self._check_passes(check_value):
                return AllureStatus.FAILED

        return AllureStatus.PASSED

    def _check_passes(self, check_value: Any) -> bool:
        """Determine if a check value passes the threshold."""
        if isinstance(check_value, bool):
            return check_value
        elif isinstance(check_value, (int, float)):
            return check_value >= self.pass_threshold
        elif isinstance(check_value, dict):
            # Handle nested check results (e.g., {"score": 0.8, "passed": true})
            if "passed" in check_value:
                return bool(check_value["passed"])
            if "score" in check_value:
                return check_value["score"] >= self.pass_threshold
            if "value" in check_value:
                return self._check_passes(check_value["value"])
        # Default to passed for unknown formats
        return True

    def _get_status_details(
        self, dp: Union[FullDataPointItem, TestDataPointItem]
    ) -> Optional[Dict[str, str]]:
        """Get status details (error message/trace) for failed tests."""
        error_message = self._get_value(getattr(dp, "error_message", None))
        error_type = self._get_value(getattr(dp, "error_type", None))

        if error_message:
            details: Dict[str, str] = {"message": str(error_message)}
            if error_type:
                details["trace"] = f"Error Type: {error_type}"
            return details

        # Check for failed checks and provide details
        checks = self._to_dict(getattr(dp, "checks", None))
        failed_checks = []
        for check_name, check_value in checks.items():
            if not self._check_passes(check_value):
                failed_checks.append(f"{check_name}: {check_value}")

        if failed_checks:
            return {
                "message": f"Failed checks: {', '.join(failed_checks)}",
            }

        return None

    def _create_steps(
        self, dp: Union[FullDataPointItem, TestDataPointItem]
    ) -> List[Dict[str, Any]]:
        """
        Convert Okareo checks to Allure test steps.

        Each check becomes a step showing pass/fail status and score.
        """
        steps = []
        checks = self._to_dict(getattr(dp, "checks", None))
        checks_metadata = self._to_dict(getattr(dp, "checks_metadata", None))

        for check_name, check_value in checks.items():
            is_passed = self._check_passes(check_value)

            # Format the check value for display
            if isinstance(check_value, dict):
                display_value = json.dumps(check_value, indent=2)
            else:
                display_value = str(check_value)

            # Get metadata for this check if available
            check_meta = checks_metadata.get(check_name, {})
            if isinstance(check_meta, dict):
                check_meta = check_meta
            else:
                check_meta = {}

            step = {
                "name": f"Check: {check_name}",
                "status": AllureStatus.PASSED if is_passed else AllureStatus.FAILED,
                "stage": "finished",
                "steps": [],
                "attachments": [],
                "parameters": [{"name": "score", "value": display_value}],
            }

            # Add status details for failed checks
            if not is_passed:
                step["statusDetails"] = {
                    "message": f"Check '{check_name}' failed with value: {display_value} (threshold: {self.pass_threshold})"
                }

            steps.append(step)

        return steps

    def _create_labels(
        self, dp: Union[FullDataPointItem, TestDataPointItem]
    ) -> List[Dict[str, str]]:
        """
        Create Allure labels from test run metadata and tags.

        Labels are used for filtering and organizing tests in Allure.
        """
        labels = []

        # Suite labels for hierarchical organization
        test_run_name = self._get_value(self.test_run.name) or "Unnamed Run"
        test_run_id = self.test_run.id
        start_time = self._get_value(self.test_run.start_time)
        
        # Parent suite = "Okareo Evaluations"
        labels.append({"name": "parentSuite", "value": "Okareo Evaluations"})
        
        # Suite = test run name
        labels.append({"name": "suite", "value": test_run_name})
        
        # Sub-suite = run ID + timestamp for unique identification
        sub_suite = test_run_id[:8]
        if start_time:
            if hasattr(start_time, 'strftime'):
                sub_suite = start_time.strftime('%Y-%m-%d %H:%M')
            elif isinstance(start_time, str):
                sub_suite = start_time[:16]
        labels.append({"name": "subSuite", "value": sub_suite})

        # Project label
        project_id = self._get_value(self.test_run.project_id)
        if project_id:
            labels.append({"name": "epic", "value": f"Project: {project_id}"})

        # Test type label
        test_type = self._get_value(self.test_run.type)
        if test_type:
            labels.append({"name": "feature", "value": test_type})

        # Metric type as story
        metric_type = self._get_value(getattr(dp, "metric_type", None))
        if metric_type:
            labels.append({"name": "story", "value": metric_type})

        # Add test run tags
        test_run_tags = self._get_value(self.test_run.tags) or []
        for tag in test_run_tags:
            labels.append({"name": "tag", "value": tag})

        # Add data point tags
        dp_tags = self._get_value(getattr(dp, "tags", None)) or []
        for tag in dp_tags:
            labels.append({"name": "tag", "value": tag})

        # Framework label
        labels.append({"name": "framework", "value": "Okareo"})

        # Severity based on status (for Allure UI)
        status = self._determine_status(dp)
        if status == AllureStatus.BROKEN:
            labels.append({"name": "severity", "value": "blocker"})
        elif status == AllureStatus.FAILED:
            labels.append({"name": "severity", "value": "critical"})

        return labels

    def _create_parameters(
        self, dp: Union[FullDataPointItem, TestDataPointItem]
    ) -> List[Dict[str, str]]:
        """
        Create Allure parameters from scenario input/result.

        Parameters show key test data in the Allure UI.
        """
        params = []

        # Scenario input
        scenario_input = self._get_value(getattr(dp, "scenario_input", None))
        if scenario_input:
            params.append(
                {
                    "name": "scenario_input",
                    "value": self._truncate(self._stringify(scenario_input), 500),
                }
            )

        # Expected result
        scenario_result = self._get_value(getattr(dp, "scenario_result", None))
        if scenario_result:
            params.append(
                {
                    "name": "expected_result",
                    "value": self._truncate(self._stringify(scenario_result), 500),
                }
            )

        # Model input (if different from scenario input)
        model_input = self._get_value(getattr(dp, "model_input", None))
        if model_input and model_input != scenario_input:
            params.append(
                {
                    "name": "model_input",
                    "value": self._truncate(self._stringify(model_input), 500),
                }
            )

        # Model result/output
        model_result = self._get_value(getattr(dp, "model_result", None))
        if model_result:
            params.append(
                {
                    "name": "model_output",
                    "value": self._truncate(self._stringify(model_result), 500),
                }
            )

        return params

    def _write_attachments(
        self, test_uuid: str, dp: Union[FullDataPointItem, TestDataPointItem]
    ) -> List[Dict[str, str]]:
        """
        Write attachment files for detailed scenario data.

        Large inputs/outputs are stored as attachments rather than inline parameters.
        """
        attachments = []

        # Scenario input attachment
        scenario_input = self._get_value(getattr(dp, "scenario_input", None))
        if scenario_input:
            attachment = self._write_attachment(
                test_uuid, "scenario_input", scenario_input
            )
            if attachment:
                attachments.append(attachment)

        # Scenario result attachment
        scenario_result = self._get_value(getattr(dp, "scenario_result", None))
        if scenario_result:
            attachment = self._write_attachment(
                test_uuid, "expected_result", scenario_result
            )
            if attachment:
                attachments.append(attachment)

        # Model result attachment
        model_result = self._get_value(getattr(dp, "model_result", None))
        if model_result:
            attachment = self._write_attachment(
                test_uuid, "model_output", model_result
            )
            if attachment:
                attachments.append(attachment)

        # Full checks data
        checks = self._get_value(getattr(dp, "checks", None))
        if checks:
            attachment = self._write_attachment(test_uuid, "checks", checks)
            if attachment:
                attachments.append(attachment)

        # Model metrics (aggregate)
        model_metrics = self._get_value(self.test_run.model_metrics)
        if model_metrics and hasattr(model_metrics, "to_dict"):
            metrics_dict = model_metrics.to_dict()
            if metrics_dict:
                attachment = self._write_attachment(
                    test_uuid, "model_metrics", metrics_dict
                )
                if attachment:
                    attachments.append(attachment)

        return attachments

    def _write_attachment(
        self, test_uuid: str, name: str, content: Any
    ) -> Optional[Dict[str, str]]:
        """Write a single attachment file."""
        try:
            source = f"{test_uuid}-{name}-attachment.json"
            file_path = os.path.join(self.output_dir, source)

            content_str = self._stringify(content)
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(content_str)

            return {
                "name": name,
                "source": source,
                "type": "application/json",
            }
        except Exception:
            return None

    def _write_environment(self) -> None:
        """Write environment.properties file with evaluation metadata."""
        env_props = []

        # Test run info
        test_run_name = self._get_value(self.test_run.name)
        if test_run_name:
            env_props.append(f"Test_Run_Name={test_run_name}")

        project_id = self._get_value(self.test_run.project_id)
        if project_id:
            env_props.append(f"Project_ID={project_id}")

        test_type = self._get_value(self.test_run.type)
        if test_type:
            env_props.append(f"Test_Type={test_type}")

        mut_id = self._get_value(self.test_run.mut_id)
        if mut_id:
            env_props.append(f"Model_Under_Test_ID={mut_id}")

        scenario_set_id = self._get_value(self.test_run.scenario_set_id)
        if scenario_set_id:
            env_props.append(f"Scenario_Set_ID={scenario_set_id}")

        data_point_count = self._get_value(self.test_run.test_data_point_count)
        if data_point_count:
            env_props.append(f"Data_Point_Count={data_point_count}")

        app_link = self._get_value(self.test_run.app_link)
        if app_link:
            env_props.append(f"Okareo_App_Link={app_link}")

        env_props.append(f"Pass_Threshold={self.pass_threshold}")
        env_props.append("Framework=Okareo")

        env_path = os.path.join(self.output_dir, "environment.properties")
        with open(env_path, "w", encoding="utf-8") as f:
            f.write("\n".join(env_props))

    def _write_categories(self) -> None:
        """Write categories.json for failure classification in Allure."""
        categories = [
            {
                "name": "Execution Errors",
                "matchedStatuses": ["broken"],
                "messageRegex": ".*",
            },
            {
                "name": "Check Failures",
                "matchedStatuses": ["failed"],
                "messageRegex": ".*Failed checks.*",
            },
            {
                "name": "Threshold Failures",
                "matchedStatuses": ["failed"],
                "messageRegex": ".*threshold.*",
            },
        ]

        categories_path = os.path.join(self.output_dir, "categories.json")
        with open(categories_path, "w", encoding="utf-8") as f:
            json.dump(categories, f, indent=2)

    def _write_json(self, filename: str, data: Dict[str, Any]) -> None:
        """Write a JSON file to the output directory."""
        file_path = os.path.join(self.output_dir, filename)
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, default=str)

    def _build_test_name(
        self, dp: Union[FullDataPointItem, TestDataPointItem], scenario_id: str
    ) -> str:
        """Build a descriptive test name from the data point."""
        # Try to get a meaningful name from scenario input
        scenario_input = self._get_value(getattr(dp, "scenario_input", None))

        if scenario_input:
            if isinstance(scenario_input, str):
                # Use first 50 chars of string input
                return self._truncate(scenario_input, 50)
            elif isinstance(scenario_input, dict):
                # Try common keys for a name
                for key in ["name", "question", "query", "input", "text", "prompt"]:
                    if key in scenario_input:
                        return self._truncate(str(scenario_input[key]), 50)

        # Fall back to scenario ID
        if scenario_id:
            return f"Scenario {scenario_id[:8]}"

        return f"Data Point {dp.id[:8]}"

    def _generate_history_id(self, scenario_id: str, test_run_id: str) -> str:
        """
        Generate a unique history ID for each test case.
        
        By including the test_run_id, each run's scenarios appear as separate
        test cases in the Allure report, rather than being collapsed as retries.
        """
        key = f"{test_run_id}:{scenario_id}"
        return hashlib.md5(key.encode()).hexdigest()

    @staticmethod
    def _to_millis(dt: Any) -> Optional[int]:
        """Convert datetime to milliseconds timestamp."""
        if dt is None:
            return None
        if isinstance(dt, datetime):
            return int(dt.timestamp() * 1000)
        if isinstance(dt, str):
            try:
                from dateutil.parser import isoparse

                parsed = isoparse(dt)
                return int(parsed.timestamp() * 1000)
            except Exception:
                return None
        return None

    @staticmethod
    def _get_value(value: Any) -> Any:
        """Get value, returning None if it's Unset."""
        if isinstance(value, Unset):
            return None
        return value

    @staticmethod
    def _to_dict(value: Any) -> Dict[str, Any]:
        """Convert a value to a dict, handling model objects with additional_properties."""
        if value is None or isinstance(value, Unset):
            return {}
        if hasattr(value, "additional_properties"):
            return value.additional_properties
        if hasattr(value, "to_dict"):
            return value.to_dict()
        if isinstance(value, dict):
            return value
        return {}

    @staticmethod
    def _stringify(value: Any) -> str:
        """Convert any value to a string representation."""
        if isinstance(value, str):
            return value
        try:
            return json.dumps(value, indent=2, default=str)
        except Exception:
            return str(value)

    @staticmethod
    def _truncate(text: str, max_length: int) -> str:
        """Truncate text to max length with ellipsis."""
        if len(text) <= max_length:
            return text
        return text[: max_length - 3] + "..."

