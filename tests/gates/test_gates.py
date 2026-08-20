from __future__ import annotations

from pathlib import Path

from seatrace_4p3l.gates.no_orphan_event_gate import validate_no_orphans
from seatrace_4p3l.gates.public_private_gate import validate_public_private_boundary
from seatrace_4p3l.gates.risky_term_gate import scan_paths


FIXTURE_DIR = Path("data/fixtures")


def test_public_private_gate_passes_fixture_contracts():
    assert validate_public_private_boundary(FIXTURE_DIR) == []


def test_no_orphan_event_gate_finds_complete_spine():
    assert validate_no_orphans(FIXTURE_DIR) == []


def test_risky_term_gate_passes_harness_public_surfaces():
    assert scan_paths((Path("src/seatrace_4p3l"), FIXTURE_DIR)) == []
