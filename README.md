# Agentes de Análise de Edital de Concessão de RSU

Arquitetura por **estágios de processo** (não por área do direito). O conhecimento jurídico vive em `00_catalogo_vicios.md`; os agentes o processam. Desenho voltado a **recall** (não deixar escapar) e **precisão** (não afogar em ruído).

## Uso no claude.ai/code
Um agente por vez. Antes de começar, leia `CLAUDE.md` (perspectiva padrão + os dois crivos + os três mecanismos de recall).

| Ordem | Comando | Função | Output |
|---|---|---|---|
| — | (ler) `agentes/00_catalogo_vicios.md` | Catálogo fechado de 45 vícios ancorados | (dado, não roda) |
| 1 | `siga agentes/01_base_factual.md` | Extração única estruturada de todo o edital | `01_base_factual.md` |
| 2 | `siga agentes/02_varredura_catalogo.md` | Percorre os 45 itens contra a base | `02_varredura_catalogo.md` |
| 3 | `siga agentes/03_contradicoes.md` | Confronto cross-documento (costuras) | `03_contradicoes.md` |
| 4 | `siga agentes/04_crivo_ranqueamento.md` | Crivos de materialidade e ancoragem + ranking | `04_crivo_ranqueamento.md` |
| 5 | `siga agentes/05_redteam_completude.md` | Releitura adversarial: o que escapou? | `05_redteam_completude.md` |
| 6 | `siga agentes/06_consolidacao.md` | Consolidação por ação (insumo dos agentes 07 e 08) | `06_consolidacao.md` |
| 7 | `siga agentes/07_explicador.md` | **Redação**: explica o edital (resumo executivo + seção técnica), neutro | `07_explicador.md` |
| 8 | `siga agentes/08_critico.md` | **Redação**: fragilidades (parecer formal + memo de riscos) | `08_critico.md` |

> 01–06 são **análise**; 07–08 são **redação** sobre o que 01 e 06 já apuraram — não reanalisam nem inventam achado. O explicador é neutro (o que o edital é); o crítico dá voz aos vícios já filtrados.

## Fluxo
```
00 catálogo ─┐
             ▼
01 base ──► 02 varredura ─┐
       └──► 03 contradições ─┴─► 04 crivo ──► 05 red-team ──► 06 consolidação ──► 07 explicador
                                     ▲_____________│ (volta)                  └──► 08 crítico
```
Análise (01–06) é linear: 01 alimenta 02 e 03; ambos alimentam 04; 05 revisa e devolve a 04/06. Redação (07–08) parte do 06: o explicador lê 01+06, o crítico lê 06+04+01. 07 e 08 são independentes entre si.

## Por que mudou (da versão por domínio)
- **Recall**: listas de tópicos abertas faziam o modelo satisfazer e parar. O catálogo fechado força veredito por item; o passe de contradições pega as costuras; o red-team busca o que faltou.
- **Precisão**: os dois crivos (materialidade + ancoragem) ficam num estágio dedicado (04), em vez de cada agente despejar tudo.
- **Reuso**: o conhecimento jurídico virou dado (`00`). Cada edital realimenta o catálogo (etapa 5 do agente 06), então a cobertura melhora a cada rodada.

## Para novo edital
1. Repositório privado no GitHub; copie `CLAUDE.md` e `agentes/`.
2. Suba os PDFs e rode 01→08 (ou pare no 06, se só quiser a análise sem os documentos redigidos).
3. Vários editais no mesmo repo: prefixe os outputs com a sigla do edital.
