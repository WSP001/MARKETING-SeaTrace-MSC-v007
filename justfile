set shell := ["bash", "-cu"]

python := ".venv/bin/python"

install:
    python3 -m venv .venv
    {{python}} -m pip install --upgrade pip
    {{python}} -m pip install -e ".[dev]"

schema-tests:
    {{python}} -m pytest tests/unit

flow-tests:
    {{python}} -m pytest tests/flows

agent-tests:
    {{python}} -m pytest tests/agents

gate-tests:
    {{python}} -m pytest tests/gates

gates:
    {{python}} -m seatrace_4p3l.gates.public_private_gate data/fixtures
    {{python}} -m seatrace_4p3l.gates.no_orphan_event_gate data/fixtures
    {{python}} -m seatrace_4p3l.gates.risky_term_gate src/seatrace_4p3l data/fixtures

owner-go:
    {{python}} -m seatrace_4p3l.gates.owner_go_gate --token "${OWNER_GO_TOKEN:-}"

run1:
    {{python}} -m seatrace_4p3l.flows.run1_incoming_receiving

run2:
    {{python}} -m seatrace_4p3l.flows.run2_finished_product_index

run3:
    {{python}} -m seatrace_4p3l.flows.run3_buyer_po_reverse_trace

verify: schema-tests flow-tests agent-tests gate-tests gates run1 run2 run3
