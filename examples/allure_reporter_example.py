"""
Allure Report Integration Example for Okareo

This example demonstrates how to use the AllureReporter to generate
Allure-compatible reports from Okareo evaluation results.

Prerequisites:
    1. pip install okareo allure-pytest  # or just okareo
    2. Install Allure CLI: https://allurereport.org/docs/install/
       - macOS: brew install allure
       - Linux: sudo apt-add-repository ppa:qameta/allure && sudo apt install allure
       - Windows: scoop install allure

Usage:
    1. Set your API key: export OKAREO_API_KEY=your_key
    2. Run this script: python allure_reporter_example.py
    3. Generate and view HTML report (Allure 3):
       allure generate -o allure-report --open allure-results
"""

import os

from okareo import Okareo, AllureReporter
from okareo_api_client.models import (
    FindTestDataPointPayload,
    ScenarioSetCreate,
    TestRunType,
)


def main():
    # Initialize Okareo client
    api_key = os.environ.get("OKAREO_API_KEY")
    base_url = os.environ.get("BASE_URL")
    openai_api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OKAREO_API_KEY environment variable is required")
    if not base_url:
        raise ValueError("BASE_URL environment variable is required")

    okareo = Okareo(api_key=api_key, base_path=base_url)

    # Create a simple scenario set for demonstration
    seed_data = okareo.seed_data_from_list([
        {
            "input": "What is the capital of France?",
            "result": "Paris"
        },
        {
            "input": "What is 2 + 2?",
            "result": "4"
        },
        {
            "input": "Who wrote Romeo and Juliet?",
            "result": "William Shakespeare"
        },
    ])

    scenario = okareo.create_scenario_set(
        ScenarioSetCreate(
            name="Allure Demo Scenario",
            seed_data=seed_data,
        )
    )

    print(f"Created scenario set: {scenario.scenario_id}")

    # Register a model (using OpenAI as example)
    # Replace with your actual model configuration
    from okareo.model_under_test import OpenAIModel

    model = okareo.register_model(
        name="allure-demo-model",
        model=OpenAIModel(
            model_id="gpt-4o-mini",
            temperature=0,
            system_prompt_template="Answer the question concisely in one word or short phrase.",
        ),
    )

    print(f"Registered model: {model.mut_id}")

    # Run evaluation with checks
    test_run = model.run_test(
        scenario=scenario,
        name="Allure Demo Evaluation",
        test_run_type=TestRunType.NL_GENERATION,
        checks=["coherence_summary"],  # Use available checks
        calculate_metrics=True,
        api_key=openai_api_key,
    )

    print(f"Test run completed: {test_run.id}")
    print(f"View in Okareo: {test_run.app_link}")

    # Fetch detailed data points for the report
    data_points = okareo.find_test_data_points(
        FindTestDataPointPayload(
            test_run_id=test_run.id,
            full_data_point=True,  # Get full details including inputs/outputs
        )
    )

    print(f"Retrieved {len(data_points)} data points")

    # Generate Allure report
    reporter = AllureReporter(
        test_run=test_run,
        data_points=data_points,
        pass_threshold=0.5,  # Checks with score >= 0.5 pass
        output_dir="./allure-results",
        include_attachments=True,
    )

    output_path = reporter.generate()
    print(f"\nAllure results written to: {output_path}")
    print("\nTo generate and view the HTML report, run:")
    print("  # Allure 3 syntax:")
    print("  allure generate -o allure-report allure-results")
    print("  allure open allure-report")
    print("")
    print("  # Or generate and open in one command:")
    print("  allure generate -o allure-report --open allure-results")


def example_with_existing_test_run():
    """
    Example showing how to generate Allure report from an existing test run.

    This is useful when you want to generate reports from historical evaluations.
    """
    api_key = os.environ.get("OKAREO_API_KEY")
    okareo = Okareo(api_key=api_key)

    # Replace with your actual test run ID
    test_run_id = "your-existing-test-run-id"

    # You would need to fetch the test run first
    # (Note: This requires an API endpoint that may need to be added)
    # test_run = okareo.get_test_run(test_run_id)

    # Fetch data points
    data_points = okareo.find_test_data_points(
        FindTestDataPointPayload(
            test_run_id=test_run_id,
            full=True,
        )
    )

    # For this example, we'll create a minimal TestRunItem
    # In practice, you'd fetch this from the API
    from okareo_api_client.models import TestRunItem

    test_run = TestRunItem(
        id=test_run_id,
        project_id="your-project-id",
        name="Historical Evaluation",
    )

    reporter = AllureReporter(
        test_run=test_run,
        data_points=data_points,
        pass_threshold=0.7,
    )

    reporter.generate()


def example_custom_thresholds():
    """
    Example showing custom threshold configuration for different check types.

    You can use different AllureReporter instances with different thresholds
    to analyze results at various quality levels.
    """
    # ... (after running evaluation and getting test_run and data_points)

    # Strict threshold (for production readiness)
    strict_reporter = AllureReporter(
        test_run=None,  # Replace with actual test_run
        data_points=[],  # Replace with actual data_points
        pass_threshold=0.9,
        output_dir="./allure-results-strict",
    )

    # Lenient threshold (for development/exploration)
    lenient_reporter = AllureReporter(
        test_run=None,
        data_points=[],
        pass_threshold=0.3,
        output_dir="./allure-results-lenient",
    )


def example_pytest_integration():
    """
    Example showing integration with pytest for automated testing.

    Create a test file (e.g., test_model_evaluation.py) with:

    ```python
    import pytest
    from okareo import Okareo, AllureReporter
    from okareo_api_client.models import FindTestDataPointPayload

    @pytest.fixture
    def okareo_client():
        return Okareo(api_key=os.environ["OKAREO_API_KEY"])

    def test_model_accuracy(okareo_client):
        # ... run your evaluation ...
        test_run = model.run_test(...)

        data_points = okareo_client.find_test_data_points(
            FindTestDataPointPayload(test_run_id=test_run.id, full=True)
        )

        # Generate Allure report
        reporter = AllureReporter(
            test_run=test_run,
            data_points=data_points,
            pass_threshold=0.8,
        )
        reporter.generate()

        # Assert on metrics
        metrics = test_run.model_metrics
        assert metrics.get("accuracy", 0) >= 0.8
    ```

    Run with: pytest --alluredir=allure-results test_model_evaluation.py
    """
    pass


if __name__ == "__main__":
    main()

