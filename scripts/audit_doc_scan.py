#!/usr/bin/env python3
"""Programmatic citation-integrity & hallucination-residue scanner for markdown knowledge packs.

Usage: python3 audit_doc_scan.py <dir> [<dir>...]

For each *.md in the dirs (files starting with 00_ are treated as governance
docs and skipped), reports:
  - Sources-block entry count and id range (start != 1 or gaps = 编号跳号)
  - prose citations not defined in Sources (undefined refs) and coverage
  - [unverified] residue (script/hallucination marker left in final docs)
  - mixed citation formats like "[37 工艺文]" ([digits + hanzi] = 说明塞进编号)
  - range-citation "连写" like "[24]-[37]" or "[12]–[31]" (V02-discovered class: guides forbid "-" ranges; must expand to [n][m]... or "(来源 [n] 等 K 个页面)")
  - 【待核实】 count, approximate table data rows (数据点 proxy)
Prints one summary row per file + totals. Stdlib only; no network needed.
"""
import os
import re
import sys


def parse_sources(txt):
    pat = re.compile(r"(?:^|\n)(\[(\d+)\]\s*(https?://[^\n]+))", re.M)
    sources = {}
    for m in pat.finditer(txt):
        sources[int(m.group(2))] = m.group(3).strip()
    return sources


def scan(path):
    with open(path, encoding="utf-8") as fh:
        txt = fh.read()
    sources = parse_sources(txt)
    # prose = everything before the last "[n] URL" line (the Sources block)
    last = max([m.start() for m in re.finditer(r"\[\d+\]\s*https?://", txt)], default=0)
    body = txt[:last]
    cited = sorted(set(int(x) for x in re.findall(r"\[(\d+)\]", body)))
    undefined = [c for c in cited if c not in sources]
    ids = sorted(sources)
    jumps = [(a, b) for a, b in zip(ids, ids[1:]) if b - a > 1]
    unv = len(re.findall(r"\[unverified\]", txt, re.I))
    mixed = re.findall(r"\[(\d+)\s*[\u4e00-\u9fff][^\]]*\]", body)
    # range/连写 citations: [n]-[m], [n]–[m], [n]~[m] (guide rule: 禁止 "-" 范围连写)
    ranges = re.findall(r"\[(\d+)\]\s*[-–—~]\s*\[(\d+)\]", body)
    dsh = len(re.findall(r"【待核实】", txt))
    rows = 0
    for m in re.finditer(r"((?:^\|.*\|$\n?)+)", txt, re.M):
        lines = [l for l in m.group(1).strip().split("\n")
                 if l.startswith("|") and not re.match(r"^\|[\s:\-|]+\|$", l)]
        if len(lines) >= 2:
            rows += len(lines) - 1
    return dict(file=os.path.basename(path), size=os.path.getsize(path),
                n_sources=len(sources), start=ids[0] if ids else None,
                end=ids[-1] if ids else None, n_cited=len(cited),
                undefined=undefined, jumps=jumps, unv=unv,
                mixed=mixed[:6], ranges=ranges, dsh=dsh, table_rows=rows)


def main(dirs):
    files = []
    for d in dirs:
        files += [os.path.join(d, f) for f in sorted(os.listdir(d))
                  if f.endswith(".md") and not f.startswith("00_")]
    hdr = f"{'file':<28}{'KB':>6}{'src':>4}{'id-range':>10}{'cited':>6}{'unv':>4}{'dsh':>5}{'rows':>6}{'jumps':>6}{'undef':>6}{'mixed':>6}{'rng':>5}"
    print(hdr)
    tot = dict(src=0, unv=0, dsh=0, rows=0, jumps=0, undef=0, mixed=0, ranges=0)
    for p in files:
        r = scan(p)
        tot["src"] += r["n_sources"]; tot["unv"] += r["unv"]; tot["dsh"] += r["dsh"]
        tot["rows"] += r["table_rows"]; tot["jumps"] += len(r["jumps"])
        tot["undef"] += len(r["undefined"]); tot["mixed"] += len(r["mixed"])
        tot["ranges"] += len(r["ranges"])
        print(f"{r['file'][:26]:<28}{r['size']/1024:>6.1f}{r['n_sources']:>4}"
              f"{str(r['start'])+'-'+str(r['end']):>10}{r['n_cited']:>6}{r['unv']:>4}"
              f"{r['dsh']:>5}{r['table_rows']:>6}{len(r['jumps']):>6}{len(r['undefined']):>6}{len(r['mixed']):>6}{len(r['ranges']):>5}")
        for a, b in r["jumps"]:
            print(f"    jump: [{a}] -> [{b}]")
        for u in r["undefined"]:
            print(f"    undefined ref: [{u}]")
        for m in r["mixed"]:
            print(f"    mixed format: {m}")
        for a, b in r["ranges"]:
            print(f"    range-cite (连写, must expand): [{a}]-[{b}]")
    print(f"TOTAL files={len(files)} sources={tot['src']} unverified={tot['unv']} "
          f"待核实={tot['dsh']} table_rows={tot['rows']} jumps={tot['jumps']} "
          f"undefined={tot['undef']} mixed={tot['mixed']} ranges={tot['ranges']}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    main(sys.argv[1:])
