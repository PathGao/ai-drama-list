# final.json + list.json → README.md / index.html
import json, html, urllib.parse
cats = json.load(open("list.json")); fin = json.load(open("final.json"))
NOTE = {"无归": "只找到第一集预告", "超度师": "匹配不确定", "零号档案": "匹配不确定", "最帅之人": "匹配不确定",
        "扳机": "匹配不确定", "合龙": "匹配不确定", "百匠纸契灵": "匹配不确定", "乡村惊魂夜": "单元剧，非第一集",
        "福仙童": "只找到预告", "余烬之后": "只找到第二集", "万物生": "只找到第2集", "引渡小分队": "单元剧，非第一集",
        "反相之地": "1-6 集合集", "污染者": "第一季合集", "执念尸": "第一季合集", "山海": "第一季 1-8 合集",
        "我是地狱": "第一季合集", "神坛之下，众生为炉": "1-4 合集", "我穿越到武侠世界的一天": "1-4 合集", "大天蓬": "1-15 合集",
        "粉墨if系列": "系列短片，独立成篇", "嘴炮女修": "系列短片，独立成篇", "彭皮肚系列": "系列短片"}
search = lambda t: "https://search.bilibili.com/all?keyword=" + urllib.parse.quote(t)
url = lambda bv: f"https://www.bilibili.com/video/{bv}"
e = html.escape
md, sec = ["# 最近看的 AI 剧\n", f"共 {sum(len(t) for _, t in cats)} 部。链接指向 B 站第一集；没找到的给搜索链接。\n"], []
for cat, ts in cats:
    md.append(f"\n## {cat}\n")
    cards = []
    for t in ts:
        f, note = fin.get(t), NOTE.get(t, "")
        if f:
            md.append(f"- [{t}]({url(f['bvid'])})" + (f"（{note}）" if note else ""))
            desc = f["desc"].strip() or "（无简介）"
            cards.append(f'''<a class="card" href="{url(f['bvid'])}" target="_blank" rel="noopener" data-k="{e(t + f['title'] + f['author'])}">
<img loading="lazy" referrerpolicy="no-referrer" src="{e(f['pic'])}@480w_270h_1c.webp" alt="">
<div class="body"><h3>{e(t)}</h3>{f'<span class="note">{e(note)}</span>' if note else ''}
<p class="vt">{e(f['title'])}</p><p class="meta">UP：{e(f['author'])} · {f['play']:,} 播放</p>
<p class="desc">{e(desc)}</p></div></a>''')
        else:
            md.append(f"- {t}（B 站未找到，[搜索]({search(t)})）")
            cards.append(f'''<a class="card miss" href="{search(t)}" target="_blank" rel="noopener" data-k="{e(t)}">
<div class="ph">未找到</div><div class="body"><h3>{e(t)}</h3><p class="desc">B 站没搜到原片，点开去搜索。</p></div></a>''')
    sec.append(f'<section><h2>{e(cat)} <small>{len(ts)}</small></h2><div class="grid">{"".join(cards)}</div></section>')
open("README.md", "w").write("\n".join(md) + "\n")
nav = "".join(f'<a href="#c{i}">{e(c)}</a>' for i, (c, _) in enumerate(cats))
body = "".join(s.replace("<section>", f'<section id="c{i}">', 1) for i, s in enumerate(sec))
open("index.html", "w").write(f'''<!doctype html><html lang="zh-CN"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1"><title>AI 剧清单</title><style>
:root{{--bg:#f6f6f4;--card:#fff;--fg:#1d1d1f;--mute:#6b6b70;--line:#e3e3e0;--acc:#fb7299}}
@media (prefers-color-scheme:dark){{:root{{--bg:#151517;--card:#1f1f22;--fg:#ececee;--mute:#9a9aa2;--line:#2e2e33}}}}
*{{box-sizing:border-box}}body{{margin:0;background:var(--bg);color:var(--fg);font:15px/1.5 -apple-system,"PingFang SC",sans-serif}}
header{{position:sticky;top:0;z-index:2;background:var(--bg);border-bottom:1px solid var(--line);padding:12px 16px}}
h1{{margin:0 0 8px;font-size:20px}}input{{width:100%;max-width:360px;padding:7px 10px;border:1px solid var(--line);border-radius:8px;background:var(--card);color:var(--fg);font-size:14px}}
nav{{display:flex;flex-wrap:wrap;gap:6px 14px;margin-top:8px;font-size:13px}}nav a{{color:var(--mute);text-decoration:none}}nav a:hover{{color:var(--acc)}}
main{{max-width:1280px;margin:0 auto;padding:8px 16px 48px}}h2{{font-size:17px;margin:28px 0 12px;scroll-margin-top:130px}}h2 small{{color:var(--mute);font-weight:400}}
.grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(240px,1fr));gap:14px}}
.card{{display:flex;flex-direction:column;background:var(--card);border:1px solid var(--line);border-radius:10px;overflow:hidden;color:inherit;text-decoration:none}}
.card:hover{{border-color:var(--acc)}}.card img,.ph{{width:100%;aspect-ratio:16/9;object-fit:cover;background:var(--line);display:block}}
.ph{{display:grid;place-items:center;color:var(--mute)}}.body{{padding:10px 12px 12px}}h3{{margin:0;font-size:16px}}
.note{{display:inline-block;margin-top:4px;font-size:12px;color:var(--acc);border:1px solid var(--acc);border-radius:4px;padding:0 5px}}
.vt{{margin:6px 0 2px;font-size:13px}}.meta{{margin:0;font-size:12px;color:var(--mute)}}
.desc{{margin:6px 0 0;font-size:12.5px;color:var(--mute);white-space:pre-line;display:-webkit-box;-webkit-line-clamp:4;-webkit-box-orient:vertical;overflow:hidden}}
.card:hover .desc{{-webkit-line-clamp:unset}}.hide{{display:none}}
</style></head><body><header><h1>AI 剧清单</h1><input id="q" type="search" placeholder="搜剧名、标题或 UP 主" aria-label="搜索"><nav>{nav}</nav></header>
<main>{body}</main><script>
const q=document.getElementById("q");q.oninput=()=>{{const s=q.value.trim().toLowerCase();
document.querySelectorAll(".card").forEach(c=>c.classList.toggle("hide",!!s&&!c.dataset.k.toLowerCase().includes(s)));
document.querySelectorAll("section").forEach(x=>x.classList.toggle("hide",!x.querySelector(".card:not(.hide)")))}}
</script></body></html>''')
print(len(fin), "matched")
