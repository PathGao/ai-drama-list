# 用 B 站搜索接口给每部剧取候选视频，缓存到 raw.json
import json, re, time, urllib.parse, urllib.request, http.cookiejar, sys
UA = "Mozilla/5.0 (Macintosh) AppleWebKit/537.36 Chrome/130 Safari/537.36"
cj = http.cookiejar.CookieJar()
op = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
op.addheaders = [("User-Agent", UA), ("Referer", "https://search.bilibili.com/")]
op.open("https://www.bilibili.com/").read()
clean = lambda s: re.sub(r"<[^>]+>", "", s).replace("&quot;", '"').replace("&amp;", "&")
try: raw = json.load(open("raw.json"))
except FileNotFoundError: raw = {}
titles = [l.strip() for l in open(__import__("sys").argv[1])] if len(__import__("sys").argv)>1 else [t for _, ts in json.load(open("list.json")) for t in ts]
for t in titles:
    for q in ((t,) if len(sys.argv)>1 else (t + " AI", t)):
        if q in raw: continue
        url = "https://api.bilibili.com/x/web-interface/search/type?search_type=video&keyword=" + urllib.parse.quote(q)
        d = json.loads(op.open(url, timeout=15).read())
        if d["code"] != 0: print("ERR", q, d["code"], file=sys.stderr); time.sleep(5); continue
        raw[q] = [{"bvid": r["bvid"], "title": clean(r["title"]), "author": r["author"], "desc": r["description"],
                   "pic": "https:" + r["pic"] if r["pic"].startswith("//") else r["pic"], "play": r["play"],
                   "duration": r["duration"], "pubdate": r["pubdate"]} for r in d["data"].get("result") or []]
        json.dump(raw, open("raw.json", "w"), ensure_ascii=False)
        time.sleep(1.2)
print(len(raw))
