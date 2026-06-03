from typing import Any

import pytest
from okareo_tests.common import API_KEY, random_string

from okareo import Okareo


def _detail_text(response: Any) -> str:
    try:
        body = response.json()
    except Exception:
        return str(getattr(response, "text", ""))

    if isinstance(body, dict):
        detail = body.get("detail")
        if isinstance(detail, str):
            return detail
    return str(body)


def _request(
    okareo: Okareo,
    *,
    method: str,
    url: str,
    api_key: str,
    json_body: dict[str, Any] | None = None,
) -> Any:
    headers = {"api-key": api_key}
    if json_body is not None:
        headers["Content-Type"] = "application/json"
    return okareo.client.get_httpx_client().request(
        method=method,
        url=url,
        json=json_body,
        headers=headers,
    )


def _post_token_exchange(okareo: Okareo, identity_proof: str | None) -> Any:
    headers: dict[str, str] = {}
    if identity_proof is not None:
        headers["api-key"] = identity_proof
    return okareo.client.get_httpx_client().request(
        method="post",
        url="/v0/auth/token/exchange",
        headers=headers,
    )


@pytest.fixture(scope="module")
def okareo() -> Okareo:
    if API_KEY == "no-api-key":
        pytest.skip("Set OKAREO_API_KEY to run auth/admin E2E tests.")
    try:
        return Okareo(api_key=API_KEY)
    except Exception as exc:
        pytest.skip(f"Could not initialize Okareo client for E2E tests: {exc}")


@pytest.fixture(scope="module")
def exchanged_session_token(okareo: Okareo) -> str:
    response = _post_token_exchange(okareo, API_KEY)
    detail = _detail_text(response)

    if response.status_code == 200:
        payload = response.json()
        token = payload.get("token") if isinstance(payload, dict) else None
        assert isinstance(token, str) and token
        return token

    pytest.fail(
        "Token exchange failed using OKAREO_API_KEY as identity proof token. "
        f"status={response.status_code} detail={detail}"
    )


def test_token_exchange_success_returns_session_token(
    exchanged_session_token: str,
) -> None:
    assert isinstance(exchanged_session_token, str)
    assert len(exchanged_session_token) > 20


def test_token_exchange_missing_identity_proof_returns_401(okareo: Okareo) -> None:
    response = _post_token_exchange(okareo, None)
    if response.status_code == 200:
        pytest.skip("Environment does not appear to be in cloud mode.")
    assert response.status_code == 401
    assert "Missing identity proof" in _detail_text(response)


def test_token_exchange_malformed_identity_proof_returns_401(okareo: Okareo) -> None:
    response = _post_token_exchange(okareo, "not-a-jwt")
    if response.status_code == 200:
        pytest.skip("Environment does not appear to be in cloud mode.")

    detail = _detail_text(response)
    if response.status_code == 500 and "Frontegg verification not configured" in detail:
        pytest.skip("Cloud token verification is not configured in this environment.")

    assert response.status_code == 401
    assert "Invalid Frontegg token" in detail


def test_api_key_lifecycle_and_token_usability(
    okareo: Okareo, exchanged_session_token: str
) -> None:
    created_key_ids: list[str] = []
    created_marker = f"e2e-auth-{random_string(10)}"

    try:
        create_response = _request(
            okareo,
            method="post",
            url="/v0/api-keys",
            api_key=exchanged_session_token,
            json_body={"description": created_marker},
        )
        assert create_response.status_code == 200, (
            f"create api-key returned {create_response.status_code}: "
            f"{create_response.text}"
        )
        create_payload = create_response.json()
        assert isinstance(create_payload, dict)

        created_row_id = create_payload.get("id")
        raw_api_key = create_payload.get("key")
        assert isinstance(created_row_id, str) and created_row_id
        assert isinstance(raw_api_key, str) and raw_api_key
        created_key_ids.append(created_row_id)

        protected_response = _request(
            okareo,
            method="get",
            url="/v0/projects",
            api_key=raw_api_key,
        )
        assert protected_response.status_code in (200, 201), (
            f"newly created token did not authenticate protected call: "
            f"{protected_response.status_code} {protected_response.text}"
        )

        list_response = _request(
            okareo,
            method="get",
            url="/v0/api-keys",
            api_key=exchanged_session_token,
        )
        assert list_response.status_code == 200
        items = list_response.json()
        assert isinstance(items, list)

        created_item = next(
            (
                item
                for item in items
                if isinstance(item, dict) and item.get("id") == created_row_id
            ),
            None,
        )
        assert isinstance(created_item, dict)
        assert created_item.get("source") == "okareo"

        delete_response = _request(
            okareo,
            method="delete",
            url=f"/v0/api-keys/{created_row_id}",
            api_key=exchanged_session_token,
        )
        assert delete_response.status_code in (200, 204)

        post_delete_list = _request(
            okareo,
            method="get",
            url="/v0/api-keys",
            api_key=exchanged_session_token,
        )
        if post_delete_list.status_code == 200:
            post_items = post_delete_list.json()
            if isinstance(post_items, list):
                post_item = next(
                    (
                        item
                        for item in post_items
                        if isinstance(item, dict) and item.get("id") == created_row_id
                    ),
                    None,
                )
                if isinstance(post_item, dict):
                    assert post_item.get("revoked_at") is not None

    finally:
        for key_id in created_key_ids:
            cleanup_response = _request(
                okareo,
                method="delete",
                url=f"/v0/api-keys/{key_id}",
                api_key=exchanged_session_token,
            )
            if cleanup_response.status_code not in (200, 204, 404):
                print(
                    f"cleanup warning: key_id={key_id} status={cleanup_response.status_code}"
                )


@pytest.mark.parametrize(
    "admin_path",
    [
        "/v0/admin/profile",
        "/v0/admin/account",
        "/v0/admin/users",
    ],
)
def test_admin_read_endpoints_best_effort(
    okareo: Okareo, exchanged_session_token: str, admin_path: str
) -> None:
    response = _request(
        okareo,
        method="get",
        url=admin_path,
        api_key=exchanged_session_token,
    )

    assert response.status_code < 500, (
        f"admin read endpoint exploded: "
        f"{response.status_code} {response.text}"
    )
    if response.status_code == 200:
        payload = response.json()
        assert isinstance(payload, dict)

