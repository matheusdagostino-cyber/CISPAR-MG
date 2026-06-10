#!/usr/bin/env python3
"""
Consulta dirigida à API "Lei na Mão TCE" (Portal do Desenvolvedor).
Base: https://tce.leinamao.com.br/api/v1  |  Auth: Authorization: Bearer lnm_...

A chave é lida de:
  1) variável de ambiente TCE_API_KEY; ou
  2) arquivo .env no diretório atual (linha TCE_API_KEY=...).
A chave NUNCA é impressa, logada ou versionada (.env está no .gitignore).

Uso:
  python3 consulta_tce.py                 # valida e roda o conjunto de buscas dirigidas
  python3 consulta_tce.py "q livre" --tribunal tce-mg --limit 20
Saída: imprime na tela e grava jurisprudencia_tce.md
"""
import os, sys, json, time, urllib.parse, urllib.request, urllib.error

BASE = "https://tce.leinamao.com.br/api/v1"

def load_key():
    k = os.environ.get("TCE_API_KEY", "").strip()
    if not k and os.path.exists(".env"):
        for line in open(".env", encoding="utf-8"):
            line = line.strip()
            if line.startswith("TCE_API_KEY=") and not line.startswith("#"):
                k = line.split("=", 1)[1].strip().strip('"').strip("'")
                break
    return k

def mask(k):
    return (k[:12] + "…") if k and len(k) > 12 else "(vazia)"

def call(path, params=None, key=None, timeout=30):
    url = f"{BASE}/{path}"
    if params:
        url += "?" + urllib.parse.urlencode({k: v for k, v in params.items() if v is not None})
    req = urllib.request.Request(url, headers={
        "Authorization": f"Bearer {key}",
        "Accept": "application/json",
        "User-Agent": "cispar-juris-check/1.0",
    })
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            body = r.read().decode("utf-8", "replace")
            return r.status, (json.loads(body) if body.strip() else {})
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", "replace") if e.fp else ""
        try:
            body = json.loads(body)
        except Exception:
            pass
        return e.code, body
    except Exception as e:
        return None, f"ERRO DE REDE: {e}"

def extract_items(payload):
    """Normaliza formatos comuns de resposta."""
    if isinstance(payload, list):
        return payload
    if isinstance(payload, dict):
        for k in ("data", "results", "decisions", "items", "decisoes"):
            if isinstance(payload.get(k), list):
                return payload[k]
    return []

def field(it, *names):
    for n in names:
        if isinstance(it, dict) and it.get(n) not in (None, ""):
            return it[n]
    return "—"

def fmt_item(it):
    """Formata uma decisão no schema real da API (data[]): tribunals{code,name},
    number, year, session_date, type, rapporteur, subject, ai_summary, cited_laws, source_url."""
    if not isinstance(it, dict):
        return f"- {it}"
    tr   = it.get("tribunals") or {}
    trib = tr.get("name") or tr.get("code") or "—"
    num  = it.get("number", "—"); year = it.get("year", "")
    tipo = it.get("type", "")
    rel  = it.get("rapporteur") or "—"
    data = it.get("session_date", "")
    subj = (it.get("subject") or "")[:180]
    summ = it.get("ai_summary") or ""
    if len(summ) > 500:
        summ = summ[:500] + "…"
    laws = ", ".join((it.get("cited_laws") or [])[:6])
    url  = it.get("source_url") or ""
    out = f"- **{trib} · {tipo} n.{num}/{year}** · {data}" + (f" · Rel. {rel}" if rel != "—" else "")
    if subj: out += f"\n  - Assunto: {subj}"
    if summ: out += f"\n  - Resumo (provedor — NÃO literal): {summ}"
    if laws: out += f"\n  - Leis citadas: {laws}"
    if url:  out += f"\n  - Fonte (inteiro teor): {url}"
    return out

