from __future__ import annotations

from seatrace_4p3l.schemas.agent_outputs import HandoffPacketOutput


def build_handoff(next_owner: str, blockers: tuple[str, ...]) -> HandoffPacketOutput:
    return HandoffPacketOutput(
        next_owner=next_owner,
        ready_for_handoff=len(blockers) == 0,
        blocked_reasons=blockers,
    )
