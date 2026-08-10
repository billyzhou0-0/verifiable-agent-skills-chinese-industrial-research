#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""360 搜索 CLI — 中文工业/B2B 设备查询的可靠发现通道（实测）。

用法: python3 s360_search.py "<查询词>" [结果数]   (默认 10)
输出: 每行 `标题 | 真实URL | 摘要前180字`

关键点:
- 360 是此环境下唯一可 curl 直抓的中文搜索引擎（Bing/Baidu/搜狗均反爬）。
- 结果块 <li class="res-list"> 的 <h3><a> 带 data-mdurl="真实URL"，
  直接取它即可绕过 so.com/link?m=… JS 跳转（该跳转需搜索页 referer，直开会 404/验证码）。
- 摘要 <p class="res-desc"> 常已含关键数值（型号/功率/产能），先读摘要再决定深抓。
- 搜索词模板命中率最高: "<设备名> 技术参数 外形尺寸 功率"；
  加 site 词 (gkzhan/zyzhan) 可直取带规格表的页面。
依赖: curl 在 PATH 中；仅标准库。
"""
import sys, re, html, subprocess, urllib.parse

UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/125.0 Safari/537.36")


def search(q, n=10):
    url = "https://www.so.com/s?q=" + urllib.parse.quote(q)
    r = subprocess.run(["curl", "-sL", "-A", UA, "--max-time", "25", url],
                       capture_output=True)
    t = r.stdout.decode("utf-8", "ignore")
    items = []
    for block in re.findall(r'<li class="res-list.*?</li>', t, re.S):
        m = re.search(
            r'<h3[^>]*>.*?<a[^>]*href="([^"]+)"[^>]*data-mdurl="([^"]+)"[^>]*>(.*?)</a>',
            block, re.S)
        if not m:
            m = re.search(r'<h3[^>]*>.*?<a[^>]*href="([^"]+)"[^>]*>(.*?)</a>',
                          block, re.S)
            if not m:
                continue
            u, real, ti = m.group(1), '', m.group(2)
        else:
            u, real, ti = m.group(1), m.group(2), m.group(3)
        ti = re.sub('<[^>]+>', '', ti).strip()
        s = re.search(r'<p class="res-desc[^"]*"[^>]*>(.*?)</p>', block, re.S)
        sn = re.sub('<[^>]+>', '', s.group(1)).strip() if s else ''
        items.append((html.unescape(ti), real or u, html.unescape(sn)[:180]))
        if len(items) >= n:
            break
    return items


if __name__ == "__main__":
    q = sys.argv[1]
    n = int(sys.argv[2]) if len(sys.argv) > 2 else 10
    for ti, u, sn in search(q, n):
        print(f"{ti} | {u} | {sn}")
