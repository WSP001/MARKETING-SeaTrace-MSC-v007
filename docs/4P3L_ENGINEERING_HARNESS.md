# SeaTrace 4P3L Engineering Harness

This repo now contains a separate engineering harness for the SeaTrace 4P3L packet model. The campaign repo is used only as a read-only reference source for packet contracts and safety rules.

## Scope

- Schemas: `src/seatrace_4p3l/schemas/`
- Fixtures: `data/fixtures/`
- ETL adapters: `src/seatrace_4p3l/etl/`
- Flows: `src/seatrace_4p3l/flows/`
- Agent contract wrappers: `src/seatrace_4p3l/agents/`
- Gates: `src/seatrace_4p3l/gates/`
- DB skeleton: `src/seatrace_4p3l/db/`
- Tests: `tests/`

## Contract spine

The fixture spine is:

```text
trip_id
  -> catch_estimate_id
      -> harvest_index_id
          -> traceability_lot_code
              -> buyer_proof_id
```

Run 1 builds SeaSide, DeckSide, and DockSide packets, then reconciles receiving. Run 2 indexes the finished product state. Run 3 validates the MarketSide buyer-proof packet and reverse path.

## Commands

```bash
just install
just verify
just gates
just run1
just run2
just run3
```

`just owner-go` intentionally blocks unless `OWNER_GO_TOKEN=OWNER-GO` is present. The harness can summarize readiness, but only the owner can grant GO.

## Safety posture

- Scenario fixtures use `SCN-` identifiers only.
- Public packet models reject forbidden claim phrases.
- Public/private gate validates that packet fixture sections do not include private field names.
- Risky-term gate scans harness source and public fixtures while excluding the gate policy source and private-record schema file.
- No live backend, no API credentials, no production deploy path, and no real customer/vessel/payment data are required.
