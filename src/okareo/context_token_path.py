"""The one JSONPath to a conversation's context token, from a config's new or old keyword.

A context token is the app's own id for a conversation, often called a session ID
or conversation ID. The custom endpoint configs first named its path
``response_session_id_path``; they now name it ``response_context_token_path``
and keep the old name working. ``one_context_token_path`` takes the path given
under either keyword and refuses two different ones. What is sent to Okareo is
not renamed: the configs still send it under ``"response_session_id_path"``.
"""


def one_context_token_path(
    response_context_token_path: str, response_session_id_path: str
) -> str:
    """The path given under either keyword; refuses two different paths."""
    if (
        response_context_token_path
        and response_session_id_path
        and response_context_token_path != response_session_id_path
    ):
        raise ValueError(
            "Give response_context_token_path or response_session_id_path, not both: "
            f"they name the same path, and {response_context_token_path!r} and "
            f"{response_session_id_path!r} differ."
        )
    return response_context_token_path or response_session_id_path
