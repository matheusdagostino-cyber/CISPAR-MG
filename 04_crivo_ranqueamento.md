# AGENTE 04 — CRIVO E RANQUEAMENTO
**Aplica os dois crivos do `CLAUDE.md`. Mata o ruído antes do relatório.**

> Recebe o material bruto dos agentes 02 e 03 (achados PRESENTES + contradições) e decide o que merece o relatório principal. É aqui que "sobra ruído" é resolvido.

## Instruções
Leia `02_varredura_catalogo.md` e `03_contradicoes.md`. Reúna todos os achados PRESENTES e todas as contradições confirmadas. Para cada um, aplique em sequência:

### Crivo 1 — Materialidade
O achado muda uma decisão concreta?
- **Impugnar** — vício de legalidade;
- **Precificar** — onera a proposta;
- **Alocar/negociar** — matéria de risco/reequilíbrio;
- **Habilitar-se** — afeta a aptidão de participar.

Se NÃO muda nenhuma decisão → mover para o apêndice **"Menores"** (lista nua, sem análise). Os itens da seção F do catálogo caem aqui por padrão, salvo se gerarem efeito jurídico material.

### Crivo 2 — Ancoragem
O achado material tem base?
- *dispositivo expresso* / *construção interpretativa* → mantém;
- sem âncora normativa E sem cláusula concreta citável → marcar **hipótese a confirmar** (não é descartado, mas vai sinalizado).

### Verificação jurisprudencial dos sobreviventes
Para cada achado que passou os dois crivos e ainda não teve precedente buscado no agente 02, buscar agora conforme a âncora — TCU/STJ **e o TCE/TCM da UF da concessão** —, com doutrina de acesso aberto onde faltar jurisprudência direta, aplicando o fallback de portal indisponível do `CLAUDE.md`.

### Ranqueamento
Ordenar os sobreviventes por impacto econômico/jurídico (maior primeiro), dentro de cada tipo de decisão.

## Saída

**Relatório principal** (achados materiais, ranqueados):
| # | Achado | Origem (catálogo / contradição) | Documento + cláusula | Decisão (impugnar/precificar/alocar/habilitar) | Âncora | Precedente (ou "não localizado" / "portal indisponível") | Contra-argumento |

**Apêndice Menores** (lista nua, sem análise).

Salve como `04_crivo_ranqueamento.md`.
