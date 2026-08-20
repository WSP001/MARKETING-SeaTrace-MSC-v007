from __future__ import annotations

from seatrace_4p3l.agents.boundary_review_agent import review_public_boundary


def test_boundary_review_agent_passes_safe_copy():
    output = review_public_boundary("Scenario-safe public proof chain with private values withheld.")

    assert output.gate_status == "PASS"
    assert output.findings == ()


def test_boundary_review_agent_flags_live_claims():
    output = review_public_boundary("This is a live API integration.")

    assert output.gate_status == "FAIL"
    assert "live API" in output.findings
