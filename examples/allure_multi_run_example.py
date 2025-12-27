"""
Allure Multi-Run Report Generator for Okareo

This script generates Allure reports from multiple historical Okareo test runs,
allowing you to view and compare evaluations across time in a single dashboard.

Features:
- Fetch test runs by project ID, model ID, scenario ID, tags, or test type
- Generate aggregated Allure results for all matching runs
- Allure's history tracking allows comparison across runs
- Filter by date range (requires manual filtering of results)

Prerequisites:
    1. pip install okareo
    2. Install Allure CLI: https://allurereport.org/docs/install/

Usage:
    1. Set environment variables:
       export OKAREO_API_KEY=your_key
       export BASE_URL=https://api.okareo.com  # or your server URL
    
    2. Run this script with desired filters:
       python allure_multi_run_example.py --project-id YOUR_PROJECT_ID
       python allure_multi_run_example.py --tags simulation,production
       python allure_multi_run_example.py --type MULTI_TURN --limit 10
    
    3. Generate and view the report:
       allure generate -o allure-report --open allure-results
"""

import argparse
import os
import sys
from datetime import datetime
from typing import Any, Dict, List, Optional

import httpx

from okareo import Okareo
from okareo.allure_reporter import AllureReporter
from okareo_api_client.models import (
    FindTestDataPointPayload,
    TestRunItem,
)


