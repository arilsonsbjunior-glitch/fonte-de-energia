#!/usr/bin/env python3
"""Gera uma página própria para cada notícia em n/<slug>/index.html.

Cada página tem a prévia para WhatsApp/redes (Open Graph), o resumo, a capa
e o botão para a matéria original. Rode sempre depois de mexer no noticias.json:

    python3 gerar_paginas.py
"""
import html
import json
import os
import re
import shutil
import unicodedata

RAIZ = os.path.dirname(os.path.abspath(__file__))
SETORES = {
    "petroleo": ("Petróleo", "#3b2bff", "#ffffff"),
    "gas": ("Gás", "#ff5a1f", "#ffffff"),
    "luz": ("Luz", "#ffd400", "#0d0d10"),
    "hidrogenio": ("Hidrogênio", "#00c2d8", "#0d0d10"),
    "renovaveis": ("Renováveis", "#19c37d", "#0d0d10"),
}
MESES = ["janeiro", "fevereiro", "março", "abril", "maio", "junho", "julho",
         "agosto", "setembro", "outubro", "novembro", "dezembro"]


def slugify(texto):
    t = unicodedata.normalize("NFD", texto).encode("ascii", "ignore").decode()
    t = re.sub(r"[^a-zA-Z0-9]+", "-", t.lower()).strip("-")
    return t[:70].rstrip("-")


def data_longa(iso):
    a, m, d = iso.split("-")
    return f"{int(d)} de {MESES[int(m) - 1]} de {a}"


def e(t):
    return html.escape(str(t or ""), quote=True)


def pagina(n, relacionadas):
    nome, cor, txt = SETORES[n["setor"]]
    fonte = n["fontes"][0]
    extras = "".join(
        f'<a class="btn ghost" href="{e(f["url"])}" target="_blank" rel="noopener">Ver também: {e(f["nome"])} ↗</a>'
        for f in n["fontes"][1:])
    video = (f'<a class="btn ghost" href="{e(n["video"])}" target="_blank" rel="noopener">▶ Ver o vídeo</a>'
             if n.get("video") else "")
    opiniao = (f'<section class="leitura"><h2>Minha leitura</h2><p>{e(n["opiniao"])}</p></section>'
               if n.get("opiniao") else "")
    if n.get("foto"):
        capa_fundo = f'<img class="photo" src="{e(n["foto"])}" alt="" onerror="this.remove()"><span class="tint"></span>'
        capa_cls = "cover has-photo"
        credito = (f'<a class="credit" href="{e(n.get("foto_link") or n["foto"])}" target="_blank" rel="noopener">'
                   f'Foto meramente ilustrativa · {e(n.get("foto_credito") or "banco de imagens")}</a>')
    else:
        capa_fundo = (f'<span class="art"><svg viewBox="0 0 200 200" fill="none" stroke="currentColor" stroke-width="3" '
                      f'stroke-linecap="round" stroke-linejoin="round">{n.get("arte", "")}</svg></span>')
        capa_cls = "cover"
        credito = ""
    rel = "".join(
        f'<a class="rel" href="../{r["slug"]}/"><span class="rel-tag" style="--c:{SETORES[r["setor"]][1]}">'
        f'{SETORES[r["setor"]][0]}</span><b>{e(r["titulo"])}</b><span class="rel-d">{data_longa(r["data"])}</span></a>'
        for r in relacionadas)
    titulo_og = f'{n["titulo"]} | Fonte de Energia'
    og_img = (f'<meta property="og:image" content="{e(n["foto"])}">\n'
              f'<meta name="twitter:image" content="{e(n["foto"])}">') if n.get("foto") else ""
    return f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(titulo_og)}</title>
<meta name="description" content="{e(n['resumo'])}">
<meta property="og:type" content="article">
<meta property="og:site_name" content="Fonte de Energia">
<meta property="og:locale" content="pt_BR">
<meta property="og:title" content="{e(titulo_og)}">
<meta property="og:description" content="{e(n['resumo'])}">
{og_img}
<meta name="twitter:card" content="summary_large_image">
<meta property="article:published_time" content="{e(n['data'])}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Anton&family=Instrument+Sans:wght@400;500;600;700&display=swap" rel="stylesheet">
<style>
:root {{ --ink:#0d0d10; --muted:#62626e; --line:#e8e8ee; --soft:#f5f5f8; --c:{cor}; --t:{txt};
  --fd:"Anton","Impact","Arial Narrow",sans-serif; --fb:"Instrument Sans",system-ui,-apple-system,"Segoe UI",sans-serif; color-scheme: light; }}
