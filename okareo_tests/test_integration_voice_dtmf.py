"""E2E DTMF validation against the IVR testtarget, for both Twilio and Vonage.

The Driver places a phone call (via a Twilio or Vonage voice target) to a number
routed to okareo_server's opt-in IVR testtarget
(``/v0/voice/twilio/testtarget/ivr``). The Driver presses a random keypad code;
the testtarget captures it — from Twilio Media-Stream ``dtmf`` events (the
out-of-band path Vonage uses) or, failing that, by decoding in-band tones from the
received audio — and stores it. This test then reads it back and asserts
``sent == received``, and runs the model-graded ``result_completed`` check against
a rubric that fails on a partial/absent sequence.

This is a live-telephony integration test — it is SKIPPED unless the rig is
configured. To run it you need:
  - okareo_server running locally with the IVR testtarget routes, reachable by the
    telephony provider (e.g. via ngrok); OKAREO_BASE_PATH points at it.
  - A phone number (IVR_TO_NUMBER) whose voice webhook hits the IVR testtarget.
  - Provider credentials (Twilio and/or Vonage) for the Driver's outbound edge.

Env:
  OKAREO_API_KEY, OKAREO_BASE_PATH (default http://localhost:8000), IVR_TO_NUMBER
  Twilio: TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, TWILIO_FROM_NUMBER
  Vonage: VONAGE_APPLICATION_ID, VONAGE_FROM_NUMBER, VONAGE_PRIVATE_KEY_PATH
  Optional driver voice: DEEPGRAM_API_KEY or OPENAI_API_KEY
"""

import os
import random
import time
from pathlib import Path

import pytest
import requests  # type: ignore

from okareo import Okareo
from okareo.model_under_test import (
    Driver,
    Target,
    TwilioVoiceTarget,
    VonagePhoneTarget,
)
from okareo_api_client.models.scenario_set_create import ScenarioSetCreate
from okareo_tests.common import API_KEY, random_string

OKAREO_BASE_PATH = os.environ.get("OKAREO_BASE_PATH", "http://localhost:8000")
IVR_TO_NUMBER = os.environ.get("IVR_TO_NUMBER", "")

TWILIO_ACCOUNT_SID = os.environ.get("TWILIO_ACCOUNT_SID", "")
TWILIO_AUTH_TOKEN = os.environ.get("TWILIO_AUTH_TOKEN", "")
TWILIO_FROM_NUMBER = os.environ.get("TWILIO_FROM_NUMBER", "")

VONAGE_APPLICATION_ID = os.environ.get("VONAGE_APPLICATION_ID", "")
VONAGE_FROM_NUMBER = os.environ.get("VONAGE_FROM_NUMBER", "")
VONAGE_PRIVATE_KEY_PATH = os.environ.get("VONAGE_PRIVATE_KEY_PATH", "")

# result_completed grades the target's utterances against this rubric. It is a
# model-graded companion to the deterministic readback assertion below (which
# already validates the full sequence, terminator included) — so it grades the
# digit echo and tolerates the trailing '#'/pound being lost in TTS->STT.
_RESULT_RUBRIC = (
    "Target audibly repeats back the digit sequence the driver pressed. Missing "
    "digits or no repeat back is a failure. The trailing pound/# terminator may be "
    "lost in speech transcription and does not by itself count as a partial."
)

_HAVE_COMMON = bool(IVR_TO_NUMBER and os.environ.get("OKAREO_API_KEY"))
_HAVE_TWILIO = bool(TWILIO_ACCOUNT_SID and TWILIO_AUTH_TOKEN and TWILIO_FROM_NUMBER)
_HAVE_VONAGE = bool(
    VONAGE_APPLICATION_ID and VONAGE_FROM_NUMBER and VONAGE_PRIVATE_KEY_PATH
)


def _driver_prompt(code: str) -> str:
    """Minimal, deterministic scenario: enter exactly ``code`` then pound.

    The send_dtmf skill (composed server-side) supplies the keypad mechanics
    (silent keypress, whole value in one press); this template supplies only the
    code and the goal.
    """
    return (
        f"You are calling an automated test line. Your account number is {code}.\n"
        "When the automated menu asks you to enter your account number followed "
        f"by the pound key, enter it on the keypad as a single entry: {code} then "
        "'#'. Do NOT say the number out loud — enter it on the keypad.\n"
        "After you have entered it and the system acknowledges, end the call "
        "politely. Keep every spoken turn to one short sentence."
    )


