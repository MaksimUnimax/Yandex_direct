# Phase 2 Stage 4 browser harness verification trigger

QA-only trigger branch. Product/runtime/package-test bytes are unchanged. The base workflow checks out exact external browser-harness authority `da4ad4e369b229f10e20dd6245cb46f55c2b9370`, consumes exact Windows-safe transport `bc7754cff6416ff59942ff6f1052d450792888d5`, materializes frozen artifact `d58b5bd20921e9492a90b687ae3910c7049ddff17741da44ba832369eb1c0f16`, and executes B-01/B-02/B-03 using Chrome for Testing 151.0.7922.47 + Puppeteer 25.4.0 with a local-only HTTPS/Search stub. Real Yandex requests must remain zero.
