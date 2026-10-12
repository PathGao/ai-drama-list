# final.json + list.json → README.md / index.html
import json, html, urllib.parse
cats = json.load(open("list.json")); fin = json.load(open("final.json"))
NOTE = {"无归": "只找到第一集预告", "超度师": "匹配不确定", "零号档案": "匹配不确定",
        "扳机": "匹配不确定", "合龙": "匹配不确定", "百匠纸契灵": "匹配不确定", "乡村惊魂夜": "单元剧，非第一集",
        "福仙童": "只找到预告", "余烬之后": "只找到第二集", "万物生": "只找到第2集", "引渡小分队": "单元剧，非第一集",
        "反相之地": "1-6 集合集", "污染者": "第一季合集", "执念尸": "第一季合集", "山海": "第一季 1-8 合集",
        "我是地狱": "第一季合集", "神坛之下，众生为炉": "1-4 合集", "我穿越到武侠世界的一天": "1-4 合集", "大天蓬": "1-15 合集",
        "粉墨if系列": "系列短片，独立成篇", "安宁大厦生存守则": "前几集合集", "嘴炮女修": "系列短片，独立成篇", "彭皮肚系列": "系列短片"}
ACTS = '<div class="acts"><label class="act fav"><input type="checkbox"><span>追剧</span></label><label class="act seen"><input type="checkbox"><span>看过</span></label></div>'
plays = lambda n: f"{n/1e4:.1f}万" if n >= 1e4 else str(n)
search = lambda t: "https://search.bilibili.com/all?keyword=" + urllib.parse.quote(t)
url = lambda bv: f"https://www.bilibili.com/video/{bv}"
e = html.escape
order = lambda ts: sorted(ts, key=lambda t: (t not in fin, -fin[t]["play"] if t in fin else 0))  # 播放量降序，没找到原片的排末尾


def card(t):
    f, note = fin.get(t), NOTE.get(t, "")
    if not f:
        return f'''<div class="card miss" data-id="{e(t)}" data-k="{e(t)}"><div class="inner"><a href="{search(t)}" target="_blank" rel="noopener">
<div class="cover ph"><span>B 站未找到原片</span></div><div class="body"><h4>{e(t)}</h4><p class="desc">点开去 B 站搜索。</p></div></a>{ACTS}</div></div>'''
    return f'''<div class="card" data-id="{e(t)}" data-k="{e(t + f['title'] + f['author'])}"><div class="inner"><a href="{url(f['bvid'])}" target="_blank" rel="noopener">
<div class="cover"><img loading="lazy" decoding="async" width="480" height="270" referrerpolicy="no-referrer" src="{e(f['pic'])}@480w_270h_1c.webp" alt="">{f'<span class="note">{e(note)}</span>' if note else ''}</div>
<div class="body"><h4>{e(t)}</h4><p class="vt">{e(f['title'])}</p>
<p class="meta"><span>{e(f['author'])}</span><span>{plays(f['play'])} 播放</span></p>
<p class="desc">{e(f["desc"].strip() or "（无简介）")}</p></div></a>{ACTS}</div></div>'''


total = sum(len(ts) for _, subs in cats for _, ts in subs)
md = ["# 最近看的 AI 剧\n", f"共 {total} 部。链接指向 B 站第一集；没找到的给搜索链接。网页版：https://pathgao.github.io/ai-drama-list/\n"]
secs, toc = [], []
for i, (cat, subs) in enumerate(cats):
    n = sum(len(ts) for _, ts in subs)
    md.append(f"\n## {cat}\n")
    blocks, links = [], []
    for j, (sub, ts) in enumerate(subs):
        md.append(f"\n### {sub}\n")
        for t in order(ts):
            f = fin.get(t)
            md.append(f"- [{t}]({url(f['bvid'])})" + (f"（{NOTE[t]}）" if t in NOTE else "") if f else f"- {t}（B 站未找到，[搜索]({search(t)})）")
        blocks.append(f'<div class="sub" id="c{i}-{j}"><h3>{e(sub)}<small>{len(ts)}</small></h3><div class="grid">{"".join(card(t) for t in order(ts))}</div></div>')
        links.append(f'<a class="l2" href="#c{i}-{j}">{e(sub)}<small>{len(ts)}</small></a>')
    secs.append(f'<section id="c{i}"><h2><span>{e(cat)}</span><small>{n}</small></h2>{"".join(blocks)}'
                f'<details class="done hide"><summary>已看过 <b>0</b> 部</summary><div class="grid"></div></details></section>')
    toc.append(f'<div class="grp"><a class="l1" href="#c{i}">{e(cat)}<small>{n}</small></a><div class="kids">{"".join(links)}</div></div>')
