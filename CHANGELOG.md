# Changelog（更新记录）

All notable changes to this project are documented here, following Keep a Changelog with semver versioning. / 本文件按 Keep a Changelog 规范记录本项目所有重要变更。

## [1.1.1] - 2026-08-11

### Patch Changes / 补丁

- [`f5cf663`](https://github.com/billyzhou0-0/verifiable-agent-skills-chinese-industrial-research/commit/f5cf663) Add `CHANGELOG.md` and `CONTRIBUTING.md`; add an **Example usage（使用示例）** section to `SKILL.md` (scenario → steps → expected output). / 添加更新记录与贡献指南；SKILL.md 新增使用示例（场景→步骤→输出）。

## [1.1.0] - 2026-08-11

### Minor Changes / 次要版本：发布打磨（Release polish）

- [`9f96c1d`](https://github.com/billyzhou0-0/verifiable-agent-skills-chinese-industrial-research/commit/9f96c1d), [`e1ffbb8`](https://github.com/billyzhou0-0/verifiable-agent-skills-chinese-industrial-research/commit/e1ffbb8) — README overhaul: / README 改造：
  - Description rewritten pain-point-first (EN+CN) / 描述痛点驱动（双语）
  - Topics tags added / 添加 Topics 标签
  - License + Stars badges / License 和 Stars 徽章
  - 'Why this exists' pain-point story / '为什么做这个'痛点故事
  - README fully bilingual (native-level EN + CN, every paragraph and table cell) / README 全面中英双语

## [1.0.0] - 2026-08-11

### Initial open-source release / 初始开源发布

- [`6321013`](https://github.com/billyzhou0-0/verifiable-agent-skills-chinese-industrial-research/commit/6321013) — Initial release. / 初始发布。

- **Verifiability golden rules / 可验证金规则** — URLs registered in the citation ledger at retrieval time (never from memory); write-as-you-go per industry; never fabricate (missing → 【待核实】); source priority openstd > industry standards > vendor sites. 抓取时即登记引用台账；边研边写；绝不编造（查不到标【待核实】）；来源优先级。
- **Proven channels / 实测渠道配方** — GB-standard three-tier lookup (openstd/hbba/foodmate), vendor spec extraction recipes (sitemap, data-v attribute tables, image-PDF OCR), EIA full-report direct links, listed-company documents (cninfo/prospectus). 标准三层检索、厂商数据提取配方（sitemap/data-v 属性表/图片 PDF OCR）、环评全本直链、上市公司文档。
- **Audit methodology / 审计方法论** — programmatic full-text scan, sampled source verification, value verification with format-variant checks, full-coverage round (590 URLs / 2,192 data points verified in production, 0 fabricated findings). 程序化扫描、抽样源验证、格式变体数值验证、全量轮（实战 590 URL/2,192 数据点，0 编造）。
- **Tiered acceptance lines / 分级验收线** — A 类 (≥30 sources, ≥60 data points) vs B 类 (≥15 sources + honest-declaration triad); the tier line is not a laziness line. A/B 分级验收；分级线不是偷懒线。
- **Reinforcement round / 补强轮** — V01→V02 patch per audit's copy-executable fix instructions; add-only discipline with diff audit; coverage repair without fabricating (3 proven patterns). 按审计指令补丁升级；只加不删+diff 审计；零编造覆盖率修复三模式。
- **Included scripts / 附带脚本** — `audit_doc_scan.py`, `cn_std_search.py`, `openstd_std_list.py`, `s360_search.py`, `spec_table_extract.py` (all stdlib-only). 5 个纯标准库脚本。

> Background / 背景：The methodology ran a 21-industry multi-worker research pipeline (2026-08), produced 21 knowledge packs with 100% citation integrity, and evolved the process guide through V1→V7 plus four audit rounds (initial / full-coverage / reinforcement / acceptance V03) before open-sourcing. / 方法论运行了 21 行业多 Worker 调研流水线（2026-08），产出 21 个知识包（引用完整性 100%），流程指南演进 V1→V7，历经四轮审计后开源。
