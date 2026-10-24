# Método R2 — Visualização arquitetônica de alto padrão usando ChatGPT

**Data:** 23/10/2026 | **Estado:** protocolo de produção derivado de evidências, ainda não validado por testes locais.  
**Não usar:** Incubadora Remote V2, GitHub Actions, publicação de mídia confidencial em repositório público.  
**Responsabilidade:** ChatGPT conduz análise, direção visual, preparação e geração com ferramenta de imagem disponível; pessoa usuária confirma o conceito/projeto.

## A regra número 1

**Preservar o projeto é um objetivo diferente de criar uma imagem atraente.** A apresentação final precisa das duas coisas. Quando não for possível verificar geometria, marcar como conceito ilustrativo, mesmo que o render tenha aparência profissional.

## Modos de operação

| Modo | Pode variar | Deve permanecer | Formato mais seguro |
| --- | --- | --- | --- |
| F1 — planta humanizada fiel | texturas leves, paleta, sombra, mobiliário já conhecido | planta 2D, vãos, divisórias, rótulos reais | sobreposição sobre desenho original, preferencialmente vetorial |
| F2 — fachada/modelo existente | materiais, céu, vegetação permitida, luz | contorno, volumes, pavimentos, vãos, câmera | editar screenshot/render base, não criar do zero |
| F3 — interior existente/modelado | tecidos, revestimento, decoração autorizada, luz | paredes, esquadrias, circulação, ponto de vista | edição regional / imagem-para-imagem |
| C — conceitual | massa, estilo e layout conforme briefing | restrições explicitamente confirmadas | criação livre, rotular conceito |
| T — técnico | cores e anotação editorial com verificação | cotas, escala, dimensões, símbolos documentais | CAD/PDF vetorial/SVG; não confiar em raster gerado |
| V — apresentação em vídeo | movimento e enquadramento, dentro do visível | materiais/forma da cena aprovada | cenas curtas de imagens aprovadas; vídeo só se modelo disponível |

## Etapa 0 — Auditoria dos insumos ANTES de renderizar

1. Analisar cada arquivo como prova, não como inspiração livre. Separar **Imagem 1 — geometria**, **Imagem 2 — material**, **Imagem 3 — atmosfera**, **Imagem 4 — objeto específico** quando houver.
2. Escrever inventário visual: perímetro, número de níveis, aberturas por fachada, escada, acessos, móveis preservados, cômodos identificáveis, perspectiva.
3. Assinalar "observado", "informado", "hipótese" ou "desconhecido". Não inventar norte, dimensão, espessura, altura de pé-direito, normas técnicas ou materiais especificados.
4. Definir contrato mínimo: "proteger X", "pode mudar Y", "a imagem final destina-se a Z".

## Etapa 1 — Bloquear estrutura pelo método possível

**Se houver CAD/BIM ou PDF vetorial:** manter a geometria e exportar vista/passe de linhas/camadas. Para planta humanizada, preferir composição: base vetorial imutável por cima, humanização em áreas internas, legendas originais conservadas.

**Se houver screenshot de SketchUp/Revit/Rhino:** manter mesma vista e proporção, usar como entrada para o gerador com instruções explícitas de câmera/vãos e acabamento; se possível, ter um clay render/sombra ou outra vista.

**Se só houver foto/croqui raster:** pedir edição limitada; geometria rigorosa e vista inédita não estão garantidas. Um mapa de contornos criado por pós-processamento comum ajuda na verificação e sobreposição, mas **não é ControlNet** dentro da geração nativa.

**Se for projeto sem fonte:** criar uma **proposta conceitual** e rotular como tal.

## Etapa 2 — Direção de arte: os 7 controles de qualidade

1. **Composição:** posição/altura de câmera, horizonte, corte, verticalidade; fachada em dois pontos, planta em ortográfica superior, interior com verticais retas.
2. **Materialidade:** especificar materiais reais por área (microtextura, acabamento fosco/brilhante, juntas, veios da madeira, rugosidade plausível). Evitar "materiais nobres" genéricos e misturar muitos estilos.
3. **Luz:** horário, céu, direção observável da luz, proporção natural/artificial, reflexos compatíveis, exposição; pode testar luz de manhã difusa antes de pôr do sol dramático.
4. **Ótica:** lente moderada, sem grande angular extrema, profundidade de campo suficientemente ampla para leitura do projeto.
5. **Escala:** pessoas, carros, vasos e mobiliário coerentes e discretos; não bloquear fachada ou acesso.
6. **Imperfeições controladas:** textura de pedra e concreto, leve variação natural de folhagem/veios, mas sem "ruído" que encubra desenho.
7. **Pós-produção:** contraste natural, correção de brancos, redução de artefatos, nitidez comedida, conferência da dimensão final do arquivo.

