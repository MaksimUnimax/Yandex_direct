# tests/

Unified regression and acceptance-support test tree for Yandex Marketing Bridge.

Development rule:

- add one service at a time;
- preserve regression coverage for all previously accepted services;
- source tests do not replace exact packaged-extension tests;
- packaged tests do not replace controlled live Chrome + production ChatGPT acceptance.

Reference tests remain evidence under `extension/reference/`; new product tests belong here.
