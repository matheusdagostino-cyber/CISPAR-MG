# AGENTE 09 — BUSCA DE JURISPRUDÊNCIA (APIs)
**Estágio de apoio: para cada achado material (dos agentes 04/06 ou das rodadas de fragilidades), buscar precedente nas APIs de jurisprudência, confirmar e citar — sem fabricar.**

> Mecanismo de ancoragem jurisprudencial. Não é varredura de vícios (isso é dos agentes 02/03/05); aqui se **confirma** a tese de cada achado já filtrado, com precedente real, respeitando as regras invioláveis do `CLAUDE.md`.

## Regras invioláveis (do CLAUDE.md)
- **NUNCA** fabricar número de acórdão, ementa ou relatoria.
- O campo `ai_summary` da API "Lei na Mão" é **resumo gerado pelo provedor (paráfrase) — NÃO é texto literal**. Para citar *verbatim*, extrair o **inteiro teor** da fonte oficial (`source_url`).
- Confirmar a redação vigente do dispositivo/precedente antes de uso em peça.
- **Fallback de portal indisponível**: se a fonte oficial não puder ser acessada, registrar o achado só com a âncora legal e marcar o precedente "verificar no portal".
- Foro: **TCE-MG** (e TCM, onde existir) ao lado de TCU/STJ. Súmula/acórdão de TCE de outro estado **não vincula** o foro, mas serve de reforço/analogia (sinalizar).

## Pré-requisitos
- `.env` (gitignored) com `TCE_API_KEY=lnm_...` e `DATAJUD_APIKEY=...` (chave pública do CNJ).
- Scripts: `consulta_tce.py` (Tribunais de Contas) e `datajud.py` (Judiciário).
- `pip install pymupdf` para extrair inteiro teor de PDFs.

---

## A. API "Lei na Mão TCE" — Tribunais de Contas (TCU/TCEs/TCDF)
Base `https://tce.leinamao.com.br/api/v1` · Auth `Authorization: Bearer lnm_...` · JSON.
Endpoints: `/stats`, `/tribunals`, `/decisions` (params: `q`, `tribunal` [ex.: `tcu`, `tce-mg`, `tce-sc`], `type` [`acordao`,`sumula`,`parecer`,...], `year_from`, `year_to`, `limit` 1–100, `offset`).
Schema de cada decisão (`data[]`): `tribunals{code,name}`, `number`, `year`, `session_date`, `type`, `rapporteur`, `subject`, **`ai_summary`** (paráfrase), `cited_laws`, **`source_url`** (inteiro teor).

**Comandos:**
```bash
# busca ad-hoc (termo + filtro de tribunal)
python3 consulta_tce.py "atestado parcela de maior relevância" --tribunal tcu --limit 10
python3 consulta_tce.py "capital social garantia habilitação"   --tribunal tce-mg --limit 10
python3 consulta_tce.py "prazo concessão amortização"            --limit 10   # sem filtro = todos

# lote dirigido (valida /stats, lista tribunais e roda o conjunto QUERIES; grava jurisprudencia_tce.md)
python3 consulta_tce.py
```
**Boas práticas de busca:** a busca é *fuzzy* e instável com **multi-termo + filtro de tribunal** (às vezes retorna 0). Prefira **termo curto/forte** e, se preciso, filtre depois. Códigos: minúsculo com hífen (`tce-mg`, `tcu`, `tce-sc`, `tcdf`...). Cobertura do **TCE-MG** é majoritariamente de **Teses/Súmulas** (base mapjuris).

---

## B. API Pública do DataJud (CNJ) — Judiciário (STJ/TJ/TRF/TST...)
Base `https://api-publica.datajud.cnj.jus.br/api_publica_<alias>/_search` · POST (Elasticsearch) · Auth `Authorization: APIKey <chave pública>`.
Cobre o **Judiciário** (NÃO os Tribunais de Contas). Retorna **metadados + movimentos** (classe, `assuntos`, órgão julgador, datas) — **NÃO** a íntegra/ementa.

**Comandos:**
```bash
python3 datajud.py stj  --assunto "Tarifa" --classe "Recurso Especial" --size 10
python3 datajud.py tjmg --assunto "Saneamento" --size 10
python3 datajud.py tjmg --texto "resíduos"   # match em assuntos.nome
```
Use o DataJud para **localizar** leading cases por assunto (ex.: cofaturamento/"venda casada", tarifa de água, concessão de saneamento); o teor obtém-se no site do tribunal pelo número do processo.

---

## C. Extrair o INTEIRO TEOR (texto literal / verbatim)
Quando o achado for ao relatório/peça, baixar o documento de `source_url` e extrair o texto literal:
```bash
# baixa o PDF do inteiro teor (TCE-MS/TCE-SC etc. costumam servir PDF direto)
curl -sSL -A "Mozilla/5.0" -o /tmp/doc.pdf "<source_url>"
python3 - <<'PY'
import fitz, re
t="\n".join(p.get_text() for p in fitz.open("/tmp/doc.pdf"))
m=re.search(r"EMENTA(.*?)(ACÓRDÃO|RELATÓRIO|Vistos)", re.sub(r"\s+"," ",t), re.S|re.I)
print((m.group(1) if m else t[:2000]).strip())
PY
```
> Portais do **TCU** (`pesquisa.apps.tcu.gov.br`, `contas.tcu.gov.br`) são **SPA em JavaScript** e **não** entregam o texto por download direto — confirmar o inteiro teor manualmente no portal e marcar "[confirmar]".

---

## Saída (por achado)
| Achado (origem) | Tese | Âncora legal | Precedente (tribunal · tipo · nº/ano · relator) | Trecho | Status |
|---|---|---|---|---|---|
- **Trecho**: literal (com a fonte oficial) **ou** "resumo do provedor — não literal".
- **Status**: ✅ verbatim oficial · ⚠️ enunciado/secundária a confirmar · ❌ só resumo (portal indisponível) · — sem precedente (só âncora legal).
- Consolidar os literais em `juris_integra.md` (separar oficial × resumo).

---

## Prompt pronto (para lançar como subagente)
```
Você é o AGENTE 09 (busca de jurisprudência). Leia 06_consolidacao.md e
fragilidades_juridicas.md. Para CADA achado material com encaminhamento
"impugnar/esclarecer", busque precedente:
1. Tribunais de Contas: `python3 consulta_tce.py "<termo curto>" --tribunal
   tce-mg|tcu|tce-sc --limit 10`. Priorize TCE-MG (foro) e TCU.
2. Judiciário (se for tese de STJ/TJ — ex.: cofaturamento/venda casada):
   `python3 datajud.py stj --assunto "<assunto TPU>" --size 10`.
3. Para os achados que irão à peça, baixe o source_url e extraia o inteiro
   teor (curl + pymupdf) para citar verbatim.
Regras: não fabricar; ai_summary é paráfrase (não literal); marcar status de
confirmação; aplicar o fallback de portal indisponível; TCE de outro estado é
reforço/analogia, não vincula. Saída no formato da tabela acima; consolidar os
textos literais em juris_integra.md.
```