Esses são critérios de **arte e fotografia**, não parâmetros físicos comprovados do gerador. "V-Ray", "Enscape", "Corona", "8K" e "ultrarrealismo" são etiquetas de estilo e não executam aqueles motores.

## Etapa 3 — Gerar com prompt separado em quatro camadas

A. **O que produzir** (um render, planta ou folha; público e finalidade).  
B. **O que deve ficar igual** (enumerar vãos/volumes/perímetro/ambientes).  
C. **O que está autorizado mudar** (acabamento, iluminação, vegetação etc.).  
D. **Como fotografar e avaliar** (câmera, luz, materiais, enquadramento, checklist).

Quando a imagem de referência já define forma/ângulo, priorizar acabamento e luz, não tentar reescrever a geometria inteira. Usar frases diretas, evitando contradições e palavras vazias. As receitas em knowledge/prompts/ são ponto de partida; os modelos R2 estão em [PROMPTS](PROMPTS_CHATGPT_R2.md).

## Etapa 4 — Avaliar ANTES de mostrar como resultado final

- Exibir lado a lado fonte × saída.
- Conferir portas, janelas, escadas, quantidade de cômodos, pavimentos, circulações e perímetro.
- Conferir textura, reflexo de vidro/espelho, exposição, sombra, escala do mobiliário, verticalidade e repetição artificial.
- Para texto/cota, conferir caractere a caractere com a fonte ou inserir vetor/texto original na montagem final.
- Classificar **reprovado** se diferença de geometria em Modo F ou T, independentemente da beleza.
- Registrar dificuldade e correção; não afirmar "100% igual" sem verificação real.

## Etapa 5 — Corrigir localmente, não fazer loteria textual

Primeiro diferenciar: erro local em textura/objeto → edição focada; erro em linhas/aberturas → voltar à base geométrica, compor camadas ou restringir escopo; erro global de iluminação → mudar uma variável; vista inédita inconsistente → exigir outra câmera do modelo ou rotular conceitual.

Regra: limitar ciclos de regeneração completa a **duas tentativas iniciais por abordagem**; se as duas alterarem geometria crítica, mudar técnica, não acrescentar adjetivos ao prompt. Esse limite é recomendação operacional nossa, não número fornecido pelas fontes.

## Etapa 6 — Entrega com qualidade declarada

- Identificar se "render conceitual" ou "representação fiel à referência com revisão visual".
- Fornecer formato e dimensão **real** do arquivo; DPI só quando tiver sentido e for verificado.
- Não prometer render 4K/8K se pixel count é menor; upscale conserva aparência mas pode fabricar/alterar detalhe.
- Para impressão, preferir escala vetorial do desenho original com humanização como camada, e verificar tamanho final do papel.

## Vídeo — tratamento diferente

**Imagem aprovada → storyboard → plano curto → animação/geração → montagem e conferência.** Se houver várias cenas e modelo 3D, preferir exportar várias vistas consistentes. De um frame único não é possível provar o corredor atrás da porta nem uma órbita completa da fachada.

Cada plano especifica **movimento de câmera e tempo**, não reconta os objetos. Preferir: plano fixo com folhagem leve, zoom/dolly sutil, pequena panorâmica. Montagem de foto com movimento 2D é válida como apresentação, **não deve ser rotulada walkthrough 3D**. A capacidade atual de gerar vídeo generativo precisa ser conferida a cada chat; o uso do ChatGPT como roteirista não implica modelo de vídeo disponível.

## História da qualidade / aprendizagem

Por tentativa: categoria, contrato geométrico, fontes (IDs privados), prompt final, alteração, modelo/versão conhecida, resolução real, tempo/custo conhecido ou "não disponível", falhas, parecer crítico e aprovação. Para repositório **público**, somente metadados anonimizados. Nunca imagens, plantas e vídeos de cliente.

## Limite honesto

A combinação de prompt + ferramenta de imagem + pós-produção **pode** atingir aparência muito próxima a renders premium em determinadas imagens estáticas, mas isso não equivale a geometria exata, consistência de múltiplas câmeras, iluminação fisicamente simulada, navegação 3D ou documentação técnica de V-Ray/Corona/Enscape/D5. Precisamos demonstrar capacidade real por benchmark — ver [plano](BENCHMARK_VISUAL_R1.md).