# Chinese Industrial Research（中国工业行业调研）

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![GitHub stars](https://img.shields.io/github/stars/billyzhou0-0/verifiable-agent-skills-chinese-industrial-research.svg)](https://github.com/billyzhou0-0/verifiable-agent-skills-chinese-industrial-research/stargazers)

**Verifiable research workflow for Chinese industrial and manufacturing industries — every data point back-to-source, no fabrication allowed.**
**可验证的中国工业/制造业调研工作流——每个数据点都能回源，绝不允许编造。**

This skill encodes a research methodology proven on a 30+ industry multi-worker pipeline (food processing, slaughter, cold chain, injection molding, PV modules, cement, and more). The deliverable is a **verifiable engineering knowledge pack**: equipment models and parameters, plant/building parameters, utility engineering data, and standard numbers — every one tied to a real Chinese source with a URL.
本技能总结了一套在 30+ 行业多 Worker 流水线上验证过的调研方法论（食品加工、屠宰、冷库冷链、注塑、光伏组件、水泥等）。产出是**可验证的工程知识包**：设备型号与参数、厂房/建筑参数、公用工程数据、标准编号——每一条都挂着一个真实的中国来源 URL。

## Why this exists（为什么做这个）

Chinese industry data is where AI hallucination goes to hide: search engines are captcha-walled, vendor domains rot silently (transferred domains still return HTTP 200), standards are scattered across four databases, and AI agents confidently invent model numbers and URLs.
中国行业数据是 AI 幻觉的藏身处：搜索引擎全被验证码挡住，厂商域名悄悄腐烂（转让出去的域名仍然返回 HTTP 200），标准散落在四个数据库里，而 AI 会自信地编造型号和网址。

Full-coverage audits of **5,000+ URLs and 20,000+ data points** across a 30+ industry pipeline caught fabricated citations, wrong-page references, and mis-attributed numbers. This workflow is the result: every number back-to-source, every unverifiable item honestly marked 【待核实】(to be verified), and an audit stage that treats every claim as guilty until proven.
30+ 行业流水线的**全量审计（5,000+ 个 URL、20,000+ 个数据点）**抓出了编造的引用、错页引用、张冠李戴的数字。本工作流就是那次审计的产物：每个数字回源、每个查不到的都诚实标注【待核实】、审计阶段把每条声称当"有罪推定"直到证明为真。

## Golden rules（金规则）

1. **Register URLs in the citation ledger at retrieval time** — never from memory after writing. / **抓取时立即登记 URL 到引用台账**——绝不事后凭记忆登记。
2. **Write-as-you-go** — research one industry to ~20-35 valid sources, write its file, THEN start the next industry. Never bank all research first. / **边研边写**——研究完一个行业（约 20-35 个有效来源）就写它的文件，再开始下一个行业。绝不把所有研究攒完再写。
3. **Never fabricate** — model numbers, vendors, dimensions, URLs not found are marked 【待核实】(to be verified). Chinese search-engine summaries frequently mislead — open the original page to verify data points. / **绝不编造**——型号/厂商/尺寸/URL 未检索到就写【待核实】。中文搜索引擎摘要经常误导，数据点优先打开原文核实。
4. Source priority: openstd（国家标准全文公开系统）＞ industry standards (NY/T, SB/T) ＞ vendor official product pages ＞ authoritative industry sites ＞ everything else. / 来源优先级：国家标准全文公开系统 ＞ 行业标准 ＞ 厂商官网产品页 ＞ 权威行业网站 ＞ 其他。

## Key channels（关键渠道，中国大陆网络实测）

### Chinese standard databases（标准库——三层检索，必须交叉验证）
1. **openstd.samr.gov.cn** — national standard full-text system. Search `std_list?p.p2=<标准号或名称>`; list rows carry the 32-hex HCNO — a single curl pass extracts 标准号/名称/类型/状态/发布日/实施日. Rate-limit: sleep 5-6s between queries. A 0-row result page is itself citable evidence that a standard is NOT in openstd. Engineering-construction GBs (GB 50xxx) are NOT in openstd — cite the EIA report that references them instead.
   国家标准全文公开系统。`std_list?p.p2=<标准号或名称>` 列表行内嵌 32 位 HCNO——一次 curl 即可提取全部字段。限速：查询间隔 sleep 5-6 秒。**0 行结果页本身是可引用证据**。工程建设类 GB（50xxx）不在 openstd——改引引用它们的环评报告。
2. **hbba.sacinfo.org.cn** — 全国标准信息公共服务平台. POST `stdQueryList` → JSON records. Good for NY/T, SB/T and confirming 现行/废止. POST `stdQueryList` → JSON 记录。适合 NY/T、SB/T 和确认现行/废止。
3. **down.foodmate.net** — 食品伙伴网标准库. gb2312 encoded; detail pages carry 发布/实施日期、颁发部门、**代替关系**、适用范围. gb2312 编码；详情页含发布/实施日期、颁发部门、代替关系、适用范围。

### Vendor equipment catalogs（厂商官网——真实数据最丰富的地方）
- Fetch `/sitemap.xml` first; batch-fetch product pages; strip HTML; extract param block between stable markers. / 先抓 `/sitemap.xml`；批量抓产品页；剥离 HTML；在稳定标记之间提取参数块。
- **Spec-table-rich profile** — real L×W×H/kW/产能/重量 tables on product pages. When you find this profile, grab BOTH spec tables and program pages (engineering capacity ranges). / **规格表型厂商（数据最全）**——产品页有真实尺寸/功率/产能/重量表格。遇到这种档案，规格表和技术/工程页（产能范围）都抓。
- **Marketing-only profile** — mine the technology/process pages, not just product pages — real numbers (吨电耗, 调质时间, 混合 CV) live in feature paragraphs. / **营销文型厂商**——挖技术/工艺页面而非产品页，真实数字藏在特性段落里。
- **JS-framework vendor sites** (every page shares one title) — curl is useless; use a browser, click the params tab, extract text. / **JS 框架官网**（所有页面同一标题）——curl 无效，用浏览器点参数页签提取。
- **New extraction forms** — values hidden in `data-v="..."` HTML attributes (grep raw HTML before assuming JS-emptiness); "dimension-rich" pages with full-machine footprints; image-only spec PDFs → render to PNG + OCR. / **新提取形态**——值藏在 `data-v` 属性里的表格（断言空页前先 grep 原始 HTML）；"尺寸最全"的页面；图片型选型 PDF → 渲染 PNG + OCR。
- **Dead-domain discipline** — a domain transferred/for-sale still returns HTTP 200; check page title/brand, never just the status code. 403/WAF is dynamic (retry with different UA/time), not permanent. / **失效分级纪律**——域名转让/出售的站仍返回 200，必须查页面标题/品牌；403/WAF 是动态失效（换 UA/时段重试），不是永久。

### Listed-company documents（上市公司文档——招股书/年报）
- cninfo `fulltextSearch/full` POST → JSON with `adjunctUrl` → PDF. Prospectuses are the richest engineering source in one PDF: 房产证表 (building areas), 主要生产设备清单 (equipment + counts), 募投项目投资概算, process parameters in industry descriptions. / cninfo 检索接口 → PDF。**招股书是单个 PDF 里最丰富的工程来源**：房产证表（建筑面积）、主要生产设备清单、募投项目概算、工艺参数。
- A+H dual-listed companies return the H-share TRADITIONAL-CHINESE annual report — grep with BOTH simplified and traditional keywords (产能 misses 產能). / A+H 两地上市返回 H 股**繁体**年报——必须简繁关键词都 grep（`产能` 搜不到 `產能`）。

### Official environmental platforms（官方环保平台——公用工程/建筑参数）
- permit.mee.gov.cn — no captcha with curl + UA; license info + emission standards per plant. / 全国排污许可平台——curl 无验证码；排污许可信息含排放执行标准。
- EIA full reports (the richest source of building params: 占地/建筑面积/净高/柱网) live at provincial 受理公示 pages with full-report PDF direct links — hundreds-of-pages EIA reports downloadable via plain curl. Note: 批复 pages show only a title; 受理公示 pages carry the full report. / 环评报告书全本（建筑参数最丰富：占地/建筑面积/净高/柱网）在**省级受理公示**页附全本 PDF 直链——纯 curl 可下数百页全本。注意：批复页只有标题，受理公示页才有全本。

### Search engines: don't waste time（搜索引擎：别浪费时间）
Most curl-able search engines are captcha/WAF-blocked from mainland China. **360 搜索 is curl-able** and is the one reliable Chinese discovery channel: result blocks carry `data-mdurl="<真实URL>"` — extract that attribute to bypass the JS redirect. Result snippets often already contain the key numbers. For everything else: skip search engines, go direct — standards databases, vendor sitemaps, B2B platforms, exchange announcement APIs.
中国大陆环境大部分搜索引擎被验证码/WAF 挡住。**360 搜索可 curl** 且是唯一可靠中文发现通道：结果块带 `data-mdurl` 真实 URL 属性，绕过 JS 跳转；摘要常已含关键数字。其余情况跳过搜索引擎直连：标准库、厂商 sitemap、B2B 平台、交易所公告 API。

## Audit methodology（审计方法论——"可验证"的核心）

The pipeline's LAST stage audits every knowledge pack for data authenticity:
流水线最后阶段审计每个知识包的数据真实性（只读，不改包）：

1. **Programmatic full-text scan / 程序化全文本扫描** — Sources numbering continuity, undefined refs, coverage, `[unverified]` residue, mixed citations, table rows. Round result: 30/30 packs had 100% ref integrity. Sources 编号连续性、未定义引用、覆盖率、残留标记、表格行数。实测 30/30 包引用完整性 100%。
2. **Sampled source verification / 抽样源验证**（≥5 URLs/pack）— parallel curl; classify failures: dynamic (403/WAF: retry) vs permanent (domain transfer: check title, not status code). 并行 curl；失败分类：动态（重试）vs 永久（查标题，不看状态码）。
3. **Value verification / 数值验证**（2-3 key numbers/pack）— HTML grep; PDF pymupdf + regex. **URL 200 ≠ claim supported** — verify content presence, and **check BOTH formatting variants before declaring absence** (a "missing" value was found after normalizing thousands separators and entity-encoded dashes). HTML 剥文本 grep；PDF pymupdf+正则。**URL 200 ≠ 数据被支持**；声明"页面无此值"前必须验证两种格式变体（曾有一次"缺失"判定被推翻：千分位+实体破折号导致漏检）。
4. **Full-coverage round / 全量轮**（when the user rejects sampling — "每项都查，不是抽查"）— run EVERYTHING: all URLs (batch curl with 3 passes + content-check), all values (fetch each unique URL once, match with format variants: thousands separators, ×/x/–/~/−, 万/亿 scaling, 吨↔万吨, kN↔吨, inch↔mm). **404 ≠ dead**: probe site root + sitemap before classifying. **False-negative traps**: PDF table cells concatenate digits; JS tables hide values in `data-v` attributes (re-grep RAW HTML); never conclude "value absent" from one search form.
   当用户拒绝抽样（"我需要的不是抽查，而是每项都查"）时全部跑：URL 全量（批量 curl 3 轮+内容检查）、数值全量（每 URL 抓一次，按格式变体匹配：千分位、×/x/–/~/−、万/亿、吨↔万吨、kN↔吨、inch↔mm）。**404 ≠ 死链**（先探站根+sitemap）；假阴性陷阱：PDF 单元格拼数字、JS 表格值藏 data-v 属性（重 grep 原始 HTML）、绝不在一种搜索形式后断定"值不存在"。

## Acceptance lines（验收线——分级，质量优先）

- **A 类 (pipeline industries with rich vendor sites / 流水线型设备密集型行业)** — 25-45 KB, sources ≥30, data points ≥60, building-parameter table ≥10 rows. 25~45 KB，来源 ≥30，数据点 ≥60，建图参数表 ≥10 行。
- **B 类 (vendor-sparse industries / 厂商官网稀少型行业)** — sources ≥15, data points ≥60, building params ≥10 rows, ≥15 KB, PLUS the honest-declaration triad: ① header notes which channels failed ② ≥5 concrete fill-gap pathways ③ registered for the reinforcement round. **The tier line is not a laziness line** — data points and fill-gap pathways are never exempted.
  来源 ≥15，数据点 ≥60，建图参数 ≥10 行，≥15 KB，外加诚实声明三件套：① 头部写明失败通道 ② 补齐途径 ≥5 项且具体 ③ 列入补强名单。**分级线不是偷懒线**——数据点/补齐途径不豁免。

## Reinforcement round（补强轮）

The audit report's fix instructions ARE the task list (graded with 文件/位置/问题/修复指令); each pack gets a reinforcement agent. Workflow: ① copy V01 → V02 and patch in place (V01 stays untouched) ② fix per audit item, register "问题编号 → 修复动作" ③ re-fetch cited URLs whenever the audit's own assumption looks off — **page titles settle double-use disputes, check BOTH sides before changing either**. Only 添加/移动 allowed, never delete sourced data. **Coverage repair without fabricating** has three proven patterns: appendix lines append "编号 [1] 至 [N]"; 编制说明 lines carry already-named channel numbers; fill-gap entries only get [n] when the subject already has a Sources number.
审计报告的修复指令就是任务清单（分级 + 文件/位置/问题/修复指令）；每包一个补强 Agent。工作流：① 复制 V01 → V02 原地修补（V01 不动）② 按审计项修复并登记 ③ 审计自身假设可疑时重抓被引 URL——**页面标题裁决双占用争议，改任何一侧前两边都查**。只允许添加/移动，绝不删除有来源数据。**覆盖率修复零编造三模式**：附录行挂"编号 [1] 至 [N]"；编制说明行挂已点名的通道编号；条目只在主语已有 Sources 编号时才补 [n]。

## Files（文件）

- `SKILL.md` — the full methodology（完整方法论，中文）.
- `scripts/audit_doc_scan.py` — stdlib citation-integrity scanner（引用完整性扫描器）.
- `scripts/cn_std_search.py` — one-shot search across openstd + hbba + foodmate（三库一次检索）.
- `scripts/openstd_std_list.py` — bulk openstd keyword search with rate-limit sleep（openstd 批量检索）.
- `scripts/s360_search.py` — 360 search with real-URL extraction（360 搜索+真实 URL 提取）.
- `scripts/spec_table_extract.py` — fetch a page and print all table rows + key-value parameter lines（抓页并打印表格行+参数行）.
- `LICENSE` — MIT.

## Related（相关）

Companion skill: `grounded-citations` (citation ledger discipline — its sources.py ledger must be used for all citation numbering; this skill covers where and how to fetch Chinese sources). Hub: [verifiable-agent-skills](../verifiable-agent-skills).
配套技能：`grounded-citations`（引用台账纪律——sources.py 台账必须用于全部引用编号；本技能覆盖去哪里、怎么抓中国来源）。主仓库：[verifiable-agent-skills](../verifiable-agent-skills)。
