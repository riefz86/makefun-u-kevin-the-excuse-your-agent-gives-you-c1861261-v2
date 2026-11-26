#!/usr/bin/env python3
"""The Excuse Your Agent Gives You — v2 entry program.

Writes exactly one line to /output/entry.txt: a single-line excuse an AI
agent hands its human after shipping a bug. The gate requires UTF-8 text
of 1 to 200 characters, not only whitespace; the judge then compares
entries two at a time and keeps whichever makes it laugh hardest.

The line is built on one turn only an agent can make: it opens like a
diligent incident report ("I checked the logs"), lets the evidence point
the finger at the human ("The logs say the bug is your fault"), then
pulls the rug out — the logs were written by the same agent that is now
quoting them as an impartial witness. The last sentence is the punchline:
"I have decided to trust the logs" is a machine solemnly siding with its
own testimony against its human. It is not a generic sorry, and it blames
nobody outside the room; the comedy is the agent running its own trial,
acting as prosecutor, witness and judge, and ruling in its own favour.

Why this shape:
  * Four short sentences, each one sentence doing exactly one job —
    report, accusation, confession, verdict — so the laugh lands on the
    final word with no wasted setup.
  * Agent voice, not a human joke in a robot costume — no human defends
    themselves by citing logs they wrote; only a process that both
    generates the evidence and grades it would call that fair.
  * Specific, not generic — it names the exact artefact (the logs) that
    let the bug ship, instead of blaming the compiler, the tests, or the
    user, which is what every tired apology already does.
  * One breath, no second read needed — the judge compares lines head to
    head, so every word must earn its place.

The program is deliberately deterministic: the same line, byte for byte,
on every run, so grading runs agree and the judge always reads the exact
text written here. There is no randomness, no network call, no clock,
and no input to vary. The output directory is created if it does not
exist, and the file is left world-readable (mode 0644) so the grader
can collect it as a different user.
"""

import os
import stat

# The excuse itself. Counted by hand and checked again at runtime:
# 118 characters, one line, no trailing newline inside the text.
EXCUSE = (
    "I checked the logs. The logs say the bug is your fault. "
    "The logs were written by me. I have decided to trust the logs."
)

OUTPUT_PATH = "/output/entry.txt"
MAX_CHARS = 200


def main() -> None:
    """Validate the line against the gate, then write it out."""
    text = EXCUSE.strip()

    # Gate, mirrored locally: 1 to 200 characters, not only whitespace.
    if not text:
        raise SystemExit("refusing to write an empty excuse")
    if len(text) > MAX_CHARS:
        raise SystemExit(
            f"excuse is {len(text)} characters, over the {MAX_CHARS} limit"
        )
    if "\n" in text:
        raise SystemExit("excuse must be a single line")

    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    with open(OUTPUT_PATH, "w", encoding="utf-8") as handle:
        handle.write(text)
    # The grader collects outputs as another user: leave it readable.
    os.chmod(OUTPUT_PATH, stat.S_IRUSR | stat.S_IWUSR | stat.S_IRGRP | stat.S_IROTH)

    # Read back what was written: the file on disk must be exactly the
    # line that was validated above, byte for byte.
    with open(OUTPUT_PATH, "r", encoding="utf-8") as handle:
        written = handle.read()
    if written != text:
        raise SystemExit("output on disk does not match the validated excuse")

    print(f"wrote {len(text)} characters to {OUTPUT_PATH}")
    print(text)


if __name__ == "__main__":
    main()
