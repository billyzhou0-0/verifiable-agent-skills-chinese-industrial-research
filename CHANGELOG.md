# Changelog（更新记录）

## Open-source release / 开源发布

- Verifiable research on Chinese industries: three-tier standard lookup, vendor spec extraction, EIA/listed-company data back-to-source, full-coverage audit method, 5 stdlib-only scripts. / 可验证的中国行业调研：标准三层检索、厂商数据提取、环评/年报回源、全量审计法、5 个纯标准库脚本。

## Initial version / 最初版本

- The verifiable research workflow took shape: researching Chinese industries, the AI fabricated model numbers/standards/URLs, search engines were walled, vendor domains silently rotted → a citation ledger (register at retrieval time), source priority, unknown marked 【待核实】, and dead-domain discipline were established. / 可验证调研工作流成型：调研中国行业时 AI 编造型号/标准/URL、搜索引擎被墙、厂商域名悄悄失效 → 建立引用台账（抓取时即登记）、来源优先级、查不到标【待核实】、失效分级纪律。

## Second update / 第二次更新

- The pipeline expanded to 30+ industries → a full-coverage audit mechanism was built: 5,000+ URLs and 20,000+ data points verified back-to-source one by one, hundreds of problem classes found (range run-ons, wrong-page citations, values hidden in page attributes); the reinforcement round upgraded packs per copy-executable fix instructions, add-only, with a diff audit proving zero sourced rows deleted. / 调研流水线扩展到 30+ 个行业 → 建立全量审计机制：5,000+ 个 URL、20,000+ 个数据点逐条回源验证，累计发现问题数百处（范围连写、引用错页、数值藏匿于页面属性）；补强轮按修复指令升级、只加不删，diff 审计证明零删除来源数据。

## Third update / 第三次更新

- False-negative "value not on page" judgments appeared → format-variant verification before declaring a value absent (thousands separators, entity-encoded dashes), previous-round conclusions re-fetched before being trusted; traditional-Chinese annual reports → grep with both simplified and traditional keywords; standard numbers re-sourced before citation. / 出现「页面无此值」的假阴性误判 → 声明值不存在前必须验证格式变体（千分位/实体破折号等），前轮结论先重新抓页再采信；A+H 股繁体年报 → 简繁关键词双 grep；标准号引用前必须回源确认。
