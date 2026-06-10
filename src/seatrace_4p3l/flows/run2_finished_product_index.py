from __future__ import annotations

import json
from pathlib import Path

from seatrace_4p3l.etl.finished_product_indexer import index_finished_product


def run_finished_product_index(payload: dict[str, object]) -> dict[str, object]:
    record = index_finished_product(payload)
    if record.qr_status != "public proof bundle ready":
        raise ValueError("finished product is not QR-ready")
    return {
        "source_harvest_id": record.source_harvest_id,
        "traceability_lot_code": record.traceability_lot_code,
        "sku_label": record.sku_label,
        "qr_status": record.qr_status,
    }


def main() -> None:
    fixture = Path("data/fixtures/finished_product_index.public.json")
    payload = json.loads(fixture.read_text())
    print(json.dumps(run_finished_product_index(payload), indent=2))


if __name__ == "__main__":
    main()
