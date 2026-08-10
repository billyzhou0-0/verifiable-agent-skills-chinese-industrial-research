# Changelog（更新记录）

All notable changes to this project are documented here, following Keep a Changelog with semver versioning. / 本文件按 Keep a Changelog 规范记录本项目所有重要变更。

## [1.0.0] - 2026-08-11

### Initial open-source release / 初始开源发布

- Verifiable research on Chinese industries: GB-standard three-tier lookup, vendor spec extraction, EIA/listed-company data back-to-source, full-coverage audit method, 5 stdlib-only scripts. / 可验证的中国行业调研：标准三层检索、厂商数据提取、环评/年报回源、全量审计法、5 个纯标准库脚本。

## Pre-release evolution（开源前演进史）

Each fix below was proven in real production. / 以下每条修复均在真实生产中验证。

### 1. AI 编造行业数据

- **Fix / 修复**：调研中国行业时 AI 编造型号/标准/URL；搜索引擎被墙、厂商域名悄悄失效（转让域名仍返回 200）。修复：引用台账（抓取时即登记）、来源优先级、查不到标【待核实】、失效分级纪律（查标题不只看状态码）。

### 2. 抽样审计漏检

- **Fix / 修复**：抽样审计「全部可达」的结论被全量轮推翻——发现范围连写 [n]-[m] 13 处、引用错页、值藏在 data-v 属性。修复：用户拒绝抽样后全量轮——590 URL 三遍验证、2,192 数据点回源（格式变体匹配：千分位/万/亿/吨↔万吨）。

### 3. 补强轮误删数据

- **Fix / 修复**：修复升级时存在删数据风险。修复：只加不删纪律 + diff 审计证明零删除来源数据行；覆盖率修复零编造三模式；「页面无此值」结论先回源再采信（88,000 kN 平反案例）。

### 4. 前轮结论被推翻

- **Fix / 修复**：「页面无此值」判定被证明是假阴性——千分位分隔符+实体破折号导致漏检。修复：声明「值不存在」前必须验证两种格式变体；前轮 absence 结论先重新抓页再采信。

### 5. 跨行业标准张冠李戴

- **Fix / 修复**：标准号引用前未回源确认名称与适用行业。修复：标准号引用前必须回源；A+H 股繁体年报简繁关键词双 grep。
