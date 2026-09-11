from __future__ import annotations

import json
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[1]
FIXTURES = ROOT / "data" / "fixtures"


def load_fixture(name: str) -> dict[str, object]:
    return json.loads((FIXTURES / name).read_text())


@pytest.fixture
def incoming_receiving_fixture() -> dict[str, object]:
    return load_fixture("incoming_receiving.public.json")


@pytest.fixture
def finished_product_fixture() -> dict[str, object]:
    return load_fixture("finished_product_index.public.json")


@pytest.fixture
def buyer_trace_fixture() -> dict[str, object]:
    return load_fixture("buyer_po_reverse_trace.public.json")
