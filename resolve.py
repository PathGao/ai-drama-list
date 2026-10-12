# 锚点视频 → 若在合集里，取合集中最早发布的正片 → 拉详情（封面、简介）存 final.json
import json, re, time
from search import op
norm = lambda s: re.sub(r"[\s·.,，:：!！()（）《》【】\[\]「」'\"、|｜-]", "", s).lower()
view = lambda bv: json.loads(op.open(f"https://api.bilibili.com/x/web-interface/view?bvid={bv}", timeout=15).read())["data"]
anchors = dict(l.rsplit(" ", 1) for l in open("anchors.txt").read().splitlines())
out = {}
for name, bv in anchors.items():
    skip = bv.endswith("!"); bv = bv.rstrip("!")
    v = view(bv); time.sleep(0.6)
    key = norm(name.replace("系列", ""))[:4]
    s = v.get("ugc_season")
    if s and not skip:
        eps = [e for sec in s["sections"] for e in sec["episodes"]]
        hit = [e for e in eps if key in norm(e["title"]) and not re.search("预告|合集|reaction|采访|花絮|pv|PV", e["title"])]
        if len(hit) >= 2:
            first = min(hit, key=lambda e: e["arc"]["pubdate"])
            if first["bvid"] != bv: v = view(first["bvid"]); time.sleep(0.6)
    out[name] = {"bvid": v["bvid"], "title": v["title"], "pic": v["pic"].replace("http://", "https://"),
                 "desc": v["desc"], "author": v["owner"]["name"], "play": v["stat"]["view"], "changed": v["bvid"] != bv}
    print(("*" if out[name]["changed"] else " "), name, "→", v["bvid"], v["title"][:50])
json.dump(out, open("final.json", "w"), ensure_ascii=False, indent=1)
