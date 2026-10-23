# AR-CORR-001 — Correção localizada sem refazer todo o render

**Versão:** 1.0 | **Estado:** candidato_nao_testado.

## Objetivo

Após gerar uma imagem, comparar com a fonte e corrigir **uma divergência por vez**. Se o gerador continuar alterando a geometria, voltar à entrada original e adotar método híbrido com máscara/composição ou base CAD/BIM. Nunca declarar a correção sem conferir.

## Caso A — janela/porta que sumiu ou foi inventada

~~~text
Corrija somente a região [DESCREVER REGIÃO] do RESULTADO ATUAL usando a IMAGEM ORIGINAL DO PROJETO como referência geométrica mandatória. Restaure exatamente o número, a posição, os contornos e as proporções visíveis de portas/janelas do original. Preserve todos os outros pixels/elementos sempre que possível: materiais, luz, câmera e paisagismo. Não adicione esquadrias decorativas nem reformule a fachada. Compare a região corrigida ao original.
~~~

## Caso B — paredes e circulação modificadas na planta

~~~text
O resultado anterior divergiu da planta original. Retome a PLANTA ORIGINAL como geometria prioritária, não a imagem alterada como única fonte. Corrija o contorno de [PAREDE/PASSAGEM/PORTA] para a posição e ligação exatas da fonte. Mantenha vista superior ortográfica e não altere os demais ambientes. Se a edição por IA não conseguir manter linhas fiéis, pare e indique necessidade de edição vetorial/sobreposição em vez de inventar solução.
~~~

## Caso C — revestimento aplicado no lugar errado

~~~text
Na Imagem 1, o material [NOVO REVESTIMENTO] deve ocupar somente a área [ÁREA ALVO]. Remova o novo revestimento de [SUPERFÍCIE INCORRETA] e restaure ali o acabamento da imagem original. Mantenha geometria, composição, iluminação e mobiliário da Imagem 1. Se houver máscara disponível, limite estritamente as alterações às duas regiões citadas.
~~~

## Caso D — imagem artificial, vidro espelhado errado ou luz exagerada

~~~text
Melhore apenas o realismo de superfície da imagem atual: reduza brilho plástico e saturação exagerada, recupere reflexos de vidro ambientalmente coerentes e sombras naturais proporcionais às aberturas/fontes existentes. Preserve exatamente os volumes, materiais especificados, posição dos objetos e enquadramento. Não criar novos elementos nem novo estilo.
~~~

## Caso E — texto incorreto na prancha

**Regra:** nomes de ambientes e cotas são informação técnica. Preferir transcrever do original usando montagem/editoração vetorial com revisão de caracteres. Se a IA continuar errando texto, **não insistir**: gerar camada visual sem texto e inserir rótulos verificados posteriormente.

## Caso F — vídeo deforma o ambiente

~~~text
Regere apenas este shot, partindo da imagem aprovada do quadro inicial. Reduza a amplitude do movimento de câmera para um deslocamento mínimo e constante. Mantenha portas, janelas, mobiliário, linhas de paredes, materiais e proporções estáveis ao longo do tempo. Evite movimento que revele faces e cômodos não documentados. Compare frame inicial, médio e final com a referência.
~~~

## Checklist por iteração

1. Qual divergência exata foi observada? Citar região e imagem original.
2. A mudança solicitada tem máscara/região definida? Se não, risco maior de drift.
3. O resultado conserva as partes fora do alvo?
4. A nova tentativa melhorou a métrica afetada sem criar outra falha?
5. Registrar o prompt de correção real, referências e comparação.

**Recomendação:** guardar falhas também. Uma receita sem exemplos negativos pode parecer universal e não é. Seguir templates/VALIDACAO.md para os portões de aprovação.