def _build_target(provider: str) -> object:
    if provider == "twilio":
        return TwilioVoiceTarget(
            account_sid=TWILIO_ACCOUNT_SID,
            auth_token=TWILIO_AUTH_TOKEN,
            from_phone_number=TWILIO_FROM_NUMBER,
            to_phone_number=IVR_TO_NUMBER,
        )
    if provider == "vonage":
        # DTMF (both OOB rfc4733 + in-band), recording, and 16 kHz are fixed
        # server-side defaults — not configurable on the target. The testtarget
        # captures the keypress via whichever path reaches it (dtmf event or
        # in-band audio).
        return VonagePhoneTarget(
            to_phone_number=IVR_TO_NUMBER,
            from_phone_number=VONAGE_FROM_NUMBER,
            application_id=VONAGE_APPLICATION_ID,
            private_key=Path(VONAGE_PRIVATE_KEY_PATH).read_text(),
        )
    raise ValueError(f"unknown provider: {provider}")


def _poll_readback(expected: str, timeout_s: float = 30.0) -> str:
    """Poll the testtarget for the DTMF it captured for the most recent call.

    A fresh, unique code per test makes ``latest`` safe against a stale value from
    a prior provider's run: only this call's digits will equal ``expected``.
    """
    url = f"{OKAREO_BASE_PATH.rstrip('/')}/v0/voice/twilio/testtarget/ivr/dtmf/latest"
    deadline = time.time() + timeout_s
    seen = ""
    while time.time() < deadline:
        try:
            r = requests.get(url, timeout=5.0)
            if r.status_code == 200:
                seen = (r.json() or {}).get("digits", "") or ""
                if seen == expected:
                    return seen
        except requests.RequestException:
            pass
        time.sleep(1.5)
    return seen


@pytest.mark.parametrize(
    "provider",
    [
        pytest.param(
            "twilio",
            marks=pytest.mark.skipif(
                not (_HAVE_COMMON and _HAVE_TWILIO),
                reason="Twilio DTMF rig not configured (IVR_TO_NUMBER + TWILIO_*).",
            ),
        ),
        pytest.param(
            "vonage",
            marks=pytest.mark.skipif(
                not (_HAVE_COMMON and _HAVE_VONAGE),
                reason="Vonage DTMF rig not configured (IVR_TO_NUMBER + VONAGE_*).",
            ),
        ),
    ],
)
def test_ivr_dtmf_sent_and_received(provider: str) -> None:
    """Driver presses a random code; the IVR testtarget must receive it intact.

    Deterministic gate: the testtarget's captured digits (read back) equal what the
    Driver pressed. The ``result_completed`` check additionally grades — model-based
    — whether the target vocalized the full sequence (partial = fail).
    """
    okareo = Okareo(api_key=API_KEY, base_path=OKAREO_BASE_PATH)
    code = f"{random.randint(1000, 9999)}"  # noqa: S311 — test nonce, not crypto
    expected = f"{code}#"

    api_keys = {}
    if os.environ.get("DEEPGRAM_API_KEY"):
        api_keys["voice"] = os.environ["DEEPGRAM_API_KEY"]
    elif os.environ.get("OPENAI_API_KEY"):
        api_keys["voice"] = os.environ["OPENAI_API_KEY"]

    scenario = okareo.create_scenario_set(
        ScenarioSetCreate(
            name=f"IVR DTMF e2e ({provider}) {random_string(4)}",
            seed_data=Okareo.seed_data_from_list(
                [{"input": {"name": "ivr caller", "voice": "oscar"}, "result": _RESULT_RUBRIC}]
            ),
        )
    )

    evaluation = okareo.run_simulation(
        name=f"IVR DTMF e2e ({provider})",
        scenario=scenario,
        target=Target(name=f"IVR DTMF {provider} target", target=_build_target(provider)),
        driver=Driver(
            name=f"IVR DTMF {provider} driver",
            temperature=0.2,
            prompt_template=_driver_prompt(code),
        ),
        max_turns=6,
        repeats=1,
        first_turn="target",
        checks=["avg_turn_latency", "result_completed"],
        api_keys=api_keys or None,
    )

    assert getattr(evaluation, "status", "") == "FINISHED", (
        f"[{provider}] simulation did not finish: "
        f"status={getattr(evaluation, 'status', '?')} app_link={getattr(evaluation, 'app_link', None)}"
    )

    received = _poll_readback(expected)
    assert received == expected, (
        f"[{provider}] IVR testtarget received {received!r}, expected {expected!r} — "
        f"partial or missing DTMF. app_link={getattr(evaluation, 'app_link', None)}"
    )
