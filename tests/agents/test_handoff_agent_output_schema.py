from __future__ import annotations

from seatrace_4p3l.agents.handoff_agent import build_handoff
from seatrace_4p3l.agents.owner_review_agent import summarize_for_owner


def test_handoff_agent_marks_ready_only_without_blockers():
    ready = build_handoff("Antigravity", ())
    blocked = build_handoff("Owner", ("missing proof",))

    assert ready.ready_for_handoff is True
    assert blocked.ready_for_handoff is False


def test_owner_review_agent_never_grants_go():
    output = summarize_for_owner("Harness passed verification.", "Owner may review.")

    assert output.go_granted is False
