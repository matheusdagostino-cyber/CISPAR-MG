#!/usr/bin/env python3
"""
juris.py — busca de jurisprudência (Tribunais de Contas + Judiciário) em 1 arquivo.
Chaves: lidas de variáveis de ambiente ou de um arquivo .env no diretório atual.
  TCE_API_KEY=lnm_...        (privada — Lei na Mão TCE)
  DATAJUD_APIKEY=...         (pública do CNJ; já vem preenchida no .env de exemplo)

Uso:
  python3 juris.py tce "<termo>" [tribunal] [limit]   # TCU/TCEs/TCDF  (ex.: tcu, tce-mg, tce-sc)
  python3 juris.py datajud <alias> "<assunto>" [size]  # Judiciário     (ex.: stj, tjmg, trf1)
  python3 juris.py teor "<url>"                         # baixa e extrai o INTEIRO TEOR (verbatim)
"""
import os, sys, json, urllib.parse, urllib.request, urllib.error

def key(name, default=""):
    v = os.environ.get(name, "").strip()
    if not v and os.path.exists(".env"):
        for ln in open(".env", encoding="utf-8"):
            if ln.strip().startswith(name + "="):
                v = ln.split("=", 1)[1].strip(); break
    return v or default

UA = "Mozilla/5.0 (juris.py)"

def tce(q, tribunal=None, limit=10):
    base = "https://tce.leinamao.com.br/api/v1/decisions"
    p = {"q": q, "limit": limit}
    if tribunal: p["tribunal"] = tribunal
    url = base + "?" + urllib.parse.urlencode(p)
    req = urllib.request.Request(url, headers={"Authorization": f"Bearer {key('TCE_API_KEY')}",
                                               "Accept": "application/json", "User-Agent": UA})
    data = json.load(urllib.request.urlopen(req, timeout=45)).get("data", [])
    print(f"[TCE] {len(data)} resultado(s) para '{q}'" + (f" em {tribunal}" if tribunal else ""))
    for it in data:
        tr = (it.get("tribunals") or {}).get("name", "—")
        s = (it.get("ai_summary") or "")[:500]
        print(f"\n• {tr} · {it.get('type')} n.{it.get('number')}/{it.get('year')} · {it.get('session_date')} · Rel. {it.get('rapporteur') or '—'}")
        print(f"  Assunto: {it.get('subject')}")
        print(f"  Resumo (provedor — NÃO literal): {s}")
        if it.get("cited_laws"): print(f"  Leis: {', '.join(it['cited_laws'][:6])}")
        if it.get("source_url"): print(f"  Inteiro teor: {it['source_url']}")

def datajud(alias, assunto, size=10):
    url = f"https://api-publica.datajud.cnj.jus.br/api_publica_{alias}/_search"
    body = {"size": int(size), "query": {"match_phrase": {"assuntos.nome": assunto}},
            "sort": [{"dataAjuizamento": {"order": "desc"}}]}
    req = urllib.request.Request(url, data=json.dumps(body).encode(),
        headers={"Authorization": f"APIKey {key('DATAJUD_APIKEY')}", "Content-Type": "application/json"})
    hits = json.load(urllib.request.urlopen(req, timeout=45)).get("hits", {}).get("hits", [])
    print(f"[DataJud/{alias}] {len(hits)} processo(s) — assunto '{assunto}' (metadados; sem ementa)")
    for h in hits:
        s = h["_source"]; ass = "; ".join(a.get("nome", "") for a in s.get("assuntos", []))
        print(f"\n• {s.get('numeroProcesso')} | {s.get('classe', {}).get('nome')} | {s.get('orgaoJulgador', {}).get('nome', '')}")
        print(f"  assuntos: {ass[:160]} | ajuizado: {str(s.get('dataAjuizamento',''))[:8]}")

def teor(url):
    import re
    try:
        import fitz
    except ImportError:
        sys.exit("Instale: pip install pymupdf")
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    open("/tmp/_juris.pdf", "wb").write(urllib.request.urlopen(req, timeout=60).read())
    t = "\n".join(p.get_text() for p in fitz.open("/tmp/_juris.pdf"))
    t1 = re.sub(r"\s+", " ", t)
    m = re.search(r"EMENTA(.*?)(ACÓRDÃO|RELAT[ÓO]RIO|Vistos|É o relat)", t1, re.S | re.I)
    print((m.group(1).strip() if m else t[:3000]))

if __name__ == "__main__":
    a = sys.argv[1:]
    if not a: print(__doc__); sys.exit(0)
    if a[0] == "tce":      tce(a[1], a[2] if len(a) > 2 else None, int(a[3]) if len(a) > 3 else 10)
    elif a[0] == "datajud":datajud(a[1], a[2], a[3] if len(a) > 3 else 10)
    elif a[0] == "teor":   teor(a[1])
    else: print(__doc__)