class MultiRunAllureGenerator:
    """
    Generates Allure reports from multiple Okareo test runs.

    This class fetches test runs based on various filter criteria and generates
    a unified Allure report that allows viewing all evaluations in a single dashboard.
    """

    def __init__(
        self,
        api_key: str,
        base_url: str = "https://api.okareo.com",
        output_dir: str = "./allure-results",
        pass_threshold: float = 0.5,
    ):
        """
        Initialize the multi-run generator.

        Args:
            api_key: Okareo API key
            base_url: Base URL for Okareo API
            output_dir: Directory for Allure result files
            pass_threshold: Threshold for pass/fail determination (0.0-1.0)
        """
        self.api_key = api_key
        self.base_url = base_url.rstrip("/")
        self.output_dir = output_dir
        self.pass_threshold = pass_threshold
        self.okareo = Okareo(api_key=api_key, base_path=base_url)
        self.http_client = httpx.Client(timeout=60.0)

    def find_test_runs(
        self,
        project_id: Optional[str] = None,
        mut_id: Optional[str] = None,
        scenario_set_id: Optional[str] = None,
        tags: Optional[List[str]] = None,
        types: Optional[List[str]] = None,
        limit: Optional[int] = None,
    ) -> List[TestRunItem]:
        """
        Find test runs matching the specified criteria.

        Args:
            project_id: Filter by project ID
            mut_id: Filter by model under test ID
            scenario_set_id: Filter by scenario set ID
            tags: Filter by tags (all specified tags must match)
            types: Filter by test run types (e.g., ["MULTI_TURN", "NL_GENERATION"])
            limit: Maximum number of runs to return

        Returns:
            List of TestRunItem objects matching the criteria
        """
        # Build the payload
        payload: Dict[str, Any] = {
            "return_model_metrics": True,
            "return_error_matrix": False,
        }

        if project_id:
            payload["project_id"] = project_id
        if mut_id:
            payload["mut_id"] = mut_id
        if scenario_set_id:
            payload["scenario_set_id"] = scenario_set_id
        if tags:
            payload["tags"] = tags
        if types:
            payload["types"] = types

        # Make the API call directly
        response = self.http_client.post(
            f"{self.base_url}/v0/find_test_runs",
            json=payload,
            headers={"api-key": self.api_key},
        )

        if response.status_code not in (200, 201):
            raise RuntimeError(
                f"Failed to find test runs: {response.status_code} - {response.text}"
            )

        # Parse response into TestRunItem objects
        test_runs = []
        data = response.json()
        if isinstance(data, list):
            for item in data:
                if isinstance(item, dict):
                    test_runs.append(TestRunItem.from_dict(item))

        # Sort by start time (most recent first) and apply limit
        test_runs.sort(
            key=lambda x: x.start_time if x.start_time else datetime.min,
            reverse=True,
        )

        if limit:
            test_runs = test_runs[:limit]

        return test_runs

    def get_test_run(self, test_run_id: str) -> TestRunItem:
        """Fetch a single test run by ID."""
        response = self.http_client.get(
            f"{self.base_url}/v0/test_runs/{test_run_id}",
            headers={"api-key": self.api_key},
        )

        if response.status_code not in (200, 201):
            raise RuntimeError(
                f"Failed to get test run {test_run_id}: {response.status_code} - {response.text}"
            )

        data = response.json()
        return TestRunItem.from_dict(data)

    def generate_report(
        self,
        test_runs: Optional[List[TestRunItem]] = None,
        test_run_ids: Optional[List[str]] = None,
        **find_kwargs,
    ) -> str:
        """
        Generate Allure report for multiple test runs.

        You can either:
        1. Pass test_runs directly
        2. Pass test_run_ids to fetch
        3. Pass filter kwargs to find matching runs

        Args:
            test_runs: List of TestRunItem objects
            test_run_ids: List of test run IDs to fetch
            **find_kwargs: Arguments to pass to find_test_runs()

        Returns:
            Path to the output directory
        """
        # Determine which test runs to process
        runs_to_process: List[TestRunItem] = []

        if test_runs:
            runs_to_process = test_runs
        elif test_run_ids:
            print(f"Fetching {len(test_run_ids)} test runs by ID...")
            for run_id in test_run_ids:
                try:
                    run = self.get_test_run(run_id)
                    runs_to_process.append(run)
                except Exception as e:
                    print(f"  Warning: Failed to fetch {run_id}: {e}")
        else:
            print("Finding test runs with specified filters...")
            runs_to_process = self.find_test_runs(**find_kwargs)

        if not runs_to_process:
            print("No test runs found matching the criteria.")
            return self.output_dir

        print(f"Found {len(runs_to_process)} test runs to process")

        # Clear existing results directory
        os.makedirs(self.output_dir, exist_ok=True)

        # Process each test run
        total_data_points = 0
        for i, test_run in enumerate(runs_to_process, 1):
            run_name = test_run.name if test_run.name else test_run.id
            print(f"\n[{i}/{len(runs_to_process)}] Processing: {run_name}")
            print(f"  ID: {test_run.id}")
            print(f"  Type: {test_run.type}")
            print(f"  Status: {test_run.status}")

            try:
                # Fetch data points for this run
                data_points = self.okareo.find_test_data_points(
                    FindTestDataPointPayload(
                        test_run_id=test_run.id,
                        full_data_point=True,
                    )
                )

                if not data_points:
                    print(f"  Warning: No data points found for this run")
                    continue

                print(f"  Data points: {len(data_points)}")
                total_data_points += len(data_points)

                # Generate Allure results for this run
                reporter = AllureReporter(
                    test_run=test_run,
                    data_points=data_points,
                    pass_threshold=self.pass_threshold,
                    output_dir=self.output_dir,
                    include_attachments=True,
                )
                reporter.generate()

            except Exception as e:
                print(f"  Error processing run: {e}")
                continue

        print(f"\n{'='*60}")
        print(f"Report generation complete!")
        print(f"  Test runs processed: {len(runs_to_process)}")
        print(f"  Total data points: {total_data_points}")
        print(f"  Output directory: {self.output_dir}")
        print(f"\nTo view the report, run:")
        print(f"  allure generate -o allure-report --open {self.output_dir}")

        return self.output_dir


