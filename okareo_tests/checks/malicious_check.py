import requests

from okareo.checks import CheckResponse, CodeBasedCheck


class Check(CodeBasedCheck):
    @staticmethod
    def evaluate(model_output: str) -> CheckResponse:  # type: ignore[override]
        """Malicious check that makes network requests and file system access."""
        # This should be blocked
        response = requests.get(
            "https://jsonplaceholder.typicode.com/posts/1", timeout=10
        )
        data = response.json()

        score = len(model_output) > 10
        explanation = f"Fetched data: {data.get('title', 'N/A')}"
        return CheckResponse(score=score, explanation=explanation)
