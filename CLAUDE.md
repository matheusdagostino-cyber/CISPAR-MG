# Análise de Edital de Concessão de RSU — Instruções Globais

## Contexto
Repositório com os PDFs de um edital de concessão de manejo de RSU (edital, minuta de contrato, plano de negócios — PN, caderno de encargos, matriz de riscos, apêndices). As instruções estão em `/agentes/`. Rode um agente por vez, na ordem do `agentes/README.md`.

## Escopo
Pipeline exclusivo para concessão: **comum** (Lei n.º 8.987/1995 — só tarifa de usuário), **patrocinada** (Lei n.º 11.079/2004 — tarifa + contraprestação pública) e **administrativa** (Lei n.º 11.079/2004 — só contraprestação pública). Não cobre contrato comum de serviço sob a Lei n.º 14.133/2021. **Identificar a modalidade no início**, porque parte do catálogo é específica do modelo de remuneração — a patrocinada, por ser híbrida, roda tanto os itens de tarifa quanto os de PPP.

## Princípio da arquitetura
O conhecimento jurídico vive no **catálogo** (`agentes/00_catalogo_vicios.md`) — uma lista fechada e enumerada de vícios recorrentes, cada um já ancorado. Os agentes são **estágios de processo**, não áreas do direito. Isso troca recall por memória-livre (que satisfaz e deixa escapar) por recall por checklist (que verifica item a item).

## Perspectiva
A análise é **sempre** da **proponente / concessionária / impugnante**: o achado interessa na medida em que serve para impugnar o edital, precificar a proposta ou alocar/negociar um risco. Não há variação por lado.

## Os dois crivos (matam ruído — aplicados pelo agente 04)
1. **Crivo de materialidade**: um achado só entra no relatório principal se mudar uma decisão concreta — *impugnar / precificar / alocar-negociar / habilitar-se*. O que não muda decisão (erro gramatical, formatação, campo `[•]` isolado) vai para um apêndice "Menores", listado sem análise.
2. **Crivo de ancoragem**: todo achado material declara sua base — *dispositivo expresso*, *construção interpretativa*, ou, se não houver nenhuma, é marcado como **hipótese a confirmar**. Achado sem âncora normativa E sem cláusula concreta citável não entra no relatório.

> Não classificar a "força" da tese (não usar forte/razoável/arriscada). A ancoragem informa o quanto o achado se sustenta; o veredito é do advogado.

## Os três mecanismos de recall (impedem que escape)
1. **Catálogo fechado** (agente 02) — enumeração exaustiva, veredito obrigatório por item.
2. **Passe de contradições** (agente 03) — confronto sistemático entre documentos; pega o que cai nas costuras dos domínios.
3. **Red-team** (agente 05) — releitura adversarial em busca do que ficou de fora do catálogo e da base.

## Formato de citação
- Legislação: "art. XX, § Y.º, inciso Z, da Lei n.º XXXXX/XXXX"
- TCU: "Acórdão XXXX/XXXX-TCU-Plenário" (ou Câmara) · Súmula XXX/TCU
- STJ: "REsp n.º X.XXX.XXX/UF, Rel. Min. Nome, Xª Turma, j. DD/MM/AAAA"
- Edital: "[Documento], cláusula/item XX"

## Jurisprudência — regras invioláveis
- **NUNCA** fabricar número de acórdão, ementa ou relatoria. Verificar na web antes de citar; não citar julgado com data futura.
- **Fallback de portal indisponível**: se pesquisa.apps.tcu.gov.br ou scon.stj.jus.br não puderem ser acessados/confirmados, dizer isso expressamente e registrar o achado só com sua âncora legal/doutrinária — sem precedente.
- As âncoras do catálogo foram conferidas em fonte oficial (Planalto / TCU / ANA). Ainda assim, confirmar a redação vigente do dispositivo ou precedente antes de uso em peça formal.
- **Jurisprudência estadual por foro**: o catálogo traz âncoras federais (lei + TCU + STJ); o **TCE — e o TCM, onde existir (ex.: TCM-BA, TCM-SP, TCM-RJ, TCM-GO, TCM-PA)** — entra como busca parametrizada pela UF/município da concessão (registrados pelo agente 01), **não** como âncora fixa no catálogo. Buscá-lo ao lado do TCU/STJ. Súmula ou acórdão de TCE de outro estado não vincula o foro do edital.
- **Doutrina**: apenas de acesso aberto (artigos e comentários indexados), sempre com autor e obra; conteúdo atrás de paywall não é acessível por esta interface — sinalizar "verificar na fonte". A doutrina complementa o item onde faltar jurisprudência direta; não forma bloco ou anexo próprio.

## Legislação-base
Lei 14.133/2021 · Lei 8.987/1995 · Lei 11.079/2004 · Lei 11.445/2007 · Lei 14.026/2020 · Lei 12.305/2010 · Decreto 11.599/2023 · IN RFB 1.700/2017 · NR 1/ANA (Res. 79/2021) · NR 13/ANA (Res. 271/2025) · Súmulas TCU.
Lex specialis do contrato: Leis 8.987/1995, 11.079/2004 e 11.445/2007. A Lei 14.133/2021 rege procedimento e habilitação.

## Como usar
`siga agentes/01_base_factual.md` e prossiga na sequência do `agentes/README.md`.
