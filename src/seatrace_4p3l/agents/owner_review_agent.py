from __future__ import annotations

from seatrace_4p3l.schemas.agent_outputs import OwnerReviewSummary


def summarize_for_owner(summary: str, recommendation: str) -> OwnerReviewSummary:
    return OwnerReviewSummary(summary=summary, recommendation=recommendation)
