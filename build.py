# final.json + list.json → README.md / index.html
import json, html, urllib.parse
cats = json.load(open("list.json")); fin = json.load(open("final.json"))
NOTE = {"无归": "只找到第一集预告", "超度师": "匹配不确定", "零号档案": "匹配不确定", "最帅之人": "匹配不确定",
        "扳机": "匹配不确定", "合龙": "匹配不确定", "百匠纸契灵": "匹配不确定", "乡村惊魂夜": "单元剧，非第一集",
        "福仙童": "只找到预告", "余烬之后": "只找到第二集", "万物生": "只找到第2集", "引渡小分队": "单元剧，非第一集",
        "反相之地": "1-6 集合集", "污染者": "第一季合集", "执念尸": "第一季合集", "山海": "第一季 1-8 合集",
        "我是地狱": "第一季合集", "神坛之下，众生为炉": "1-4 合集", "我穿越到武侠世界的一天": "1-4 合集", "大天蓬": "1-15 合集",
        "粉墨if系列": "系列短片，独立成篇", "嘴炮女修": "系列短片，独立成篇", "彭皮肚系列": "系列短片"}
SEEN = '<label class="seen"><input type="checkbox"><span>看过</span></label>'
plays = lambda n: f"{n/1e4:.1f}万" if n >= 1e4 else str(n)
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
            cards.append(f'''<div class="card" data-id="{e(t)}" data-k="{e(t + f['title'] + f['author'])}"><a href="{url(f['bvid'])}" target="_blank" rel="noopener">
<div class="cover"><img loading="lazy" decoding="async" width="480" height="270" referrerpolicy="no-referrer" src="{e(f['pic'])}@480w_270h_1c.webp" alt="">{f'<span class="note">{e(note)}</span>' if note else ''}</div>
<div class="body"><h3>{e(t)}</h3><p class="vt">{e(f['title'])}</p>
<p class="meta"><span>{e(f['author'])}</span><span>{plays(f['play'])} 播放</span></p>
<p class="desc">{e(desc)}</p></div></a>{SEEN}</div>''')
        else:
            md.append(f"- {t}（B 站未找到，[搜索]({search(t)})）")
            cards.append(f'''<div class="card miss" data-id="{e(t)}" data-k="{e(t)}"><a href="{search(t)}" target="_blank" rel="noopener">
<div class="cover ph"><span>B 站未找到原片</span></div><div class="body"><h3>{e(t)}</h3><p class="desc">点开去 B 站搜索。</p></div></a>{SEEN}</div>''')
    sec.append(f'<section><h2><span>{e(cat)}</span><small>{len(ts)}</small></h2><div class="grid">{"".join(cards)}</div><details class="done hide"><summary>已看过 <b>0</b> 部</summary><div class="grid"></div></details></section>')
