from __future__ import annotations

import argparse


def owner_go_granted(token: str | None) -> bool:
    return token == "OWNER-GO"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--token", default=None)
    args = parser.parse_args()
    if owner_go_granted(args.token):
        print("OWNER_GO_GATE_PASS")
        return 0
    print("OWNER_GO_GATE_BLOCKED")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
