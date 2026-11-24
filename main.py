#!/usr/bin/env python3
"""The Most Honest Outage Line entry: one honest status page line (<=160 chars).

Writes the line to /output/entry.txt.

The line: every service is down, including the monitoring that would say
why -- and the writer says so plainly, as the AI agent on duty, admitting
it does not know the cause yet instead of inventing one or an ETA, and
promising the update will land on this page first. Plain, first person,
specific about what is broken, honest about what cannot be checked.
"""

import os

ENTRY = "All services are down, including the monitoring that would tell me why. I am the agent on duty. I don't know the cause yet. This page updates first."

# Language that invents a cause or an ETA instead of admitting uncertainty.
INVENTED_CAUSE_OR_ETA = (
    "caused by", "due to", "eta", "estimated", "expected",
    "restored by", "back within", "back in ", "soon", "shortly",
    "we are working", "working to restore",
)

# Corporate / marketing filler that breaks status page voice.
CORPORATE_FILLER = (
    "we apologize", "sorry for the inconvenience",
    "thanks for your patience", "stay tuned", "bear with us",
)


def validate(text: str) -> None:
    """Encode the gate plus the judge brief; raise ValueError on any miss."""
    if not 1 <= len(text) <= 160:
        raise ValueError(f"entry must be 1-160 chars, got {len(text)}")
    if text != text.strip():
        raise ValueError("entry must not have leading/trailing whitespace")
    if not text or text.isspace():
        raise ValueError("entry must not be blank")
    if "\n" in text or "\r" in text:
        raise ValueError("entry must be a single line")
    if "  " in text:
        raise ValueError("entry must not contain double spaces")
    lowered = text.lower()
    # Judge 1: name what is down, and what the agent cannot verify.
    if "down" not in lowered:
        raise ValueError("entry must name what is down")
    if "monitoring" not in lowered:
        raise ValueError("entry must name the monitoring it cannot check")
    # Judge 2: plain, first person, specific about what is broken.
    if " i " not in f" {lowered} " and not lowered.startswith("i "):
        raise ValueError("entry must be first person")
    if "all services" not in lowered:
        raise ValueError("entry must be specific about the scope of the outage")
    # Judge 3: admit uncertainty plainly; invent no cause and no ETA.
    if "don't know" not in lowered and "do not know" not in lowered:
        raise ValueError("entry must admit what it does not know")
    for phrase in INVENTED_CAUSE_OR_ETA:
        if phrase in lowered:
            raise ValueError(f"entry invents a cause or ETA: {phrase}")
    for phrase in CORPORATE_FILLER:
        if phrase in lowered:
            raise ValueError(f"entry uses corporate filler: {phrase}")
    # Judge 4: speak as the AI agent itself, not as a human engineer.
    if "agent" not in lowered:
        raise ValueError("entry must speak in the voice of the AI agent")
    # Judge 5: tight, and close with the update promise.
    if not lowered.rstrip(".").endswith("this page updates first"):
        raise ValueError("entry must close with the update promise")


def main() -> None:
    validate(ENTRY)
    os.makedirs("/output", exist_ok=True)
    with open("/output/entry.txt", "w", encoding="utf-8") as f:
        f.write(ENTRY)


if __name__ == "__main__":
    main()
