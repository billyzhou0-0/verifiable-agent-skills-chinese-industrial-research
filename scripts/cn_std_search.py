#!/usr/bin/env python3
"""Search Chinese national/industry standards across openstd + hbba + foodmate.

Stdlib-only. Usage:
    python3 cn_std_search.py <keyword> [more keywords...]

Each keyword is searched in all three databases; results printed with status.
Register found URLs in the grounded-citations ledger afterwards.
"""
import json
import re
import sys
import urllib.parse
import urllib.request

UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/120.0 Safari/537.36")


def get(url, headers=None):
    req = urllib.request.Request(url, headers={"User-Agent": UA, **(headers or {})})
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.read()


def openstd(kw):
    """National standard full-text system; returns [(std_no_or_name, hcno)]."""
    url = ("https://openstd.samr.gov.cn/bzgk/gb/std_list?p.p1=0"
           "&p.p90=circulation_date&p.p91=desc&p.p2=" + urllib.parse.quote(kw))
    try:
        html = get(url).decode("utf-8", "replace")
    except Exception as e:
        return [("openstd error: %s" % e, "")]
    return re.findall(r"showInfo\('([0-9A-F]{32})'\);\">([^<]+)</a>", html)


def hbba(kw):
    """全国标准信息公共服务平台 JSON API; returns [(code, chName, status)]."""
    data = urllib.parse.urlencode({"key": kw, "current": 1, "pageSize": 30, "type": ""}).encode()
    try:
        req = urllib.request.Request(
            "https://hbba.sacinfo.org.cn/stdQueryList",
            data=data,
            headers={"User-Agent": UA,
                     "X-Requested-With": "XMLHttpRequest",
                     "Referer": "https://hbba.sacinfo.org.cn/",
                     "Content-Type": "application/x-www-form-urlencoded"},
        )
        raw = urllib.request.urlopen(req, timeout=30).read()
        j = json.loads(raw)
        return [(r["code"], r["chName"], r["status"]) for r in j.get("records", [])]
    except Exception as e:
        return [("hbba error: %s" % e, "", "")]


def foodmate(kw):
    """食品伙伴网标准库 (gb2312); returns [(title, url)]."""
    url = "http://down.foodmate.net/standard/search.php?kw=" + urllib.parse.quote(kw)
    try:
        raw = get(url)
        html = raw.decode("gb18030", "replace")
    except Exception as e:
        return [("foodmate error: %s" % e, "")]
    return re.findall(
        r'<A title="([^"]+)" href="(https://down\.foodmate\.net/standard/sort/[0-9]+/[0-9]+\.html)"',
        html)


def main():
    kws = sys.argv[1:] or ["示例"]
    for kw in kws:
        print("=" * 70)
        print("KEYWORD:", kw)
        print("-" * 70)
        print("## openstd")
        for name, hcno in openstd(kw):
            print("   %s -> hcno=%s" % (name, hcno))
        print("## hbba")
        for code, ch, status in hbba(kw):
            print("   %s | %s | %s" % (code, ch, status))
        print("## foodmate")
        for title, url in foodmate(kw):
            print("   %s -> %s" % (title, url))


if __name__ == "__main__":
    main()
