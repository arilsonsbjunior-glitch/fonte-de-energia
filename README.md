# Fonte de Energia

Site de notícias de energia (petróleo, gás, luz, hidrogênio e renováveis), resumidas em poucas linhas e sempre com o link da fonte original.

## Como funciona

- `index.html`: o site inteiro (layout, estilo e globo animado).
- `noticias.json`: a lista de notícias. **Só esse arquivo muda no dia a dia.**
- O Netlify publica o site automaticamente a cada alteração neste repositório.

## Formato de cada notícia (`noticias.json`)

```json
{
  "data": "2026-11-17",
  "setor": "gas",
  "titulo": "Título curto, na linguagem do dia a dia",
  "resumo": "Duas ou três frases explicando o fato de forma simples.",
  "destaque": "−32%",
  "legenda": "o que esse número significa, em poucas palavras",
  "fontes": [{ "nome": "eixos", "url": "https://link-da-materia-original" }],
  "video": "",
  "arte": "<path d=\"...\"/>",
  "foto": "https://images.pexels.com/photos/.../pexels-photo-....jpeg?auto=compress&cs=tinysrgb&w=1200",
  "foto_credito": "Pexels",
  "foto_link": "https://www.pexels.com/photo/..."
}
```

- `setor`: `petroleo`, `gas`, `luz`, `hidrogenio` ou `renovaveis`.
- `destaque`: o número principal da notícia (aparece grande na capa colorida).
- `video`: link do vídeo no Instagram/TikTok, quando houver. Vazio mostra "Vídeo em breve".
- `arte`: desenho exclusivo da notícia, em SVG de traço (viewBox 0 0 200 200, sem preenchimento, sem cores, sem texto; só `path`, `circle`, `ellipse`, `rect`). Se ficar vazio, o site usa o desenho padrão do setor.
- `foto`: foto real ilustrativa, só de bancos com licença livre (Pexels, Unsplash, Agência Brasil com crédito, Wikimedia Commons com licença livre). Nunca usar foto da matéria do jornal. O site mostra "Foto meramente ilustrativa · crédito" com link para a página original da foto.
- `foto_credito`: fotógrafo e banco (ex.: "Gabriel Xavier / Unsplash"; no Pexels, se o nome não estiver claro, use "Pexels").
- `foto_link`: página da foto no banco de imagens.
- Se `foto` estiver vazia, a capa usa o desenho (`arte`).
- A ordem é automática pela data; as 3 mais novas viram os destaques do topo.

## Regras de conteúdo

- Todo número precisa estar na fonte citada. Sem fonte, não entra.
- O resumo é escrito com palavras próprias; nunca copiar parágrafos da matéria.
- Não usar fotos ou logos dos veículos.
