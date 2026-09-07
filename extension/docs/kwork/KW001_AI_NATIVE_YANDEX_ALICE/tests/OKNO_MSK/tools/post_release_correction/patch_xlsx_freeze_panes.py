#!/usr/bin/env python3
"""Add the required frozen header row and first two columns to artifact-tool XLSX output.

Artifact-tool 2.8.6 accepts the documented freezePanes calls but the current
exporter omits the resulting pane nodes. This narrow OpenXML post-processing step
changes only worksheet view metadata; values, formulas, styles and tables remain
authored by artifact-tool.
"""

from __future__ import annotations

import argparse
import os
import re
import tempfile
import zipfile
from pathlib import Path


PANE_XML = (
    b'<x:pane xSplit="2" ySplit="1" topLeftCell="C2" '
    b'activePane="bottomRight" state="frozen" />'
    b'<x:selection pane="topRight" activeCell="C1" sqref="C1" />'
    b'<x:selection pane="bottomLeft" activeCell="A2" sqref="A2" />'
    b'<x:selection pane="bottomRight" activeCell="C2" sqref="C2" />'
)


def patch_sheet_xml(data: bytes, member: str) -> bytes:
    if b"<x:pane " in data:
        return data
    pattern = re.compile(rb"(<x:sheetView\b[^>]*)\s*/>")
    replacement = rb"\1>" + PANE_XML + b"</x:sheetView>"
    patched, count = pattern.subn(replacement, data, count=1)
    if count != 1:
        raise RuntimeError(f"Could not add frozen pane to {member}")
    return patched


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--xlsx", required=True)
    args = parser.parse_args()
    source = Path(args.xlsx).resolve()
    if not source.is_file():
        raise FileNotFoundError(source)

    descriptor, temporary_name = tempfile.mkstemp(prefix=f".{source.name}.", suffix=".tmp", dir=source.parent)
    os.close(descriptor)
    temporary = Path(temporary_name)
    try:
        with zipfile.ZipFile(source, "r") as incoming, zipfile.ZipFile(temporary, "w") as outgoing:
            worksheet_members = [name for name in incoming.namelist() if re.fullmatch(r"xl/worksheets/sheet\d+\.xml", name)]
            if len(worksheet_members) != 6:
                raise RuntimeError(f"Expected 6 worksheet XML files, found {len(worksheet_members)}")
            for info in incoming.infolist():
                payload = incoming.read(info.filename)
                if info.filename in worksheet_members:
                    payload = patch_sheet_xml(payload, info.filename)
                outgoing.writestr(info, payload)
        os.replace(temporary, source)
    finally:
        if temporary.exists():
            temporary.unlink()
    print(f"freeze panes patched: {source}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
