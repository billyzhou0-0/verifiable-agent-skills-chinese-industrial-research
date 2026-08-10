# Chinese Industrial Research（中国工业行业调研）

**Verifiable research workflow for Chinese industrial and manufacturing industries — every data point back-to-source, no fabrication allowed.**

This skill encodes a research methodology proven on a 21-industry multi-worker pipeline (food processing, slaughter, cold chain, injection molding, PV modules, cement, and more). The deliverable is a **verifiable engineering knowledge pack**: equipment models and parameters, plant/building parameters, utility engineering data, and standard numbers — every one tied to a real Chinese source with a URL.

## What problem it solves

- AI research on Chinese industries produces **hallucinated model numbers, wrong standards, fabricated URLs** — because search-engine summaries lie and vendor sites rot.
- Knowledge packs get written from memory instead of from fetched pages, and nobody audits the citations.
- A 21-industry audit found: 590 URLs, 2,192 data points — the full-coverage round caught range-citation errors, wrong-page references, and one famous reversal (a value declared "absent from page" that was actually there, in a different number format).

## Golden rules

1. **Register URLs in the citation ledger at retrieval time** — never from memory after writing.
2. **Write-as-you-go**: research one industry to ~20-35 valid sources, write its file, THEN start the next industry. Never bank all research first (timeout risk).
3. **Never fabricate**: 型号/厂商/尺寸/URL 未检索到就写【待核实】(to be verified). Chinese search-engine summaries frequently mislead — open the original page to verify data points.
4. Source priority: openstd（国家标准全文公开系统）＞ industry standards (NY/T, SB/T) ＞ vendor official product pages ＞ authoritative industry sites ＞ everything else.

## Key channels (all curl-verified from mainland China)

### Chinese standard databases (three-tier lookup, always cross-check)
1. **openstd.samr.gov.cn** — national standard full-text system. Search `std_list?p.p2=<标准号或名称>`; list rows carry the 32-hex HCNO — a single curl pass extracts 标准号/名称/类型/状态/发布日/实施日. Rate-limit: sleep 5-6s between queries. A 0-row result page is itself citable evidence that a standard is NOT in openstd. Engineering-construction GBs (GB 50xxx) and some environmental GBs are NOT in openstd — cite the EIA report that references them instead.
2. **hbba.sacinfo.org.cn** — 全国标准信息公共服务平台. POST `stdQueryList` → JSON records. Good for NY/T, SB/T and confirming 现行/废止.
3. **down.foodmate.net** — 食品伙伴网标准库. gb2312 encoded; detail pages carry 发布/实施日期、颁发部门、**代替关系**、适用范围.
4. **Cross-check rule**: mandatory 食品安全国标 can be MISSING from openstd/hbba — locate via foodmate or 卫健委平台, mark 【待核实】 with that pathway. Standards get replaced — always record the replacement chain.

### Vendor equipment catalogs (the most valuable real data)
- Fetch `/sitemap.xml` first; batch-fetch product pages; strip HTML; extract param block between stable markers.
- **Spec-table-rich profile**: real L×W×H/kW/产能/重量 tables on product pages. When you find this profile, grab BOTH spec tables and program pages (engineering capacity ranges).
- **Marketing-only profile**: mine the technology/process pages, not just product pages — real numbers (吨电耗, 调质时间, 混合 CV) live in feature paragraphs.
- **JS-framework vendor sites** (every page shares one title): curl is useless — use a browser, click the params tab, extract text.
- **New extraction forms**: values hidden in `data-v="..."` HTML attributes (grep raw HTML before assuming JS-emptiness); "dimension-rich" pages with full-machine footprints; image-only spec PDFs → render to PNG + OCR.
- **Dead-domain discipline**: a domain transferred/for-sale still returns HTTP 200 — check page title/brand, never just the status code. 403/WAF is dynamic (retry with different UA/time), not permanent.
- **Vendor discovery when search engines are dead**: listed-company annual reports/prospectuses beat domain guessing (~0 hit rate). eastmoney F10 company survey JSON carries the company's contact email — the email domain is usually the current official site.

### Listed-company documents (招股书/募集说明书/年报)
- cninfo `fulltextSearch/full` POST → JSON with `adjunctUrl` → PDF. Prospectuses are the richest engineering source in one PDF: 房产证表 (building areas), 主要生产设备清单 (equipment + counts), 募投项目投资概算, process parameters in industry descriptions.
- PDF extraction: pymupdf. A+H dual-listed companies return the H-share TRADITIONAL-CHINESE annual report — grep with BOTH simplified and traditional keywords (产能 misses 產能).

### Official environmental platforms (排污许可/环评 — 公用工程/环保 data)
- permit.mee.gov.cn — no captcha with curl + UA; license info + emission standards per plant.
- EIA full reports (the richest source of building params: 占地/建筑面积/净高/柱网) live at provincial 受理公示 pages with full-report PDF direct links (`downfile.jsp?filename=<md5>.pdf`) — 551-page EIA reports downloadable via plain curl.
- 行政审批局 (not just 生态环境厅) 环评公示 pages often attach the FULL 环评报告表 as PDF — one 115-page report yielded 92 equipment rows + 防爆区 + building areas.

