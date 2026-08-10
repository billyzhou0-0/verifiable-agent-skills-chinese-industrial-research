#!/usr/bin/env python3
"""Bulk keyword search of openstd std_list, extracting hcno + standard metadata.

Worker 6 recipe (2026-08): std_list rows embed hcno as
`<a href="javascript:o('<32-HEX>');">标准号</a>` — no browser needed.
Built-in 5s rate-limit sleep between keywords (rapid-fire queries return
empty result lists, which is transient limiting, NOT "no standards").

Usage:
  python3 openstd_std_list.py 印染 造纸 压铸           # one query per keyword
  python3 openstd_std_list.py --sleep 8 压铸机         # custom rate-limit
Output per row: hcno|标准号|名称|类型|状态|发布日|实施日
"""
import html
import re
import subprocess
import sys
import time
import urllib.parse

UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/120.0 Safari/537.36")


def fetch(keyword: str, sleep_s: int = 5) -> list:
    q = urllib.parse.quote(keyword)
    url = f"https://openstd.samr.gov.cn/bzgk/std/std_list?p.p1=0&p.p2={q}"
    r = subprocess.run(
        ["curl", "-s", "-m", "20", "-A", UA, url],
        capture_output=True, text=True,
    )
    raw = r.stdout
    rows = re.findall(r"<tr[^>]*>(.*?)</tr>", raw, re.S)
    out = []
    for it in rows:
        hcno_m = re.search(r"o\('([0-9A-F]+)'\)", it)
        tds = re.findall(r"<td[^>]*>(.*?)</td>", it, re.S)
        txts = [html.unescape(re.sub(r"<[^>]+>", "", t)).strip() for t in tds]
        txts = [t for t in txts if t.strip()]
        if hcno_m and len(txts) >= 7:
            out.append((hcno_m.group(1), " | ".join(txts[:7])))
    return out


def main() -> int:
    args = sys.argv[1:]
    sleep_s = 5
    if args and args[0] == "--sleep" and len(args) >= 3:
        sleep_s = int(args[1])
        args = args[2:]
    if not args:
        print(__doc__)
        return 1
    for kw in args:
        res = fetch(kw, sleep_s)
        print(f"== {kw}: {len(res)} 条 ==")
        for hcno, line in res:
            print(hcno, line)
        time.sleep(sleep_s)
    return 0


if __name__ == "__main__":
    sys.exit(main())
