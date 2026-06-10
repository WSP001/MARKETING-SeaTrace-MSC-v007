from __future__ import annotations

from seatrace_4p3l.gates.owner_go_gate import owner_go_granted


def test_owner_go_gate_returns_true_only_for_exact_owner_go_token():
    assert owner_go_granted("OWNER-GO") is True


def test_owner_go_gate_returns_false_for_none():
    assert owner_go_granted(None) is False


def test_owner_go_gate_returns_false_for_other_strings():
    assert owner_go_granted("") is False
    assert owner_go_granted("owner-go") is False
    assert owner_go_granted(" OWNER-GO") is False
    assert owner_go_granted("OWNER-GO ") is False
    assert owner_go_granted("SOME-OTHER-TOKEN") is False