# Buscas dirigidas para fechar as pendências de confirmação da análise CISPAR.
QUERIES = [
    ("Atestado/parcela de maior relevância (50%)", {"q": "atestado capacidade técnica parcela maior relevância", "type": "acordao"}),
    ("Atestado acima de 50% — restrição", {"q": "atestado quantitativo superior 50% restrição competitividade"}),
    ("Concessão de RSU / manejo de resíduos", {"q": "concessão manejo resíduos sólidos urbanos"}),
    ("Cofaturamento / tarifa de resíduos na conta de água", {"q": "cofaturamento tarifa resíduos sólidos conta de água"}),
    ("Prazo de concessão x amortização", {"q": "prazo concessão amortização investimentos justificativa"}),
    ("Reequilíbrio / fluxo de caixa marginal", {"q": "reequilíbrio econômico-financeiro fluxo de caixa marginal concessão"}),
    ("Parcelamento do objeto (Súmula 247)", {"q": "parcelamento do objeto adjudicação por item"}),
    ("Capital social x garantia (cumulatividade)", {"q": "capital social mínimo garantia cumulativa habilitação"}),
    ("Outorga fixa em concessão", {"q": "outorga fixa concessão custeio poder concedente"}),
    ("Matriz de riscos / inadimplência do usuário", {"q": "matriz de riscos inadimplência usuário concessão"}),
]
# Foros de interesse (None = todos). Ajustar 'tce-mg' ao código real visto em /tribunals.
TRIBUNAIS = [None, "tce-mg", "tcu"]

def main():
    key = load_key()
    if not key or "COLE_O_RESTANTE" in key or key.endswith("xxxx"):
        print("⚠️  Chave ausente/placeholder. Defina TCE_API_KEY (env) ou edite .env.")
        print(f"    Valor atual: {mask(key)}")
        sys.exit(2)
    print(f"🔑 Chave carregada: {mask(key)}")

    # Modo ad-hoc: python3 consulta_tce.py "termo" [--tribunal x] [--limit n]
    args = sys.argv[1:]
    if args and not args[0].startswith("-"):
        q = args[0]
        trib = None; lim = 20
        if "--tribunal" in args: trib = args[args.index("--tribunal")+1]
        if "--limit" in args: lim = int(args[args.index("--limit")+1])
        st, pl = call("decisions", {"q": q, "tribunal": trib, "limit": lim}, key)
        print(f"HTTP {st}")
        items = extract_items(pl)
        print(f"{len(items)} resultado(s)")
        for it in items: print(fmt_item(it)); print()
        if not items: print(json.dumps(pl, ensure_ascii=False, indent=2)[:1500])
        return

    # 1) Validação
    st, stats = call("stats", key=key)
    print(f"GET /stats -> HTTP {st}")
    if st == 200:
        print("  ", json.dumps(stats, ensure_ascii=False)[:300])
    elif st in (401, 403):
        print("  ❌ Autenticação/plano recusado. Verifique a chave/plano. Resposta:", str(stats)[:300]); sys.exit(1)
    st, tribs = call("tribunals", key=key)
    print(f"GET /tribunals -> HTTP {st}")
    trib_items = extract_items(tribs) or (tribs if isinstance(tribs, list) else [])
    if trib_items:
        codes = [field(t, "codigo", "code", "id", "sigla") for t in trib_items][:60]
        print("  Tribunais:", ", ".join(str(c) for c in codes))

    # 2) Buscas dirigidas
    out = ["# Jurisprudência TCE/TCU — consulta dirigida (API Lei na Mão)\n",
           f"_Gerado em {time.strftime('%Y-%m-%d %H:%M')} — chave {mask(key)}_\n"]
    for titulo, params in QUERIES:
        out.append(f"\n## {titulo}\n")
        for trib in TRIBUNAIS:
            p = dict(params); p["tribunal"] = trib; p.setdefault("limit", 10)
            st, pl = call("decisions", p, key)
            items = extract_items(pl)
            tag = trib or "todos"
            line = f"\n### [{tag}] HTTP {st} — {len(items)} resultado(s)\n"
            out.append(line); print(line.strip())
            if st == 429:
                out.append("_Rate limit — aguardando 60s_\n"); time.sleep(60)
                st, pl = call("decisions", p, key); items = extract_items(pl)
            for it in items[:10]:
                out.append(fmt_item(it) + "\n")
            if st != 200 and not items:
                out.append(f"_resposta: {str(pl)[:300]}_\n")
            time.sleep(0.7)  # cortesia ao rate limit
    open("jurisprudencia_tce.md", "w", encoding="utf-8").write("\n".join(out))
    print("\n✅ Resultados gravados em jurisprudencia_tce.md")

if __name__ == "__main__":
    main()
