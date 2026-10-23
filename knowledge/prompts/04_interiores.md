# AR-INT-001 — Interiores fotorrealistas

**Versão:** 1.0 | **Estado:** candidato_nao_testado | **Modo:** F por padrão; C quando redesenho for autorizado.

## Entradas

Imagem 1 = foto, screenshot de modelo ou render base do cômodo. Imagem 2 = paleta/estilo (não geometria), Imagem 3 = móvel específico ou acabamento (não ambiente completo). Indicar claramente quais objetos existentes devem continuar.

## Prompt-mestre

~~~text
TAREFA: Produza uma imagem realista de INTERIOR a partir da Imagem 1 para apresentação de [AMBIENTE: SALA/COZINHA/QUARTO/BANHEIRO/ÁREA GOURMET/OUTRO].

IMUTÁVEIS: a Imagem 1 define a geometria principal e o enquadramento. Mantenha paredes, piso/teto, pé-direito aparente, vãos, portas, janelas, pilares, escadas e elementos embutidos explicitamente preservados. Não alargue o cômodo, não crie aberturas nem altere paredes para melhorar a fotografia.

INTERVENÇÕES PERMITIDAS: [EXEMPLO: acabamentos, marcenaria indicada, iluminação, decoração, estofados]. Manter obrigatoriamente [LISTA DE ITENS FIXOS]. Inserir mobília apenas nos locais com circulação visualmente plausível, sem bloquear portas/janelas/escadas. Não inventar dimensões.

MATERIAIS: pisos [ESPECIFICAÇÃO], paredes [ESPECIFICAÇÃO], marcenaria [ESPECIFICAÇÃO], estofados [ESPECIFICAÇÃO], metais/louças [ESPECIFICAÇÃO]. Rugosidades e reflexos naturais; veios de madeira com escala adequada; juntas e sombras de contato discretas.

ILUMINAÇÃO: luz natural plausível chegando das aberturas existentes e iluminação artificial [TEMPERATURA/ESTILO] compatível com luminárias autorizadas. Destaque profundidade, sensação de conforto e leitura dos acabamentos, sem brilho estourado ou áreas escuras artificiais.

LINGUAGEM FOTOGRÁFICA: editorial de arquitetura e design de interiores, câmera ao nível humano, perspectiva corrigida, verticais retas, enquadramento parecido com a imagem-base, lente moderadamente ampla sem distorções extremas.

CONFERÊNCIA: superfícies, aberturas e elementos fixos devem estar nas mesmas posições da fonte. Espelhos e vidros devem refletir a cena de forma compatível, sem mostrar portas, janelas, pessoas ou móveis inexistentes.

SAÍDA: gere uma única imagem fotorrealista apropriada para [APRESENTAÇÃO/PORTFÓLIO], aspecto [FORMATO], sem texto ou logotipos não solicitados. Faça conferência com a Imagem 1 após gerar.
~~~

## Quando a única fonte for uma planta 2D

Não assumir que a planta define automaticamente altura de janelas, volumetria completa, eletrodomésticos ou materiais. A perspectiva 3D será **proposta ilustrativa** até receber cortes, elevações, fotografias ou modelo. Registrar escolhas inventadas como hipóteses.

## Checklist

- [ ] Aberturas e pontos de vista mantidos.
- [ ] Mobiliário compatível com circulação e proporções aparentes.
- [ ] Reflexos e iluminação coerentes.
- [ ] Elementos não autorizados não surgiram no render.

**Fonte:** OpenAI Image prompting, Chaos (interiores/Veras), Google Gemini prompt tips.