def main():
    parser = argparse.ArgumentParser(
        description="Generate Allure reports from multiple Okareo test runs",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # All runs for a project
  python allure_multi_run_example.py --project-id abc123

  # Runs with specific tags
  python allure_multi_run_example.py --tags simulation,v2

  # Multi-turn simulations only, limit 5
  python allure_multi_run_example.py --type MULTI_TURN --limit 5

  # Specific test run IDs
  python allure_multi_run_example.py --run-ids id1,id2,id3

  # By model under test
  python allure_multi_run_example.py --model-id model123
        """,
    )

    parser.add_argument(
        "--project-id",
        help="Filter by project ID",
    )
    parser.add_argument(
        "--model-id",
        help="Filter by model under test ID",
    )
    parser.add_argument(
        "--scenario-id",
        help="Filter by scenario set ID",
    )
    parser.add_argument(
        "--tags",
        help="Filter by tags (comma-separated)",
    )
    parser.add_argument(
        "--type",
        choices=[
            "MULTI_CLASS_CLASSIFICATION",
            "NL_GENERATION",
            "INFORMATION_RETRIEVAL",
            "TEXT_RERANKER",
            "MULTI_TURN",
            "MULTI_TURN_DRIVER",
        ],
        help="Filter by test run type",
    )
    parser.add_argument(
        "--run-ids",
        help="Specific test run IDs (comma-separated)",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=20,
        help="Maximum number of runs to process (default: 20)",
    )
    parser.add_argument(
        "--threshold",
        type=float,
        default=0.5,
        help="Pass/fail threshold for checks (default: 0.5)",
    )
    parser.add_argument(
        "--output",
        default="./allure-results",
        help="Output directory for Allure results (default: ./allure-results)",
    )
    parser.add_argument(
        "--open",
        action="store_true",
        help="Open the report in browser after generation",
    )

    args = parser.parse_args()

    # Get credentials from environment
    api_key = os.environ.get("OKAREO_API_KEY")
    base_url = os.environ.get("BASE_URL", "https://api.okareo.com")

    if not api_key:
        print("Error: OKAREO_API_KEY environment variable is required")
        sys.exit(1)

    # Check that at least one filter is provided
    has_filter = any([
        args.project_id,
        args.model_id,
        args.scenario_id,
        args.tags,
        args.type,
        args.run_ids,
    ])

    if not has_filter:
        print("Error: At least one filter must be provided.")
        print("Use --help to see available options.")
        sys.exit(1)

    # Initialize generator
    generator = MultiRunAllureGenerator(
        api_key=api_key,
        base_url=base_url,
        output_dir=args.output,
        pass_threshold=args.threshold,
    )

    # Build kwargs for find_test_runs
    find_kwargs = {"limit": args.limit}

    if args.project_id:
        find_kwargs["project_id"] = args.project_id
    if args.model_id:
        find_kwargs["mut_id"] = args.model_id
    if args.scenario_id:
        find_kwargs["scenario_set_id"] = args.scenario_id
    if args.tags:
        find_kwargs["tags"] = [t.strip() for t in args.tags.split(",")]
    if args.type:
        find_kwargs["types"] = [args.type]

    # Generate the report
    if args.run_ids:
        run_ids = [r.strip() for r in args.run_ids.split(",")]
        output_path = generator.generate_report(test_run_ids=run_ids)
    else:
        output_path = generator.generate_report(**find_kwargs)

    # Optionally open the report
    if args.open:
        import subprocess

        print("\nGenerating and opening Allure report...")
        subprocess.run(
            ["allure", "generate", "-o", "allure-report", "--open", output_path],
            check=True,
        )


def example_programmatic_usage():
    """
    Example showing programmatic usage without CLI arguments.
    """
    api_key = os.environ.get("OKAREO_API_KEY")
    base_url = os.environ.get("BASE_URL", "https://api.okareo.com")

    generator = MultiRunAllureGenerator(
        api_key=api_key,
        base_url=base_url,
        output_dir="./allure-results",
        pass_threshold=0.7,
    )

    # Example 1: Get all MULTI_TURN runs for a project
    generator.generate_report(
        project_id="your-project-id",
        types=["MULTI_TURN"],
        limit=10,
    )

    # Example 2: Get runs by specific IDs
    generator.generate_report(
        test_run_ids=[
            "run-id-1",
            "run-id-2",
            "run-id-3",
        ]
    )

    # Example 3: Get runs with specific tags
    generator.generate_report(
        tags=["production", "v2"],
        limit=50,
    )

    # Example 4: Combine multiple filters
    generator.generate_report(
        project_id="your-project-id",
        mut_id="your-model-id",
        types=["NL_GENERATION"],
        tags=["regression"],
        limit=20,
    )


def example_with_date_filtering():
    """
    Example showing how to filter by date after fetching runs.
    (Date filtering is done client-side since the API doesn't support it directly)
    """
    from datetime import datetime, timedelta

    api_key = os.environ.get("OKAREO_API_KEY")
    base_url = os.environ.get("BASE_URL", "https://api.okareo.com")

    generator = MultiRunAllureGenerator(
        api_key=api_key,
        base_url=base_url,
    )

    # Fetch runs
    all_runs = generator.find_test_runs(
        project_id="your-project-id",
        limit=100,  # Fetch more to filter
    )

    # Filter by date (last 7 days)
    cutoff_date = datetime.now() - timedelta(days=7)
    recent_runs = [
        run
        for run in all_runs
        if run.start_time and run.start_time >= cutoff_date
    ]

    print(f"Found {len(recent_runs)} runs from the last 7 days")

    # Generate report for filtered runs
    generator.generate_report(test_runs=recent_runs)


if __name__ == "__main__":
    main()