open("README.md", "w").write("\n".join(md) + "\n")
total = sum(len(t) for _, t in cats)
nav = "".join(f'<a href="#c{i}">{e(c)}</a>' for i, (c, _) in enumerate(cats))
body = "".join(s.replace("<section>", f'<section id="c{i}">', 1) for i, s in enumerate(sec))
open("index.html", "w").write(f'''<!doctype html><html lang="zh-CN"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1"><title>AI 剧清单</title><style>
:root{{--bg:#f5f4f1;--card:#fff;--fg:#1b1b1d;--mute:#6e6e76;--soft:#9a9aa2;--line:#e6e4df;--acc:#fb7299;--acc2:#fff0f4;--shadow:0 1px 2px rgba(0,0,0,.04),0 6px 20px rgba(0,0,0,.05)}}
@media (prefers-color-scheme:dark){{:root{{--bg:#111113;--card:#1b1b1e;--fg:#ededf0;--mute:#a3a3ab;--soft:#76767e;--line:#2a2a2f;--acc2:#3a1f28;--shadow:0 1px 2px rgba(0,0,0,.3)}}}}
*{{box-sizing:border-box}}html{{scroll-behavior:smooth;scroll-padding-top:112px}}
body{{margin:0;background:var(--bg);color:var(--fg);font:15px/1.55 -apple-system,BlinkMacSystemFont,"PingFang SC","Hiragino Sans GB","Microsoft YaHei",sans-serif;-webkit-font-smoothing:antialiased}}
.hero{{text-align:center;padding:40px 16px 18px}}
h1{{margin:0;font-size:30px;letter-spacing:.04em;font-weight:800}}h1 i{{font-style:normal;color:var(--acc)}}
.sub{{margin:6px 0 0;color:var(--mute);font-size:14px}}
#stat{{display:inline-block;margin-top:10px;padding:3px 12px;border-radius:999px;background:var(--acc2);color:var(--acc);font-size:13px;font-weight:600}}#stat:empty{{display:none}}
.bar{{position:sticky;top:0;z-index:3;padding:10px 16px;background:color-mix(in srgb,var(--bg) 82%,transparent);backdrop-filter:blur(12px);-webkit-backdrop-filter:blur(12px);border-bottom:1px solid var(--line);text-align:center}}
input[type=search]{{width:100%;max-width:420px;padding:9px 16px;border:1px solid var(--line);border-radius:999px;background:var(--card);color:var(--fg);font-size:14px;outline:none;transition:border-color .15s,box-shadow .15s}}
input[type=search]:focus{{border-color:var(--acc);box-shadow:0 0 0 3px var(--acc2)}}
nav{{display:flex;gap:8px;justify-content:center;flex-wrap:wrap;margin-top:10px}}
nav a{{padding:4px 12px;border-radius:999px;background:var(--card);border:1px solid var(--line);color:var(--mute);font-size:13px;text-decoration:none;white-space:nowrap;transition:color .15s,border-color .15s}}
nav a:hover{{color:var(--acc);border-color:var(--acc)}}
@media (max-width:640px){{nav{{flex-wrap:nowrap;justify-content:flex-start;overflow-x:auto;scrollbar-width:none;margin:10px -16px 0;padding:0 16px}}nav::-webkit-scrollbar{{display:none}}.hero{{padding-top:28px}}h1{{font-size:26px}}}}
main{{max-width:1320px;margin:0 auto;padding:4px 16px 64px}}
h2{{display:flex;align-items:center;gap:10px;font-size:19px;margin:36px 0 14px}}
h2 span{{padding-left:12px;border-left:4px solid var(--acc);line-height:1.2}}
h2 small{{font-size:12px;font-weight:600;color:var(--mute);background:var(--card);border:1px solid var(--line);border-radius:999px;padding:1px 9px}}
.grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(250px,1fr));gap:16px}}
.card{{position:relative;display:flex;flex-direction:column;background:var(--card);border:1px solid var(--line);border-radius:14px;overflow:hidden;box-shadow:var(--shadow);transition:border-color .15s,box-shadow .15s}}
.card:hover{{border-color:var(--acc);box-shadow:0 0 0 3px var(--acc2),var(--shadow)}}
.card>a{{color:inherit;text-decoration:none;flex:1;display:flex;flex-direction:column}}
.cover{{position:relative;aspect-ratio:16/9;background:var(--line);overflow:hidden}}
.cover img{{width:100%;height:100%;object-fit:cover;display:block}}
.cover::after{{content:"";position:absolute;inset:auto 0 0;height:40%;background:linear-gradient(transparent,rgba(0,0,0,.45));pointer-events:none}}
.ph{{display:grid;place-items:center;color:var(--soft);font-size:13px;background:repeating-linear-gradient(135deg,var(--line) 0 10px,transparent 10px 20px)}}.ph::after{{display:none}}
.ph span{{background:var(--card);padding:4px 12px;border-radius:999px}}
.note{{position:absolute;left:10px;bottom:9px;z-index:1;font-size:12px;font-weight:600;color:#fff;background:var(--acc);border-radius:6px;padding:1px 7px}}
.body{{padding:12px 14px 14px;display:flex;flex-direction:column;flex:1}}
h3{{margin:0;font-size:17px;font-weight:700}}
.vt{{margin:4px 0 0;font-size:13px;color:var(--fg);opacity:.85}}
.meta{{display:flex;justify-content:space-between;gap:8px;margin:6px 0 0;font-size:12px;color:var(--soft)}}.meta span:first-child{{overflow:hidden;text-overflow:ellipsis;white-space:nowrap}}.meta span:last-child{{flex-shrink:0}}
.desc{{margin:10px 0 0;padding-top:10px;border-top:1px dashed var(--line);font-size:12.5px;line-height:1.65;color:var(--mute);white-space:pre-line;overflow-wrap:anywhere}}
.seen{{position:absolute;top:10px;right:10px;z-index:2;display:flex;gap:5px;align-items:center;padding:4px 10px;border-radius:999px;background:rgba(20,20,22,.55);backdrop-filter:blur(6px);-webkit-backdrop-filter:blur(6px);color:#fff;font-size:12.5px;cursor:pointer;white-space:nowrap;user-select:none;transition:background .15s}}
.seen:hover{{background:rgba(20,20,22,.75)}}.seen input{{margin:0;accent-color:var(--acc)}}
.done .seen{{background:var(--acc)}}.done .card{{box-shadow:none}}.done .cover img{{filter:grayscale(.7);opacity:.75}}.done .body{{opacity:.65}}
.done{{margin-top:16px}}.done summary{{display:inline-block;cursor:pointer;color:var(--mute);font-size:13px;padding:5px 14px;border:1px dashed var(--line);border-radius:999px;list-style:none}}
.done summary::-webkit-details-marker{{display:none}}.done summary::before{{content:"▸ "}}.done[open] summary::before{{content:"▾ "}}.done summary:hover{{color:var(--acc);border-color:var(--acc)}}.done .grid{{margin-top:12px}}
.hide{{display:none!important}}
footer{{text-align:center;color:var(--soft);font-size:12px;padding:0 16px 40px}}
</style></head><body>
<header class="hero"><h1>AI <i>剧</i>清单</h1><p class="sub">{total} 部 · {len(cats)} 类 · 点卡片看 B 站第一集</p><div id="stat"></div></header>
<div class="bar"><input id="q" type="search" placeholder="搜剧名、标题或 UP 主" aria-label="搜索"><nav>{nav}</nav></div>
<main>{body}</main><footer>勾选「看过」只保存在你自己的浏览器里</footer><script>
const q=document.getElementById("q");q.oninput=()=>{{const s=q.value.trim().toLowerCase();
document.querySelectorAll(".card").forEach(c=>c.classList.toggle("hide",!!s&&!c.dataset.k.toLowerCase().includes(s)));
document.querySelectorAll("section").forEach(x=>x.classList.toggle("hide",!x.querySelector(".card:not(.hide)")))}};
// 看过状态只存在本机浏览器
const KEY="seen-v1";let seen=new Set();try{{seen=new Set(JSON.parse(localStorage.getItem(KEY)||"[]"))}}catch(_){{}}
const total=document.querySelectorAll(".card").length,order=new Map([...document.querySelectorAll(".card")].map((c,i)=>[c,i]));
function place(c){{const sec=c.closest("section"),on=seen.has(c.dataset.id),g=on?sec.querySelector(".done .grid"):sec.querySelector(".grid");
c.querySelector("input").checked=on;c.querySelector(".seen span").textContent=on?"取消看过":"看过";const after=[...g.children].find(x=>order.get(x)>order.get(c));g.insertBefore(c,after||null)}}
function count(){{document.querySelectorAll("section").forEach(sec=>{{const n=sec.querySelectorAll(".done .card").length;
sec.querySelector(".done b").textContent=n;sec.querySelector(".done").classList.toggle("hide",!n)}});
document.getElementById("stat").textContent=seen.size?`已看 ${{seen.size}} / ${{total}}`:""}}
document.querySelectorAll(".card").forEach(c=>{{place(c);c.querySelector("input").onchange=e=>{{
e.target.checked?seen.add(c.dataset.id):seen.delete(c.dataset.id);try{{localStorage.setItem(KEY,JSON.stringify([...seen]))}}catch(_){{}}place(c);count()}}}});count();
</script></body></html>''')
print(len(fin), "matched")
