#!/usr/bin/env python3
"""
Cliente da API Pública do DataJud (CNJ).
Base: https://api-publica.datajud.cnj.jus.br/api_publica_<alias>/_search  (POST, Elasticsearch)
Auth: header  Authorization: APIKey <chave pública do CNJ>

IMPORTANTE:
- Cobre o Judiciário (STJ, TJs, TRFs, TST, TSE, TJMs...). NÃO cobre Tribunais de Contas (TCE/TCU).
- Retorna METADADOS processuais e MOVIMENTOS (classe, assuntos, órgão julgador, datas),
  NÃO a íntegra/ementa das decisões. Use para LOCALIZAR processos; o teor fica no site do tribunal.

A chave é lida de DATAJUD_APIKEY (env) ou do .env; há fallback para a chave pública do CNJ.

Uso:
  python3 datajud.py tjmg --assunto "Saneamento" --size 10
  python3 datajud.py stj  --assunto "Tarifa" --classe "Recurso Especial" --size 5
  python3 datajud.py tjmg --texto "resíduos"            # match em assuntos.nome
"""
import os, sys, json, urllib.request, urllib.error

BASE = "https://api-publica.datajud.cnj.jus.br"
# Chave PÚBLICA oficial do CNJ (não é segredo).
PUBLIC_KEY = "cDZHYzlZa0JadVREZDJCendQbXY6SkJlTzNjLV9TRENyQk1RdnFKZGRQdw=="

def load_key():
    k = os.environ.get("DATAJUD_APIKEY", "").strip()
    if not k and os.path.exists(".env"):
        for line in open(".env", encoding="utf-8"):
            if line.startswith("DATAJUD_APIKEY="):
                k = line.split("=", 1)[1].strip()
                break
    return k or PUBLIC_KEY

def search(alias, body, timeout=45):
    url = f"{BASE}/api_publica_{alias}/_search"
    req = urllib.request.Request(url, data=json.dumps(body).encode("utf-8"),
        headers={"Authorization": f"APIKey {load_key()}", "Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return r.status, json.loads(r.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode("utf-8", "replace")[:400]
    except Exception as e:
        return None, str(e)[:400]

def build_query(assunto=None, classe=None, texto=None, ano_from=None, ano_to=None, size=10):
    must = []
    if assunto: must.append({"match_phrase": {"assuntos.nome": assunto}})
    if classe:  must.append({"match_phrase": {"classe.nome": classe}})
    if texto:   must.append({"match": {"assuntos.nome": texto}})
    q = {"match_all": {}} if not must else {"bool": {"must": must}}
    body = {"size": size, "query": q, "sort": [{"dataAjuizamento": {"order": "desc"}}]}
    return body

def fmt(hit):
    s = hit.get("_source", {})
    ass = "; ".join(a.get("nome", "") for a in s.get("assuntos", []))
    movs = s.get("movimentos", [])
    ult = ""
    if movs:
        m = sorted(movs, key=lambda x: x.get("dataHora", ""))[-1]
        ult = f"{m.get('nome','')} ({str(m.get('dataHora',''))[:10]})"
    d = str(s.get("dataAjuizamento", ""))
    d = f"{d[6:8]}/{d[4:6]}/{d[0:4]}" if len(d) >= 8 else d
    return (f"• {s.get('numeroProcesso')} | {s.get('tribunal')} {s.get('grau','')} | "
            f"{s.get('classe',{}).get('nome')} | {s.get('orgaoJulgador',{}).get('nome','')}\n"
            f"   assuntos: {ass[:180]}\n"
            f"   ajuizado: {d} | último movimento: {ult}")

def main():
    if len(sys.argv) < 2:
        print(__doc__); sys.exit(0)
    alias = sys.argv[1].lower()
    a = sys.argv[2:]
    def opt(name, default=None):
        return a[a.index(name)+1] if name in a else default
    body = build_query(
        assunto=opt("--assunto"), classe=opt("--classe"), texto=opt("--texto"),
        ano_from=opt("--ano-from"), ano_to=opt("--ano-to"),
        size=int(opt("--size", "10")))
    st, res = search(alias, body)
    print(f"POST /api_publica_{alias}/_search -> HTTP {st}")
    if not isinstance(res, dict):
        print(res); return
    total = res.get("hits", {}).get("total", {})
    hits = res.get("hits", {}).get("hits", [])
    print(f"total: {total.get('value')} ({total.get('relation')}) | exibindo {len(hits)}\n")
    for h in hits:
        print(fmt(h)); print()

if __name__ == "__main__":
    main()