### Search engines: don't waste time (as of 2026-08)
Most curl-able search engines are captcha/WAF-blocked or geo-polluted from mainland China. **360 搜索 (www.so.com/s?q=...) IS curl-able** and is the one reliable Chinese discovery channel: result blocks carry `data-mdurl="<真实URL>"` on the `<h3><a>` — extract that attribute to bypass the JS redirect. Result snippets often already contain the key numbers. Workaround for everything else: skip search engines; go direct — standards databases, vendor sitemap.xml, B2B platforms, exchange announcement APIs.

## Audit methodology (the part that makes it "verifiable")

The pipeline's LAST stage audits every knowledge pack for data authenticity:

1. **Programmatic full-text scan** of every pack: Sources numbering continuity, undefined prose refs, coverage, `[unverified]` residue, mixed `[数字+汉字]` citations, 【待核实】counts, table rows. Round result: 21/21 packs had 100% ref integrity.
2. **Sampled source verification** (≥5 URLs/pack): parallel curl with UA + `-L` + `--compressed`; classify failures — dynamic (403/WAF: retry) vs permanent (domain transfer: check title, not status code).
3. **Value verification** (2-3 key numbers/pack): HTML → grep context from stripped text; PDFs → pymupdf + regex. **URL 200 ≠ claim supported** — verify content presence, and **verify BOTH formatting variants before declaring absence** (a value "absent" was found after normalizing thousands separators and entity-encoded dashes).
4. **Standard-number verification**: foodmate detail page title carries the standard name — decode gb2312 and title-match.
5. **Full-coverage round (when the user rejects sampling — "每项都查，不是抽查")**: run EVERYTHING — all URLs (batch curl with 3 passes + content-check), all values (fetch every unique URL once, match with format variants: thousands separators, ×/x/–/~/−, 万/亿 scaling, 吨↔万吨, kN↔吨, inch↔mm). **404 ≠ dead**: probe site root + sitemap before classifying. **False-negative traps**: PDF table cells concatenate digits; JS tables hide values in `data-v` attributes (re-grep RAW HTML); never conclude "value absent" from one search form.

## Acceptance lines (tiered, quality-first)

- **A 类 (pipeline industries with rich vendor sites)**: 25-45 KB, sources ≥30, data points ≥60, building-parameter table ≥10 rows.
- **B 类 (vendor-sparse industries)**: sources ≥15, data points ≥60, building params ≥10 rows, ≥15 KB, PLUS the honest-declaration triad — ① header notes which channels failed, ② ≥5 concrete fill-gap pathways, ③ register for the reinforcement round. **分级线不是偷懒线**: data points/column completeness/fill-gap pathways are not exempted.

## User governance requirements (hard rules for this class of work)

1. **Audits must be full-coverage, not sampling** — a sampled audit that found "all reachable" was later shown wrong.
2. **Judge quality before speed** when evaluating which recommendations worked.
3. **Reinforcement rounds only ADD information, never delete** (unless an audit proves an error) — V01→V02 upgrades must pass a diff audit proving zero sourced data rows deleted.
4. **Skill/methodology files are created only after consulting the user** — subagents once created skills autonomously; the ruling was: keep them, but no further formalization without discussion.

## Reinforcement round (补强轮)

The audit report's fix instructions ARE the task list (graded with 文件/位置/问题/修复指令); each pack gets a reinforcement agent. Workflow: ① read registry + guide + audit; ② copy V01 → V02 and patch in place (V01 stays untouched); ③ fix per audit item, register "问题编号 → 修复动作"; ④ re-fetch cited URLs whenever the audit's own assumption looks off — **page titles settle double-use disputes, check BOTH sides before changing either**. Only 添加/移动 allowed, never delete sourced data. **Coverage repair without fabricating** has three proven patterns: ① appendix lines append "编号 [1] 至 [N]"; ② 编制说明 lines carry already-named channel numbers; ③ fill-gap entries only get [n] when the subject already has a Sources number — never bolt fabricated citations onto pathway descriptions.

## Files

- `SKILL.md` — the full methodology (Chinese).
- `scripts/audit_doc_scan.py` — stdlib citation-integrity scanner (Sources numbering, undefined refs, unverified residue, range-citation detection).
- `scripts/cn_std_search.py` — one-shot search across openstd + hbba + foodmate.
- `scripts/openstd_std_list.py` — bulk openstd keyword search with rate-limit sleep.
- `scripts/s360_search.py` — 360 search with real-URL extraction.
- `scripts/spec_table_extract.py` — fetch a page and print all table rows + key-value parameter lines.
- `LICENSE` — MIT.

## Related

Companion skill: `grounded-citations` (citation ledger discipline — its sources.py ledger must be used for all citation numbering; this skill covers where and how to fetch Chinese sources). Hub: [verifiable-agent-skills](../verifiable-agent-skills).
