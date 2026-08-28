(() => {
  "use strict";

  function canonicalDomain(value) {
    return String(value ?? "").trim().toLowerCase().replace(/\.$/u, "");
  }

  function boundedInt(value, { min, max, fallback }) {
    const number = Number(value);
    return Number.isSafeInteger(number) && number >= min && number <= max ? number : fallback;
  }

  function normalizedResult(item) {
    const payload = item?.result_payload;
    if (!payload || typeof payload !== "object" || Array.isArray(payload)) return null;
    if (payload.result && typeof payload.result === "object" && !Array.isArray(payload.result)) return payload.result;
    if (payload.provider_result?.result && typeof payload.provider_result.result === "object") return payload.provider_result.result;
    if (payload.report_envelope?.result && typeof payload.report_envelope.result === "object") return payload.report_envelope.result;
    return null;
  }

  function rankedRows(item, topN = 100) {
    const result = normalizedResult(item);
    const source = Array.isArray(result?.results) ? result.results : [];
    const limit = boundedInt(topN, { min: 1, max: 100, fallback: 10 });
    const rows = source.map((row, index) => {
      const observedRank = Number(row?.rank);
      const rank = Number.isSafeInteger(observedRank) && observedRank > 0 ? observedRank : index + 1;
      return Object.freeze({
        rank,
        url: String(row?.url ?? ""),
        domain: canonicalDomain(row?.domain),
        title: String(row?.title ?? "")
      });
    }).filter((row) => row.rank <= limit).sort((a, b) => a.rank - b.rank);
    return Object.freeze(rows);
  }

  function uniqueDomains(rows) {
    const seen = new Set();
    const domains = [];
    for (const row of rows) {
      const domain = canonicalDomain(row?.domain);
      if (!domain || seen.has(domain)) continue;
      seen.add(domain);
      domains.push(domain);
    }
    return Object.freeze(domains);
  }

  function projectItem(item, { topN = 10, targetDomains = [] } = {}) {
    const rows = rankedRows(item, topN);
    const domains = uniqueDomains(rows);
    const targets = (Array.isArray(targetDomains) ? targetDomains : []).map((raw) => {
      const domain = canonicalDomain(raw);
      const matches = rows.filter((row) => canonicalDomain(row.domain) === domain);
      const best = matches.length ? Math.min(...matches.map((row) => row.rank)) : null;
      return Object.freeze({
        domain,
        best_rank_within_observed_topN: best,
        matching_urls: Object.freeze(matches.map((row) => row.url).filter(Boolean))
      });
    });
    const result = normalizedResult(item);
    return Object.freeze({
      item_id: String(item?.item_id || ""),
      query_text: String(item?.command?.queryText || ""),
      region: item?.command?.region == null ? null : String(item.command.region),
      search_type: String(item?.command?.searchType || ""),
      requested_groups: Number(item?.command?.groupsOnPage || 0),
      observed_result_count: Number(result?.result_count ?? (Array.isArray(result?.results) ? result.results.length : 0)),
      ranked_results: rows,
      top_domains: domains,
      target_domains: Object.freeze(targets)
    });
  }

  function successfulItems(job) {
    return (Array.isArray(job?.items) ? job.items : []).filter((item) => String(item?.status || "") === "SUCCEEDED" && normalizedResult(item));
  }

  function projectPage(job, options = {}) {
    const items = successfulItems(job);
    const offset = boundedInt(options.offset, { min: 0, max: 1_000_000, fallback: 0 });
    const limit = boundedInt(options.limit, { min: 1, max: 100, fallback: 20 });
    const topN = boundedInt(options.topN, { min: 1, max: 100, fallback: 10 });
    const selected = items.slice(offset, offset + limit).map((item) => projectItem(item, { topN, targetDomains: options.targetDomains || [] }));
    return Object.freeze({
      job_id: String(job?.job_id || ""),
      total_successful: items.length,
      offset,
      limit,
      topN,
      next_offset: offset + selected.length < items.length ? offset + selected.length : null,
      items: Object.freeze(selected)
    });
  }

  function overlapRecord(leftItem, rightItem, topN) {
    const left = projectItem(leftItem, { topN });
    const right = projectItem(rightItem, { topN });
    const rightSet = new Set(right.top_domains);
    const shared = left.top_domains.filter((domain) => rightSet.has(domain));
    const union = new Set([...left.top_domains, ...right.top_domains]);
    const sharedCount = shared.length;
    const leftCount = left.top_domains.length;
    const rightCount = right.top_domains.length;
    const unionCount = union.size;
    return Object.freeze({
      left_item_id: left.item_id,
      left_query: left.query_text,
      right_item_id: right.item_id,
      right_query: right.query_text,
      left_domain_count: leftCount,
      right_domain_count: rightCount,
      shared_domains: Object.freeze([...shared]),
      shared_count: sharedCount,
      union_count: unionCount,
      jaccard: unionCount ? sharedCount / unionCount : 0,
      left_containment: leftCount ? sharedCount / leftCount : 0,
      right_containment: rightCount ? sharedCount / rightCount : 0
    });
  }

  function overlapPage(job, options = {}) {
    const items = successfulItems(job);
    const topN = boundedInt(options.topN, { min: 1, max: 100, fallback: 10 });
    const offset = boundedInt(options.offset, { min: 0, max: 10_000_000, fallback: 0 });
    const limit = boundedInt(options.limit, { min: 1, max: 1000, fallback: 100 });
    const totalPairs = items.length > 1 ? (items.length * (items.length - 1)) / 2 : 0;
    const out = [];
    let pairIndex = 0;
    const stopAt = offset + limit;
    outer: for (let left = 0; left < items.length; left += 1) {
      for (let right = left + 1; right < items.length; right += 1) {
        if (pairIndex >= offset && pairIndex < stopAt) out.push(overlapRecord(items[left], items[right], topN));
        pairIndex += 1;
        if (pairIndex >= stopAt) break outer;
      }
    }
    return Object.freeze({
      job_id: String(job?.job_id || ""),
      total_successful: items.length,
      total_pairs: totalPairs,
      offset,
      limit,
      topN,
      next_offset: offset + out.length < totalPairs ? offset + out.length : null,
      items: Object.freeze(out)
    });
  }

  globalThis.YMBSearchBatchProjection = Object.freeze({
    canonicalDomain,
    rankedRows,
    uniqueDomains,
    projectItem,
    projectPage,
    overlapPage
  });
})();