#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""网页规格表提取 CLI — 从厂商/行业站产品页批量挖 型号/功率/尺寸/产能 表（2026-08-11 实测）。

用法: python3 spec_table_extract.py <URL> [--jina]
输出: 以 `TBL | ` 开头的表格行 + 以 `KV  | ` 开头的关键参数键值行。

行为:
- 先直接 curl（带 UA）；若返回体过小 (<200 字符) 自动用 r.jina.ai 重抓（JS 渲染站）。
- 表格: 只输出含参数关键词 (型号/产量/功率/尺寸/重量/外形/产能…) 的行，过滤导航垃圾。
- KV: 从剥离标签后的文本正则抓 "参数名+数值" 片段（型号|产量|功率|尺寸|重量|生产能力|模孔|冲头|总功率|主机尺寸…）。
- 实测命中站点: gkzhan.com/chanpin/、zyzhan.com、cnpowder.com.cn、shxsyj.com、keyuanone.com、
  wzhxjx.cn、tablet-press.cn、ctntech.com、leimaijixie88.com、czxf.cn 等（直抓即有表）；
  pm8.cn 只有描述性正文无数字表（表外 KV 提取仍可用）；北极星等反爬站抓不到正文，改用搜索摘要。
依赖: curl 在 PATH 中；仅标准库。
"""
import sys, re, html, subprocess

UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/125.0 Safari/537.36")
KW = ['型号', '产量', '功率', '尺寸', '重量', '外形', '电源', '电压', '冲',
      '粒', '板', '次/分', '次/小时', 'kg', 'kw', 'mm', 't/h', 't/d', '转速',
      '产能', '风量', '电机', '机重', '整机', '模孔', '冲头', '投料', '净重']


def fetch(u, use_jina=False):
    if use_jina:
        r = subprocess.run(["curl", "-s", "--max-time", "90",
                            "https://r.jina.ai/" + u], capture_output=True)
        return r.stdout.decode('utf-8', 'ignore')
    r = subprocess.run(["curl", "-sL", "-A", UA, "--max-time", "30", u],
                       capture_output=True)
    return r.stdout.decode('utf-8', 'ignore')


def extract(t):
    out = []
    for tb in re.findall(r'<table.*?</table>', t, re.S):
        for r in re.findall(r'<tr.*?</tr>', tb, re.S):
            cells = [html.unescape(re.sub('<[^>]+>', '', c)).strip()
                     for c in re.findall(r'<t[dh][^>]*>(.*?)</t[dh]>', r, re.S)]
            cells = [c for c in cells if c]
            if cells and any(k in ' '.join(cells) for k in KW):
                out.append('TBL | ' + ' | '.join(cells))
    txt = html.unescape(re.sub(r'<[^>]+>', ' ', t))
    txt = re.sub(r'\s+', ' ', txt)
    pat = (r'([\u4e00-\u9fa5A-Za-z0-9/（）()·\-]{1,12}?'
           r'(?:型号|产量|功率|尺寸|重量|外形尺寸|外形|电源|电压|总功率|主机功率|'
           r'电机功率|生产能力|产能|转速|冲裁|模孔|冲头|适用胶囊|净重|机重|'
           r'整机重量|整机功率|装机容量|重量)[:：]?\s*[0-9][^,;。|]{0,40})')
    for m in re.finditer(pat, txt):
        s = m.group(1).strip()
        if s not in out:
            out.append('KV  | ' + s)
    return out


if __name__ == "__main__":
    u = sys.argv[1]
    jina = '--jina' in sys.argv
    t = fetch(u, jina)
    if len(t) < 200 and not jina:
        t2 = fetch(u, True)
        if len(t2) > len(t):
            t, jina = t2, True
    print(f"# {u} (jina={jina}, len={len(t)})")
    for line in extract(t)[:60]:
        print(line)
