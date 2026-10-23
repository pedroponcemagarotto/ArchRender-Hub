# AR-VIDEO-001 — Vídeo de apresentação arquitetônica

**Versão:** 1.0 | **Estado:** candidato_nao_testado | **Modalidade:** image-to-video quando ferramenta disponível; alternativa = animação editorial de imagens aprovadas.

## Princípio central

O ChatGPT prepara imagens-base, define shots, constrói prompts de movimento e, **se a ferramenta de geração/edição de vídeo estiver disponível neste contexto**, executa e verifica o vídeo. Não presumir que produzir um prompt equivale a gerar MP4. Não alegar vídeo generativo se só foi feita apresentação de imagens com zoom/pan.

Para vídeo de arquitetura, shots individuais curtos são preferíveis a um prompt único que inventa um passeio completo. Modelo generativo a partir de única imagem não conhece ambientes fora do quadro.

## Insumos

- Imagens/renderizações **já aprovadas**, uma base visual para cada plano.
- Tipo de projeto, ordem da narrativa, restrições arquitetônicas e autorização para mostrar pessoas, mobiliário ou vizinhança.
- Duração total [30–60 segundos como sugestão editorial, não regra], formato [16:9 ou 9:16], idioma e texto exato.
- Trilha/licença, logomarca e dados de cliente — somente se fornecidos/autorizados; não publicar no GitHub público.

## Shot 1 — fachada, dolly-in discreto (5–8 s)

~~~text
Use a IMAGEM DE FACHADA APROVADA como primeiro frame e fonte visual. Vídeo arquitetônico realista, shot único e suave. A câmera faz um dolly-in lento, aproximadamente ao longo do eixo do olhar, com parallax discreto e verticais arquitetônicas estáveis. Luz, materiais, portas, janelas, muros, número de pavimentos e paisagismo permanecem coerentes com a imagem-base. Árvores podem oscilar levemente ao vento; pessoas/veículos só se existirem na referência ou forem explicitamente permitidos. Manter composição elegante e movimento contínuo, sem transformação da edificação. Duração alvo [6 s].
~~~

## Shot 2 — perspectiva externa de detalhe (5–8 s)

~~~text
Use a IMAGEM APROVADA DE DETALHE EXTERNO como base exclusiva. A câmera realiza deslocamento lateral lento e curto, apenas o bastante para enfatizar a textura de [REVESTIMENTO] e profundidade da fachada. Preserve esquadrias, ripados, juntas, guarda-corpos, volumes, reflexos e bordas existentes; o movimento não deve exigir mostrar superfícies ocultas que não aparecem em referências adicionais. Luz suave [HORÁRIO], movimento estável, aparência de filme arquitetônico. Duração alvo [6 s].
~~~

## Shot 3 — interior, pan controlado (5–8 s)

~~~text
Use a IMAGEM APROVADA DO INTERIOR como primeiro frame. Travelling/pan horizontal sutil, na altura dos olhos, dentro do campo de informação realmente mostrado pela referência. Manter paredes, vãos, mobiliário, marcenaria e posição das luminárias inalterados. Sombras delicadas e reflexos coerentes; movimento leve de cortina/planta apenas se fizer sentido. Não abrir novas vistas por portas ou janelas, não inventar cômodos conectados. Duração alvo [6 s].
~~~

## Storyboard sugerido — 36 segundos

| Tempo editorial | Fonte necessária | Movimento | Objetivo |
| --- | --- | --- | --- |
| 0–6 s | Fachada hero aprovada | Dolly-in lento | Identidade do projeto |
| 6–12 s | Outro ângulo exterior aprovado | Pan curto | Volumetria |
| 12–18 s | Detalhe de materiais aprovado | Parallax discreto | Acabamentos |
| 18–24 s | Sala/cozinha aprovada | Pan suave | Experiência interna |
| 24–30 s | Área externa/paisagismo aprovado | Plano quase fixo | Relação com entorno |
| 30–36 s | Fachada ou composição final aprovada | Movimento mínimo | Encerramento e título na edição |

**Atenção:** não criar uma nova perspectiva a partir de uma única fachada sem geometria adicional verificável; se só existir um quadro, usar movimento 2D sutil com transparência sobre a limitação. Cada cena gerativa pode precisar de múltiplas tentativas e verificação quadro a quadro.

## Instrução do diretor para o ChatGPT

~~~text
Prepare a apresentação de vídeo a partir somente das imagens arquitetônicas aprovadas. Liste primeiro os shots e suas referências, depois elabore prompts individuais com movimento de câmera, velocidade e elementos imóveis. Preserve o desenho construído e a identidade de materiais entre shots. Se houver ferramenta de vídeo disponível, produza os takes e monte um MP4 verificado. Se não houver, informe a limitação e ofereça storyboard, sequência de frames ou montagem animada de imagens estáticas claramente identificada. Não afirmar sucesso sem arquivo de saída verificado.
~~~

## Revisão de produção

- [ ] Existe uma imagem aprovada para cada plano.
- [ ] Não ocorreu deformação, mutação de esquadrias/móveis ou abertura inventada.
- [ ] Continuidade visual: materiais, clima, orientação da luz e escala.
- [ ] Resolução e duração reais do MP4 conferidas após render/edição.
- [ ] Título/logo/créditos corretos; trilha com licença adequada.
- [ ] Método de produção devidamente identificado.

**Fontes:** Runway Gen-4/Gen-4.5 prompting; links em ../FONTES_E_CURADORIA.md. Esses guias orientam escrita de movimento, não garantem que o ChatGPT desta sessão acesse Runway nem qualquer outro modelo de vídeo.

## Variante AR-VIDEO-FREE-001 — Vídeo gratuito com FFmpeg no PC

**Status:** implementado como pipeline opcional e avaliado em um teste manual curto no ambiente de desenvolvimento; não validado no PC Host. Esta variante **não depende de modelo generativo**. Usar somente imagens aprovadas, preferencialmente várias perspectivas reais de um mesmo projeto.

**Execução Windows:** abrir \`INICIAR_VIDEO_WINDOWS.bat\`, escolher imagens PNG/JPG, ordenar, selecionar 720p para protótipo e 1080p para entrega quando recursos forem suficientes, duração de 4–6 s por imagem e movimento \`auto\` (sutil). Gerar MP4. Se quiser título/logotipo/trilha própria ou licenciada, finalizar no Shotcut.

**Execução CLI:**
~~~bat
py -3 tools\video_local.py -o "D:\ArchRender\Videos\apresentacao.mp4" --size 720p --seconds 5 --transition dissolve "D:\ArchRender\fachada.png" "D:\ArchRender\sala.png"
~~~

**Verificação:** reproduzir início/meio/final; conferir os metadados de duração/FPS/resolução do MP4, pontos de geometria das imagens aprovadas, cortes que omitam elementos críticos, continuidade de estilo e ausência de trilha não licenciada.

**Próximos modos:** DepthFlow para paralaxe 2.5D e Blender com modelo 3D autorizado. LTX Desktop só após confirmação da GPU/RAM/espaço e licença; proibir API paga no modo gratuito. Documentação: \`../VIDEO_GRATUITO_PC.md\`.