open("README.md", "w").write("\n".join(md) + "\n")

CSS = r"""
:root{--bg:#f5f4f1;--card:#fff;--fg:#1b1b1d;--mute:#6e6e76;--soft:#9a9aa2;--line:#e6e4df;--acc:#fb7299;--acc2:#fff0f4;--gold:#f5a623;--shadow:0 1px 2px rgba(0,0,0,.04),0 6px 20px rgba(0,0,0,.05)}
@media (prefers-color-scheme:dark){:root{--bg:#111113;--card:#1b1b1e;--fg:#ededf0;--mute:#a3a3ab;--soft:#76767e;--line:#2a2a2f;--acc2:#3a1f28;--shadow:0 1px 2px rgba(0,0,0,.3)}}
*{box-sizing:border-box}html{scroll-behavior:smooth;scroll-padding-top:24px}
body{margin:0;background:var(--bg);color:var(--fg);font:15px/1.55 -apple-system,BlinkMacSystemFont,"PingFang SC","Hiragino Sans GB","Microsoft YaHei",sans-serif;-webkit-font-smoothing:antialiased}
#prog{position:fixed;top:0;left:0;height:3px;width:0;background:linear-gradient(90deg,var(--acc),var(--gold));z-index:20}
.hero{text-align:center;padding:48px 16px 26px;background:radial-gradient(600px 220px at 50% 0,var(--acc2),transparent 70%)}
h1{margin:0;font-size:34px;letter-spacing:.06em;font-weight:800}h1 i{font-style:normal;color:var(--acc)}
.sub-t{margin:6px 0 0;color:var(--mute);font-size:14px}
#stat{display:inline-block;margin-top:10px;padding:3px 12px;border-radius:999px;background:var(--acc2);color:var(--acc);font-size:13px;font-weight:600}#stat:empty{display:none}
.layout{display:grid;grid-template-columns:232px minmax(0,1fr);gap:28px;max-width:1480px;margin:0 auto;padding:0 20px}
aside{position:sticky;top:16px;align-self:start;max-height:calc(100vh - 32px);display:flex;flex-direction:column;gap:12px}
input[type=search]{width:100%;padding:9px 16px;border:1px solid var(--line);border-radius:999px;background:var(--card);color:var(--fg);font-size:14px;outline:none;transition:border-color .15s,box-shadow .15s}
input[type=search]:focus{border-color:var(--acc);box-shadow:0 0 0 3px var(--acc2)}
.toc{overflow-y:auto;scrollbar-width:thin;padding:4px 0 12px;border-left:2px solid var(--line)}
.toc a{display:flex;justify-content:space-between;gap:8px;text-decoration:none;color:var(--mute);margin-left:-2px;border-left:2px solid transparent;transition:color .15s,border-color .15s,background .15s}
.toc small{color:var(--soft);font-size:11.5px;font-variant-numeric:tabular-nums}
.l1{padding:6px 10px 6px 14px;font-size:14px;font-weight:600;color:var(--fg)!important}
.l2{padding:3px 10px 3px 26px;font-size:13px}
.toc a:hover{color:var(--acc)}
.toc .on{border-left-color:var(--acc);color:var(--acc)!important;background:linear-gradient(90deg,var(--acc2),transparent)}
.toc .on small{color:var(--acc)}
.kids{display:none}.grp.open .kids{display:block}
.toc .fav-l{color:var(--gold)!important}
main{min-width:0;padding-bottom:64px}
section{margin-top:8px}
h2{display:flex;align-items:center;gap:10px;font-size:21px;margin:28px 0 4px}
h2 span{padding-left:12px;border-left:4px solid var(--acc);line-height:1.2}
h2 small,h3 small{font-size:12px;font-weight:600;color:var(--mute);background:var(--card);border:1px solid var(--line);border-radius:999px;padding:1px 9px}
h3{display:flex;align-items:center;gap:8px;font-size:15px;font-weight:600;color:var(--mute);margin:22px 0 12px}
h3::before{content:"";width:6px;height:6px;border-radius:50%;background:var(--acc)}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(250px,1fr));gap:18px}
/* 卡片占位固定高：封面 16:9 + 正文 186px；内容层绝对定位，悬停时向下展开盖住下一行，不推动布局 */
.card{position:relative;--bodyh:186px}
.card::before{content:"";display:block;padding-bottom:calc(56.25% + var(--bodyh))}
.inner{position:absolute;inset:0 0 auto;height:100%;display:flex;flex-direction:column;background:var(--card);border:1px solid var(--line);border-radius:16px;overflow:hidden;box-shadow:var(--shadow);transition:box-shadow .2s,border-color .2s}
.inner::after{content:"";position:absolute;inset:auto 0 0;height:22px;background:linear-gradient(transparent,var(--card));pointer-events:none}
.card:hover .inner,.card:focus-within .inner{height:auto;min-height:100%;z-index:5;border-color:var(--acc);box-shadow:0 0 0 3px var(--acc2),0 18px 40px rgba(0,0,0,.18)}
.card:hover .inner::after,.card:focus-within .inner::after{display:none}
.inner>a{color:inherit;text-decoration:none;flex:1;display:flex;flex-direction:column;outline:none}
.cover{position:relative;aspect-ratio:16/9;background:var(--line);overflow:hidden;flex-shrink:0}
.cover img{width:100%;height:100%;object-fit:cover;display:block;transition:transform .5s cubic-bezier(.2,.7,.2,1)}
.card:hover .cover img{transform:scale(1.05)}
.cover::after{content:"";position:absolute;inset:auto 0 0;height:45%;background:linear-gradient(transparent,rgba(0,0,0,.5));pointer-events:none}
.cover::before{content:"";position:absolute;left:50%;top:50%;z-index:1;width:46px;height:46px;margin:-23px 0 0 -23px;border-radius:50%;background:rgba(251,114,153,.92) url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24'%3E%3Cpath fill='white' d='M8 5v14l11-7z'/%3E%3C/svg%3E") 55% 50%/22px no-repeat;opacity:0;transform:scale(.8);transition:opacity .2s,transform .2s;box-shadow:0 6px 18px rgba(251,114,153,.45)}
.card:hover .cover::before{opacity:1;transform:scale(1)}
.ph{display:grid;place-items:center;color:var(--soft);font-size:13px;background:repeating-linear-gradient(135deg,var(--line) 0 10px,transparent 10px 20px)}.ph::after,.ph::before{display:none}
.ph span{background:var(--card);padding:4px 12px;border-radius:999px}
.note{position:absolute;left:10px;bottom:9px;z-index:1;font-size:12px;font-weight:600;color:#fff;background:var(--acc);border-radius:6px;padding:1px 7px}
.body{padding:12px 14px 14px;display:flex;flex-direction:column;flex:1}
h4{margin:0;font-size:17px;font-weight:700;letter-spacing:.01em}
.vt{margin:4px 0 0;font-size:13px;line-height:1.5;opacity:.85}
.meta{display:flex;justify-content:space-between;gap:8px;margin:6px 0 0;font-size:12px;color:var(--soft)}.meta span:first-child{overflow:hidden;text-overflow:ellipsis;white-space:nowrap}.meta span:last-child{flex-shrink:0}
.desc{margin:10px 0 0;padding-top:10px;border-top:1px dashed var(--line);font-size:12.5px;line-height:1.65;color:var(--mute);white-space:pre-line;overflow-wrap:anywhere}
.vt,.desc{display:-webkit-box;-webkit-box-orient:vertical;overflow:hidden}.vt{-webkit-line-clamp:2}.desc{-webkit-line-clamp:3}
.card:hover .vt,.card:hover .desc,.card:focus-within .vt,.card:focus-within .desc{-webkit-line-clamp:unset}
.acts{position:absolute;top:10px;right:10px;z-index:2;display:flex;gap:6px}
.act{display:flex;gap:5px;align-items:center;padding:4px 10px;border-radius:999px;background:rgba(20,20,22,.55);backdrop-filter:blur(6px);-webkit-backdrop-filter:blur(6px);color:#fff;font-size:12.5px;cursor:pointer;white-space:nowrap;user-select:none;transition:background .15s}
.act:hover{background:rgba(20,20,22,.75)}.act input{margin:0;accent-color:var(--acc)}.fav input{accent-color:var(--gold)}
.done .seen{background:var(--acc)}#fav .fav{background:var(--gold)}#fav h2 span{border-color:var(--gold)}
.done .inner{box-shadow:none}.done .cover img{filter:grayscale(.7);opacity:.75}.done .body{opacity:.65}
.done{margin-top:20px}.done summary{display:inline-block;cursor:pointer;color:var(--mute);font-size:13px;padding:5px 14px;border:1px dashed var(--line);border-radius:999px;list-style:none}
.done summary::-webkit-details-marker{display:none}.done summary::before{content:"▸ "}.done[open] summary::before{content:"▾ "}.done summary:hover{color:var(--acc);border-color:var(--acc)}.done .grid{margin-top:12px}
.hide,.filtered,.sub.empty{display:none!important}
footer{text-align:center;color:var(--soft);font-size:12px;padding:0 16px 40px}
/* 窄屏：目录变成顶部吸顶横条，只列大类 */
@media (max-width:1000px){
 html{scroll-padding-top:112px}
 .layout{display:block;padding:0 16px}
 aside{top:0;z-index:10;max-height:none;margin:0 -16px;padding:10px 16px;background:color-mix(in srgb,var(--bg) 85%,transparent);backdrop-filter:blur(12px);-webkit-backdrop-filter:blur(12px);border-bottom:1px solid var(--line);gap:10px}
 .toc{display:flex;gap:8px;overflow-x:auto;scrollbar-width:none;border:0;margin:0 -16px;padding:0 16px}.toc::-webkit-scrollbar{display:none}
 .grp{display:contents}.kids{display:none!important}
 .toc .l1{flex-shrink:0;margin:0;gap:6px;padding:4px 12px;border:1px solid var(--line);border-radius:999px;background:var(--card);font-size:13px;font-weight:500;white-space:nowrap}
 .toc .l1.on{background:var(--acc);border-color:var(--acc);color:#fff!important}.toc .l1.on small{color:#fff}
}
@media (hover:none){.card::before,.inner::after{display:none}.inner{position:static;height:auto}.vt,.desc{-webkit-line-clamp:unset}}
"""

