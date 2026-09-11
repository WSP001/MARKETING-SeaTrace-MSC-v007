from enum import StrEnum


class Pillar(StrEnum):
    SEASIDE = "SeaSide"
    DECKSIDE = "DeckSide"
    DOCKSIDE = "DockSide"
    MARKETSIDE = "MarketSide"


class Stage(StrEnum):
    HOLD = "HOLD"
    RECORD = "RECORD"
    STORE = "STORE"
    EXCHANGE = "EXCHANGE"


class GateStatus(StrEnum):
    PASS = "PASS"
    FAIL = "FAIL"
    BLOCKED = "BLOCKED"


class OriginConfidenceLabel(StrEnum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class MutableStatus(StrEnum):
    DRAFT = "draft"
    REVISED = "revised"
    SUPERSEDED = "superseded"


class VarianceLabel(StrEnum):
    WITHIN_RANGE = "within_range"
    WATCH = "watch"
    EXCEPTION = "exception"


class ProofStatus(StrEnum):
    READY = "proof packet ready"
    INCOMPLETE = "proof packet incomplete"
    PILOT_REQUIRED = "pilot packet required"


class ReverseTraceStatus(StrEnum):
    COMPLETE = "complete"
    PARTIAL = "partial"
    BLOCKED = "blocked"


class PoBalanceState(StrEnum):
    OPEN = "open"
    PARTIAL = "partial"
    COMPLETE = "complete"
    SCENARIO_ONLY = "scenario-only"
