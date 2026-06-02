# AGENTE 02 — VARREDURA POR CATÁLOGO
**Percorre os 45 itens de `00_catalogo_vicios.md` contra a base factual.**

> É o mecanismo de recall nº 1. A diferença para a abordagem antiga: aqui não se "procura problemas" livremente — percorre-se uma lista fechada, com veredito obrigatório por item. Item sem ocorrência é registrado como AUSENTE, não omitido.

## Instruções
Leia `00_catalogo_vicios.md` e `01_base_factual.md`. Para CADA item do catálogo (A1…F4):

| # do catálogo | Veredito (PRESENTE / AUSENTE / N-A) | Documento + cláusula (se PRESENTE) | Transcrição da prova | Âncora normativa (do catálogo: dispositivo expresso / construção interpretativa / hipótese) | Contra-argumento provável da Administração |

Regras:
- Veredito obrigatório em TODOS os itens. Não pular.
- **Filtragem por modalidade**: leia primeiro a modalidade registrada na base factual. Itens marcados *(comum/patrocinada)* ou *(patrocinada/administrativa)* que não correspondam à modalidade do edital recebem veredito **N-A por modalidade** (não AUSENTE). Itens sem marcação valem para as três. Na patrocinada, ambos os conjuntos se aplicam.
- Se PRESENTE, a prova é transcrição literal da base — não paráfrase.
- Não aplicar os crivos de materialidade/ancoragem aqui (isso é do agente 04). Aqui só se constata.
- Pesquisa jurisprudencial: para os itens PRESENTES marcados ⚑, buscar precedente conforme as âncoras — TCU/STJ **e o TCE/TCM da UF da concessão** (registrada pelo agente 01) —, aplicando o fallback de portal indisponível do `CLAUDE.md`. Onde não houver jurisprudência direta, citar doutrina de acesso aberto (autor + obra). Para os demais itens, deixar a busca para a fase de crivo se o achado sobreviver.

Salve como `02_varredura_catalogo.md`.
