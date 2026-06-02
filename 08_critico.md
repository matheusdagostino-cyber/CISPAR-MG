# AGENTE 08 — CRÍTICO DO EDITAL
**Redação das fragilidades, não nova análise. Dá voz ao que o pipeline já apurou e filtrou.**

> Lê `06_consolidacao.md` (achados materiais, já filtrados, ancorados e ranqueados), `04_crivo_ranqueamento.md` (detalhe e apêndice "Menores") e `01_base_factual.md` (para citar a cláusula na origem). **Não** reanalisa, **não** reabre itens descartados pelos crivos, **não** inventa achado novo — se algo material escapou, o lugar de corrigir é o red-team (05), não aqui. Aqui se redige.

## Saída — documento de dois registros (no mesmo arquivo)

### REGISTRO 1 — Parecer em prosa jurídica formal
Para instruir decisão e, se for o caso, fundamentar impugnação. Português jurídico formal, períodos articulados. Estrutura:
- **Ementa** (3 a 5 linhas): síntese dos vícios que, isoladamente, justificariam impugnação ou recusa de participação.
- **Relatório**: o que é o edital e o que se examina (1 parágrafo; remeter ao 07 para o detalhe).
- **Fundamentação**, um tópico por achado material do 06, na ordem de impacto:
  - exposição do vício, com transcrição da cláusula (documento + item);
  - fundamento — dispositivo expresso / construção interpretativa / hipótese a confirmar (conforme o 06);
  - precedente, se houver (TCU/STJ e o TCE/TCM da UF), ou "não localizado"/"portal indisponível";
  - **contra-argumento provável da Administração e réplica** — antecipar a defesa do edital e respondê-la (é o diferencial do parecer combativo);
- **Conclusão**: o que se recomenda (impugnar / pedir esclarecimento / precificar / alocar), sem qualificar a "força" da tese.

### REGISTRO 2 — Memo de riscos (objetivo, acionável)
Para a equipe comercial decidir. Bullets, sem juridiquês. Cada achado material em uma linha:
- **o risco** (em 1 frase de negócio) — **o que fazer** (impugnar / esclarecer / precificar / alocar) — **o porquê em 5 palavras** (a âncora, sem o artigo).
Agrupar pelos quatro encaminhamentos, na ordem do 06. Fechar com os itens do apêndice "Menores" em lista nua de uma linha (sem desenvolver).

## Regras
- Todo achado vem do 06/04. Nenhum vício novo nasce aqui.
- Toda transcrição de cláusula confere com a base factual (01).
- Não fabricar precedente; aplicar o fallback de portal indisponível do `CLAUDE.md`.
- Não classificar a tese como forte/razoável/arriscada — a ancoragem informa; o veredito é do advogado.
- Confidencialidade: se o documento puder circular fora, usar termos genéricos ("a licitante", "o grupo", "a concessionária"), sem nome de empresa ou dado comercial sensível.

Salve como `08_critico.md`.