JS = r"""
// 追剧、看过只存在本机浏览器；看过优先（看完就不再算追剧）
const load=k=>{try{return new Set(JSON.parse(localStorage.getItem(k)||"[]"))}catch(_){return new Set}};
const st={seen:load("seen-v1"),fav:load("fav-v1")},KEYS={seen:"seen-v1",fav:"fav-v1"},TXT={seen:["看过","取消看过"],fav:["追剧","取消追剧"]};
const cards=[...document.querySelectorAll(".card")],total=cards.length,order=new Map(cards.map((c,i)=>[c,i])),home=new Map(cards.map(c=>[c,c.parentElement]));
const favSec=document.getElementById("fav"),favLink=document.getElementById("fav-l");
function place(c){const id=c.dataset.id,h=home.get(c);
 const g=st.seen.has(id)?h.closest("section").querySelector(".done .grid"):st.fav.has(id)?favSec.querySelector(".grid"):h;
 for(const k in st){const on=st[k].has(id);c.querySelector(`.${k} input`).checked=on;c.querySelector(`.${k} span`).textContent=TXT[k][+on]}
 const after=[...g.children].find(x=>order.get(x)>order.get(c));g.insertBefore(c,after||null)}
function count(){
 document.querySelectorAll("section:not(#fav)").forEach(sec=>{const n=sec.querySelectorAll(".done .card").length;
  sec.querySelector(".done b").textContent=n;sec.querySelector(".done").classList.toggle("hide",!n)});
 document.querySelectorAll(".sub").forEach(s=>s.classList.toggle("empty",!s.querySelector(".card")));
 const f=favSec.querySelectorAll(".card").length;favSec.querySelector("small").textContent=f;favSec.classList.toggle("hide",!f);
 favLink.classList.toggle("hide",!f);favLink.querySelector("small").textContent=f;
 document.getElementById("stat").textContent=[st.seen.size&&`已看 ${st.seen.size} / ${total}`,f&&`追剧 ${f}`].filter(Boolean).join(" · ")}
cards.forEach(c=>{place(c);for(const k in st)c.querySelector(`.${k} input`).onchange=e=>{
 e.target.checked?st[k].add(c.dataset.id):st[k].delete(c.dataset.id);try{localStorage.setItem(KEYS[k],JSON.stringify([...st[k]]))}catch(_){}place(c);count();cur=null;spy()}});
// 搜索
const q=document.getElementById("q");q.oninput=()=>{const s=q.value.trim().toLowerCase();
 cards.forEach(c=>c.classList.toggle("hide",!!s&&!c.dataset.k.toLowerCase().includes(s)));
 document.querySelectorAll(".sub,section").forEach(x=>x.classList.toggle("filtered",!!s&&!x.querySelector(".card:not(.hide)")));cur=null;spy()};
// 目录跟随滚动：当前所在的大类、小类高亮，顶部进度条显示读到哪
const links=[...document.querySelectorAll(".toc a")],byId=new Map(links.map(a=>[a.getAttribute("href").slice(1),a]));
const targets=[...document.querySelectorAll("main section,main .sub")],prog=document.getElementById("prog"),toc=document.querySelector(".toc");
let cur=null;
function spy(){const narrow=innerWidth<=1000,y=narrow?130:60;let sec=null,sub=null;
 for(const t of targets){if(t.offsetParent===null)continue;if(t.getBoundingClientRect().top-y>0)break;t.classList.contains("sub")?sub=t:(sec=t,sub=null)}
 const h=document.documentElement;prog.style.width=(h.scrollTop/(h.scrollHeight-innerHeight)*100||0)+"%";
 const key=(sec&&sec.id)+"|"+(sub&&sub.id);if(key===cur)return;cur=key;
 links.forEach(a=>a.classList.remove("on"));document.querySelectorAll(".grp").forEach(g=>g.classList.remove("open"));
 const a1=sec&&byId.get(sec.id),a2=sub&&byId.get(sub.id);
 if(a1){a1.classList.add("on");a1.parentElement.classList.add("open")}if(a2)a2.classList.add("on");
 const act=narrow?a1:a2||a1;if(!act)return;const r=act.getBoundingClientRect(),p=toc.getBoundingClientRect();
 if(narrow)toc.scrollTo({left:toc.scrollLeft+r.left-p.left-p.width/2+r.width/2,behavior:"smooth"});
 else if(r.top<p.top||r.bottom>p.bottom)toc.scrollTo({top:toc.scrollTop+r.top-p.top-p.height/3,behavior:"smooth"})}
let tick=0;addEventListener("scroll",()=>{if(!tick){tick=1;requestAnimationFrame(()=>{tick=0;spy()})}},{passive:true});addEventListener("resize",()=>{cur=null;spy()});
count();spy();
"""

page = f'''<!doctype html><html lang="zh-CN"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1"><title>AI 剧清单</title><style>{CSS}</style></head><body><div id="prog"></div>
<header class="hero"><h1>AI <i>剧</i>清单</h1><p class="sub-t">{total} 部 · {len(cats)} 大类 {sum(len(s) for _, s in cats)} 小类 · 按 B 站播放量排序 · 点卡片看第一集</p><div id="stat"></div></header>
<div class="layout"><aside><input id="q" type="search" placeholder="搜剧名、标题或 UP 主" aria-label="搜索">
<nav class="toc"><div class="grp"><a class="l1 fav-l hide" id="fav-l" href="#fav">★ 我的追剧<small>0</small></a></div>{"".join(toc)}</nav></aside>
<main><section id="fav" class="hide"><h2><span>我的追剧</span><small>0</small></h2><div class="grid"></div></section>{"".join(secs)}</main></div>
<footer>「追剧」和「看过」只保存在你自己的浏览器里</footer><script>{JS}</script></body></html>'''
open("index.html", "w").write(page)
print(len(fin), "matched")
