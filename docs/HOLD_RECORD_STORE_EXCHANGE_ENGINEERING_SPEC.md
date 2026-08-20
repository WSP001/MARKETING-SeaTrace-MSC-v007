# SeaTrace HOLD–RECORD–STORE–EXCHANGE Engineering Specification

Status: PROPOSED — branch review only  
Specification ID: ST-HRSE-001  
Repository scope: `WSP001/MARKETING-SeaTrace-MSC-v007`  
Architecture credit: Scott Echols / WSP001 — Commons Good

## 1. Control law

SeaTrace models one evidence history through four state transitions:

```text
SeaSide HOLD → DeckSide RECORD → DockSide STORE → MarketSide EXCHANGE
```

The stages are modular services, not four marketing panels. Each service accepts a typed input, evaluates named gates, appends an event or exception, produces only authorized projections, and emits a receipt.

The governing rule is:

> One evidence ledger. Two projections. Mandatory policy filter. No silent rewriting.

Public and private records are paired by shared metadata. They are never merged into one public object.

## 2. Rails

| Rail | Purpose | Permitted examples |
|---|---|---|
| `PUBLIC` | Approved, non-reconstructable public projection | scenario marker, generalized origin, status, band, count, public reason code |
| `COMPLIANCE` | Regulated evidence references and verification states | receiving reference, fish-ticket reference, lot linkage, audit status |
| `PRIVATE` | Exact operational and commercial evidence | exact location, weight, variance, tolerance, recovery, price, invoice, customer record |
| `SHARED_METADATA` | Pairing and verification without raw evidence | IDs, hashes, versions, counts, classifications, verdicts, timestamps |

Compliance does not mean public. Synthetic does not automatically mean safe.

## 3. Canonical terms

| Term | Canonical meaning |
|---|---|
| `#CATCH` | Mutable DeckSide public-safe estimate/record projection |
| `$CHECK` | Paired private DeckSide operational projection |
| `#HARVEST` | Accepted DockSide measured-confirmation event |
| `HARVEST_RAIL` | Compliance lineage of harvest, exception, correction, and supersession events |
| `$BOOK` | Private DockSide/MarketSide ledger projection |
| `PUBLIC_PROJECTION` | Allowlisted, non-reconstructable output created before the public renderer |
| `SHARED_METADATA_RECEIPT` | Hash/count/classification/verdict/timestamp handoff |

Deprecated alias: `$BOOKS` maps to `$BOOK`. It must not appear as an independent rail.

## 4. Service contracts

### Component A — SeaSide Origin Context

- Transition: `HOLD`
- Accepts: authorization context, generalized geography, trip window, vessel/gear/species categories.
- Private: exact position, vessel intelligence, identity, permit evidence not cleared for publication.
- Public: generalized origin context and evidence status.
- Stops when identity, authority, time, geography, or rail is unknown.

### Component B — DeckSide Catch Pairing

- Transition: `RECORD`
- Emits: mutable `#CATCH` and paired private `$CHECK`.
- An estimate is not a measurement.
- Revisions append and supersede; they do not erase earlier assertions.
- The public projection never contains exact operational values.

### Component C — DockSide Harvest Confirmation

- Transition: `STORE`
- Purpose: reconcile `#CATCH` lineage against accepted receiving/measurement evidence.
- Emits one of: `#HARVEST`, `HARVEST_EXCEPTION`, `HARVEST_CORRECTION`, or `HARVEST_SUPERSESSION`.
- Writes exact operational and commercial records only to `$BOOK`.
- A variance exception is still evidence and must be appended; it must not disappear because public release is blocked.

Component C invariants:

1. `#HARVEST` requires accepted measured evidence. Observation, assertion, or prediction is insufficient.
2. Every measurement and exception appends to `HARVEST_RAIL`.
3. Exact measurement, variance, tolerance, recovery, price, settlement, customer, and contract fields remain private.
4. Public output is limited to an approved status, band, count, reason code, or scenario marker.
5. Corrections include `prior_event_hash` and `supersedes_event_id`.
6. Public reverse replay stops at public/compliance lineage; it never opens `$BOOK`.

### Component D — MarketSide Proof Exchange

- Transition: `EXCHANGE`
- Consumes an approved public projection envelope, never a mixed private/public record.
- Produces buyer-safe continuity status, public lineage, and scenario-safe proof.
- Does not assert certification, endorsement, partnership, production status, or guaranteed compliance without separate authority.

## 5. Projection boundary

The public projection is allowlist-based and fail-closed.

A blocklist is defense in depth only. Unknown fields do not become public merely because their names are absent from a forbidden-term list.

The public renderer must never be the first place private fields are removed.

Required negative tests:

1. unknown-field rejection;
2. exact-value canary/no-echo;
3. reconstruction-group detection;
4. public bundle transitive scan;
5. exception-event preservation;
6. correction/supersession replay;
7. incomplete-lineage rejection;
8. missing-policy failure;
9. unsupported-claim rejection.

## 6. Forward and reverse flows

Forward:

```text
Origin context
→ mutable catch assertion
→ measured DockSide event or exception
→ approved product/public projection
```

Public reverse:

```text
MarketSide public proof
→ public projection receipt
→ shared-metadata lineage
→ DockSide public/compliance status
→ generalized DeckSide/SeaSide context
```

Private reverse traversal is a separate authorized operation. A public request must not traverse the private graph.

## 7. Harness correction requirements

Before this PR may be described as boundary-proven:

1. Remove exact weights, exact dates, first-receiver references, quantities, PO state, and source-document references from models and fixtures labeled public, or convert them into approved bands/statuses.
2. Move variance calculation and thresholds behind the private/compliance boundary.
3. Replace blocklist-only public projection with an explicit allowlist contract.
4. Replace Boolean companion claims with verified shared-metadata binding identifiers/hashes.
5. Add exception, correction, supersession, no-echo, reconstruction, and unknown-field tests.
6. Rename buyer/PO-specific public flow terminology to role-neutral terms unless publication authority is recorded.
7. Keep readiness distinct: `LOCAL_GREEN → GATE_GREEN → DOC_GREEN → GO_GREEN`.
8. Only the Owner can confer `GO_GREEN`.

## 8. Source-census rule

Files outside this repository, including OneDrive and local `C:\WSP001` materials, are source candidates only. Filename listings do not authorize content ingestion or publication.

Before use, record path, media type, size, hash, rail, access state, authority state, duplicate group, and supersession state. Default unknown commercial, customer, recovery, valuation, invoice, and operational materials to `PRIVATE / REVIEW_REQUIRED`.

## 9. Completion evidence

A conforming change returns:

- exact repository, branch, and commit SHA;
- changed-file list;
- named gate/test results;
- public/private/reconstruction finding counts;
- shared-metadata receipt hash;
- readiness state;
- explicit Owner decision.

No agent may manufacture Owner approval.