* {{ box-sizing: border-box; }} html, body {{ margin: 0; }}
body {{ background:#fff; color:var(--ink); font-family:var(--fb); font-size:17px; line-height:1.6; -webkit-font-smoothing:antialiased; }}
a {{ color:inherit; text-decoration:none; }}
:focus-visible {{ outline:3px solid var(--ink); outline-offset:3px; border-radius:6px; }}
.top {{ border-bottom:1.5px solid var(--ink); }}
.top .w {{ display:flex; align-items:center; justify-content:space-between; gap:12px; padding-top:14px; padding-bottom:12px; }}
.logo {{ font-family:var(--fd); font-size:26px; text-transform:uppercase; line-height:1; }}
.logo span {{ color:transparent; -webkit-text-stroke:1.2px var(--ink); }}
.back {{ font-size:14px; font-weight:600; }}
.w {{ width:100%; margin:0 auto; padding-left:clamp(16px,3.2vw,56px); padding-right:clamp(16px,3.2vw,56px); }}
.cover {{ position:relative; overflow:hidden; border-radius:20px; background:var(--c); color:var(--t); aspect-ratio:21/8; min-height:380px; max-height:72vh;
  display:flex; flex-direction:column; justify-content:space-between; padding:28px 32px; margin-top:22px; container-type:inline-size; }}
.cover > * {{ position:relative; z-index:1; }}
.cover > .photo {{ position:absolute; inset:0; z-index:0; width:100%; height:100%; object-fit:cover; filter:saturate(.85); }}
.cover > .tint {{ position:absolute; inset:0; z-index:0; background:linear-gradient(180deg,rgba(0,0,0,0) 30%,rgba(0,0,0,.5) 62%,rgba(0,0,0,.9) 100%); }}
.cover > .art {{ position:absolute; z-index:0; right:-2%; bottom:-6%; width:50%; aspect-ratio:1; opacity:.24; }}
.cover > .art svg {{ width:100%; height:100%; }}
.cover.has-photo {{ color:#fff; background:#111; }}
.row {{ display:flex; justify-content:space-between; align-items:center; gap:10px; font-size:12px; font-weight:700; letter-spacing:.1em; text-transform:uppercase; }}
.has-photo .row {{ text-shadow:0 1px 8px rgba(0,0,0,.7); }}
.tag {{ background:var(--c); color:var(--t); padding:3px 10px; border-radius:999px; text-shadow:none; }}
.num {{ font-family:var(--fd); font-size:clamp(56px,12cqi,170px); line-height:.9; white-space:nowrap; }}
.cap {{ margin-top:8px; font-size:14px; font-weight:500; opacity:.92; max-width:36ch; }}
h1 {{ font-family:var(--fd); font-weight:400; text-transform:uppercase; font-size:clamp(34px,4.4vw,72px); line-height:1; margin:0 0 12px; max-width:20ch; }}
.corpo {{ display:grid; grid-template-columns:minmax(0,1fr) minmax(280px,380px); gap:clamp(32px,5vw,80px); margin-top:30px; align-items:start; }}
.corpo aside {{ position:sticky; top:24px; }}
.meta {{ font-size:14px; color:var(--muted); display:flex; flex-wrap:wrap; gap:6px 14px; }}
.meta b {{ color:var(--c); filter:brightness(.8); }}
.resumo {{ font-size:19px; line-height:1.6; margin:20px 0 0; max-width:62ch; }}
.leitura {{ margin-top:24px; padding:18px 20px; background:var(--soft); border-left:4px solid var(--c); }}
.leitura h2 {{ margin:0 0 6px; font-size:13px; letter-spacing:.1em; text-transform:uppercase; }}
.leitura p {{ margin:0; }}
.acoes {{ display:flex; flex-wrap:wrap; gap:10px; margin-top:28px; }}
.btn {{ display:inline-flex; align-items:center; gap:8px; padding:12px 20px; border-radius:999px; font-weight:700; font-size:15px; border:1.5px solid var(--ink); background:var(--ink); color:#fff; cursor:pointer; font-family:inherit; }}
.btn.ghost {{ background:#fff; color:var(--ink); }}
.btn.zap {{ background:#25d366; border-color:#25d366; color:#06311a; }}
.credit {{ display:block; margin-top:14px; font-size:12px; color:var(--muted); }}
.aviso {{ margin-top:26px; font-size:13px; color:var(--muted); border-top:1px solid var(--line); padding-top:14px; }}
.mais {{ margin:0 0 60px; }}
.mais h2 {{ font-family:var(--fd); font-weight:400; text-transform:uppercase; font-size:26px; margin:0 0 14px; border-bottom:1.5px solid var(--ink); padding-bottom:8px; }}
.rel {{ display:grid; gap:4px; padding:14px 0; border-bottom:1px solid var(--line); }}
.rel b {{ font-size:17px; line-height:1.25; }}
.rel:hover b {{ text-decoration:underline; text-underline-offset:3px; }}
.rel-tag {{ font-size:11px; font-weight:700; letter-spacing:.08em; text-transform:uppercase; color:var(--ink); display:inline-flex; align-items:center; gap:6px; }}
.rel-tag::before {{ content:""; width:8px; height:8px; border-radius:50%; background:var(--c); }}
.rel-d {{ font-size:13px; color:var(--muted); }}
@media (max-width:900px) {{ .corpo {{ grid-template-columns:minmax(0,1fr); }} .corpo aside {{ position:static; }} .mais {{ margin-top:20px; }} }}
@media (max-width:600px) {{ .logo {{ font-size:22px; }} .back {{ font-size:13px; white-space:nowrap; }} .cover {{ aspect-ratio:4/5; min-height:0; max-height:none; padding:18px; }} .num {{ font-size:clamp(56px,22cqi,120px); }} .resumo {{ font-size:17.5px; }} .btn {{ width:100%; justify-content:center; }} }}
</style>
</head>
<body>
<header class="top"><div class="w">
  <a class="logo" href="../../">Fonte <span>de</span> Energia</a>
  <a class="back" href="../../">← Início</a>
</div></header>
<main class="w">
  <div class="{capa_cls}">
    {capa_fundo}
    <div class="row"><span class="tag">{nome}</span><span>{e(fonte['nome'])}</span></div>
    <div><div class="num">{e(n.get('destaque'))}</div><div class="cap">{e(n.get('legenda'))}</div></div>
  </div>
  {credito}
  <div class="corpo"><article>
  <h1>{e(n['titulo'])}</h1>
  <div class="meta"><b>{nome}</b><span>{data_longa(n['data'])}</span><span>Fonte: {e(fonte['nome'])}</span></div>
  <p class="resumo">{e(n['resumo'])}</p>
  {opiniao}
  <div class="acoes">
    <a class="btn" href="{e(fonte['url'])}" target="_blank" rel="noopener">Ler a matéria completa na {e(fonte['nome'])} ↗</a>
    {extras}{video}
    <button class="btn zap" type="button" id="compartilhar">Compartilhar</button>
  </div>
  <p class="aviso">Este é um resumo com palavras próprias. A matéria original pertence a {e(fonte['nome'])}.</p>
  </article>
  <aside><section class="mais"><h2>Mais notícias</h2>{rel}</section></aside>
  </div>
</main>
<script>
document.getElementById("compartilhar").addEventListener("click", async () => {{
  const url = location.href, titulo = {json.dumps(n['titulo'])};
  try {{ if (navigator.share) {{ await navigator.share({{ title: titulo, url }}); return; }} }} catch (err) {{ return; }}
  window.open("https://wa.me/?text=" + encodeURIComponent(titulo + " " + url), "_blank");
}});
</script>
</body>
</html>
"""


def main():
    caminho = os.path.join(RAIZ, "noticias.json")
    lista = json.load(open(caminho, encoding="utf-8"))
    usados = set()
    for n in lista:
        if not n.get("slug"):
            base = f'{n["setor"]}-{slugify(n["titulo"])}'
            s, i = base, 2
            while s in usados:
                s, i = f"{base}-{i}", i + 1
            n["slug"] = s
        usados.add(n["slug"])
    lista.sort(key=lambda n: n["data"], reverse=True)
    json.dump(lista, open(caminho, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    open(caminho, "a", encoding="utf-8").write("\n")

    pasta = os.path.join(RAIZ, "n")
    if os.path.isdir(pasta):
        shutil.rmtree(pasta)
    for n in lista:
        mesmo = [r for r in lista if r is not n and r["setor"] == n["setor"]][:2]
        outros = [r for r in lista if r is not n and r not in mesmo][:3 - len(mesmo)]
        d = os.path.join(pasta, n["slug"])
        os.makedirs(d, exist_ok=True)
        open(os.path.join(d, "index.html"), "w", encoding="utf-8").write(pagina(n, mesmo + outros))
    print(f"{len(lista)} páginas geradas em n/")


if __name__ == "__main__":
    main()
