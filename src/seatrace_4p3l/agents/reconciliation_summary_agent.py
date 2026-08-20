from __future__ import annotations

from seatrace_4p3l.schemas.agent_outputs import ReconciliationSummaryOutput
from seatrace_4p3l.schemas.reconciliation import ReceivingReconciliationEvent


def summarize_reconciliation(event: ReceivingReconciliationEvent) -> ReconciliationSummaryOutput:
    return ReconciliationSummaryOutput(
        scenario_id=event.scenario_id,
        variance_label=event.variance_label.value,
        buyer_safe_summary=f"Scenario receiving variance is {event.variance_label.value}; private math remains withheld.",
    )
