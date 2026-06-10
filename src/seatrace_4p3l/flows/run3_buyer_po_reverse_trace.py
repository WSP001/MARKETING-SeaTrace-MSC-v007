from __future__ import annotations

import json
from pathlib import Path

from seatrace_4p3l.etl.private_graph_adapter import collect_spine, require_full_spine
from seatrace_4p3l.schemas.public_packets import BuyerProofPacket


def run_buyer_po_reverse_trace(payload: dict[str, object]) -> dict[str, object]:
    proof = BuyerProofPacket.model_validate(payload["marketside"])
    spine = collect_spine(proof.model_dump())
    require_full_spine(spine)

    if proof.reverse_trace_status != "complete":
        raise ValueError("reverse trace is not complete")

    return {
        "buyer_proof_id": proof.buyer_proof_id,
        "proof_packet_status": proof.proof_packet_status,
        "reverse_trace_path": proof.reverse_trace_path,
        "spine": spine,
    }


def main() -> None:
    fixture = Path("data/fixtures/buyer_po_reverse_trace.public.json")
    payload = json.loads(fixture.read_text())
    print(json.dumps(run_buyer_po_reverse_trace(payload), indent=2, default=str))


if __name__ == "__main__":
    main()
