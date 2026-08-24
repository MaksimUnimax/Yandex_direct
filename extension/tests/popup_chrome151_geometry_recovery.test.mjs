import fs from "node:fs";
import test from "node:test";
import assert from "node:assert/strict";

const css = fs.readFileSync(new URL("../src/popup.css", import.meta.url), "utf8");
const html = fs.readFileSync(new URL("../src/popup.html", import.meta.url), "utf8");

function compact(value) {
  return String(value).replace(/\s+/g, " ");
}

const normalized = compact(css);

test("action popup root is bounded below Chromium 600px autosize limit", () => {
  assert.match(normalized, /html, body \{[^}]*width: 430px;/);
  assert.match(normalized, /html, body \{[^}]*min-width: 430px;/);
  assert.match(normalized, /html, body \{[^}]*max-width: 430px;/);
  assert.match(normalized, /html, body \{[^}]*height: 560px;/);
  assert.match(normalized, /html, body \{[^}]*min-height: 560px;/);
  assert.match(normalized, /html, body \{[^}]*max-height: 560px;/);
  assert.match(normalized, /html, body \{[^}]*overflow: hidden;/);
});

test("long settings page scrolls inside fixed popup instead of growing action host", () => {
  assert.match(normalized, /main \{[^}]*height: 100%;/);
  assert.match(normalized, /main \{[^}]*overflow-x: hidden;/);
  assert.match(normalized, /main \{[^}]*overflow-y: auto;/);
  assert.ok((html.match(/<section>/g) || []).length >= 8, "fixture must remain a long popup that would exceed 600px without the root bound");
});

test("no viewport-relative root max-width remains in popup", () => {
  assert.doesNotMatch(normalized, /body \{[^}]*max-width: 100vw;/);
});
