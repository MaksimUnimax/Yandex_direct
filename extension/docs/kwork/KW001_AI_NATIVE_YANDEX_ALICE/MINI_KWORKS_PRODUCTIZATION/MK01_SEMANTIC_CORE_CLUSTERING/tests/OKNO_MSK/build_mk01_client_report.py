#!/usr/bin/env python3
"""Compatibility entrypoint for MK01 client report generation.

The 2026-09-09 generator that produced a numerically correct but analytically weak
execution-protocol-style PDF is retired under failure classes E38/E39.

All new generation goes through build_mk01_client_report_v2.py, whose preflight
requires an evidence-backed executive summary, demand/task structure, material
semantic groups and review/exclusion analysis. Page count is not a quality gate.
"""

from build_mk01_client_report_v2 import main


if __name__ == "__main__":
    main()
