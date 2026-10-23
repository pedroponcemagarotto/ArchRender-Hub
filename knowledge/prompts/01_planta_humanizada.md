# AR-PLAN-HUM-001 — Planta humanizada fiel

**Versão:** 1.0 | **Estado:** candidato_nao_testado | **Modo:** F — fidelidade a layout aprovado.  
**Entrega:** imagem de planta humanizada ortográfica, apresentação ao cliente sem redefinir o projeto.

## Insumos

- **Imagem 1 (obrigatória):** planta base legível, idealmente exportada de CAD/BIM em alta resolução.
- **Imagem 2 (opcional):** paleta/moodboard de revestimentos; tem papel apenas estético.
- **Briefing:** funções dos ambientes, se confirmadas; texto/cotas a manter; mobiliário autorizado.

## Prompt-mestre — adaptar e executar com a imagem anexa

~~~text
TAREFA: Gere uma imagem de PLANTA HUMANIZADA para apresentação arquitetônica a partir da Imagem 1. Ela é a referência geométrica prioritária e representa o layout a respeitar. Não crie uma planta diferente.

LEITURA DA BASE: Antes de desenhar, identifique visualmente perímetro, divisórias, portas com sentidos de abertura visíveis, janelas, circulação, escadas, áreas molhadas e eventual mobiliário existente. Dados ilegíveis ou ausentes não são autorização para modificar o desenho.

IMUTÁVEIS: mantenha o traçado, o número e a posição dos ambientes, espessuras relativas de paredes, aberturas, pilares, escadas, níveis indicados e a relação espacial. Não acrescente divisórias, portas, janelas, novos cômodos, circulação ou cotas inventadas. Preserve a organização visual e a orientação da folha.

MUDANÇAS AUTORIZADAS: aplique materiais de piso compatíveis com [MATERIAIS CONFIRMADOS], texturas discretas, vegetação decorativa apenas em locais livres apropriados e mobiliário exclusivamente onde o programa e o desenho permitirem. Se os usos dos ambientes não estão claros, mantenha a apresentação neutra em vez de inventar cozinha, quarto ou banheiro.

PROJEÇÃO: planta rigorosamente vista de cima, projeção ortográfica, sem inclinação isométrica, sem paredes erguidas e sem perspectiva 3D. Materiais legíveis com sombras de contato muito suaves, textura na escala visual coerente, boa distinção entre ambientes, paredes e mobiliário.

LINGUAGEM: apresentação arquitetônica contemporânea, editorial, profissional, cores naturais, contraste de desenho suficientemente forte para manter portas, paredes e vãos identificáveis. Evite texturas que escondam linhas.

TEXTOS: somente palavras confirmadas e legíveis na Imagem 1 ou no briefing. Se não houver segurança na escrita de cotas e legendas, prefira produzir a humanização sem rótulos novos; não invente números, áreas ou nomes.

SAÍDA: uma única planta completa, enquadramento central, sem cortes do perímetro e sem artefatos, no aspecto [PROPORÇÃO/FORMATO]. Gere efetivamente a imagem. Depois, compare visualmente com a base e aponte qualquer divergência geométrica observável.
~~~

## Variação controlada

Uma segunda versão pode mudar apenas paleta de pisos, densidade da textura ou estilo de mobiliário **sem modificar a geometria**. Mantenha a mesma Imagem 1 e orientação; se o modelo deslocar paredes, voltar à fonte.

## Portão de qualidade

- [ ] Perímetro e quantidade de ambientes coincidem.
- [ ] Portas/janelas/escadas nas mesmas posições.
- [ ] A humanização não ocultou o desenho.
- [ ] Nenhuma medida foi inventada.
- [ ] Projeção estritamente superior, sem profundidade fictícia.

**Falha crítica:** alteração de parede, abertura, escada ou circulação. Reprovar e reconstruir com abordagem de sobreposição/edição regional, se necessário.

**Fontes dos princípios:** documentação OpenAI de image prompting; Chaos (AI architecture prompts); referências e datas em ../FONTES_E_CURADORIA.md.