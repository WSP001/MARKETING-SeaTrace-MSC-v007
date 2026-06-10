from __future__ import annotations

from seatrace_4p3l.gates.blocked_terms import scan_text
from seatrace_4p3l.schemas.agent_outputs import BoundaryReviewOutput
from seatrace_4p3l.schemas.enums import GateStatus


def review_public_boundary(text: str) -> BoundaryReviewOutput:
    hits = scan_text(text)
    if hits:
        return BoundaryReviewOutput(
            gate_status=GateStatus.FAIL,
            findings=tuple(hits),
            recommended_fix="Replace public-risk wording with scenario-safe labels.",
        )
    return BoundaryReviewOutput(
        gate_status=GateStatus.PASS,
        findings=(),
        recommended_fix="No boundary change required.",
    )
