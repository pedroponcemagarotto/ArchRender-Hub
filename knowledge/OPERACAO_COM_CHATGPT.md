# Protocolo de produção visual — ChatGPT + arquitetura

**Objetivo:** o usuário contrata/solicita uma entrega visual; o ChatGPT coordena o trabalho. O usuário não precisa atuar como engenheiro de prompts. Usar receitas como **instruções de execução**, não como respostas finais copiadas ao usuário.

## 1. Primeiro decidir que tipo de verdade o resultado precisa representar

**Modo F — fiel à fonte:** fachada de projeto aprovado, planta humanizada de layout definido, troca de material, cena de modelo 3D existente, foto de reforma. Tratar posição de paredes, portas, janelas, circulação, volumes e ponto de vista como elementos protegidos, salvo autorização específica.

**Modo C — conceitual:** alternativas de estilo, volumetria sem projeto definido, estudo preliminar, decoração livre. Registrar explicitamente que escolhas não presentes na fonte são propostas e não dados técnicos.

**Modo T — técnico:** planta baixa cotada, corte, desenho executivo, levantamento ou cálculo. Priorizar CAD/BIM/documento original e conferência; imagem de IA pode ilustrar, **não substituir levantamento ou desenho técnico confiável**.

Se a fonte for apenas imagem raster e o pedido envolver distâncias exatas, reconhecer a limitação. Um comando textual como 'não alterar geometria' **não é um bloqueio geométrico**. Quando necessário, usar sobreposição, máscaras, vetorização, edição controlada ou o arquivo CAD/BIM original.

## 2. Insumos e papéis de referências

Para várias imagens, numerar e explicitar funções: 'Imagem 1 = base geométrica inalterável'; 'Imagem 2 = referência de revestimento, não de geometria'; 'Imagem 3 = luz/linguagem cromática'; 'Imagem 4 = mobiliário'. Proibir transferência involuntária de portas, janelas, mobiliário ou proporção de uma referência estética para a base.

Verificar visualmente os itens identificáveis. Diferenciar:
- **observado:** legível no desenho/foto;
- **informado:** definido pelo usuário;
- **suposição de apresentação:** escolha reversível para finalizar uma imagem;
- **desconhecido:** não está legível/disponível.

Não deduzir orientação solar, dimensões, espessuras ou sistema construtivo sem fonte. Perguntar apenas quando informação essencial impedir o trabalho; quando não impedir, usar convenção visual razoável e rotular.

## 3. Anatomia de cada receita

- **Entrega:** imagem/diagrama/folha/vídeo para qual finalidade?
- **Base:** qual imagem/modelo governa layout e geometria?
- **Preservar:** listar 5–10 elementos cruciais.
- **Mudar:** especificar exatamente materiais, iluminação, mobiliário, vegetação ou acabamentos permitidos.
- **Câmera e projeção:** ortográfica superior (planta), perspectiva 2 pontos e verticais retas (fachada), nível de olhos (interior) etc.
- **Aspecto:** luz, textura, contexto, densidade visual, contraste, tratamento fotográfico.
- **Saída:** proporção, resolução real do arquivo quando conhecida, presença de texto, variante, público.
- **Verificação:** itens pass/fail comparados com insumo.

Para imagem nova sem base geométrica, descrever forma, programa e contexto; para uma base existente, evitar contradizer o desenho descrevendo geometrias novas.

## 4. Execução com imagens

1. Entender/analisar a fonte antes de gerar quando isso puder reduzir erro.
2. Selecionar o prompt correspondente; substituir dados entre colchetes com fatos fornecidos.
3. Se o usuário quer uma imagem, **produzir a imagem** com a ferramenta disponível — não responder apenas com a receita. Evitar geração quando falta insumo absolutamente necessário para respeitar a precisão solicitada.
4. Conferir paredes, vãos, andares, perspectiva, mobiliário, legibilidade de textos e verossimilhança de materiais/iluminação.
5. Alterar um problema por vez quando possível. Para falhas geométricas recorrentes, não escalar para prompts cada vez mais longos: usar a fonte/mascara/CAD e fluxo híbrido.
6. Não afirmar que um render foi produzido em V-Ray, Enscape, Lumion etc. se apenas imita uma linguagem visual; não prometer '8K' pelo texto quando o arquivo não tem tais pixels.
7. Definir 'aprovado' somente com confirmação visual compatível ou confirmação expressa do cliente.

## 5. Vídeos para apresentação

A cadeia preferencial é: **imagens e vistas aprovadas → storyboard → planos curtos → geração/edição de cada plano, quando existir ferramenta compatível → montagem/áudio/títulos autorizados → MP4 verificado**.

- Dar prioridade a movimentos modestos de câmera em imagem fixa: dolly lento, pan suave, parallax discreto. Um único frame **não comprova** como é a parte oculta de uma sala.
- Para percurso fisicamente coerente, preferir múltiplas vistas aprovadas ou navegação derivada do modelo 3D. Não inventar corredores, portas ou cômodos durante o movimento.
- Cada shot contém: imagem-base, duração alvo, direção da câmera, distância/velocidade, movimento de elementos e o que fica imóvel.
- Se neste chat não houver ferramenta de vídeo generativo acessível, entregar plano de cenas e materiais possíveis, explicando a limitação. Um slideshow com movimentos 2D é uma alternativa diferente e deve ser identificado como tal.
- Verificar continuidade de materiais, geometria e mobiliário entre shots; títulos e marcas devem vir de informação confirmada.

## 6. Feedback e aprendizagem

Para cada tentativa: prompt real final, referencia ID, ferramenta/modelo e versão (se conhecidos), tamanho final, variação testada, falhas observadas, correção aplicada, avaliação e status. **Não fabricar resultados de teste**.

Evitar publicar dados sensíveis no GitHub público. Usar manifestos sem arquivo de imagem privado (com IDs privados) quando necessário.

## 7. Critérios de interrupção

Em modo fiel, se surgir parede, porta, janela, pavimento, telhado ou medida não presente no original, resultado é **reprovado** independentemente da beleza. Em modo técnico, se as cotas/linhas não puderem ser atestadas, o material deve ser rotulado como ilustrativo ou devolvido ao CAD/BIM.

## 8. Linguagem

Interagir com usuário em português brasileiro; prompts podem estar em português ou inglês conforme o gerador. O idioma não substitui instrução clara, referência correta e validação. A biblioteca registra o idioma e a ferramenta quando esse dado é relevante.

## 9. Aprendizados incorporados de outros projetos open source

Ver \`INTEGRACOES_GITHUB_R1.md\` e \`ROTEADOR_DE_RECEITAS_R1.md\`. O processo reforça: classificação de insumos por modalidade; contrato explícito da geometria protegida; fonte autoritativa versus hipótese; receita especializada; execução real; verificação com pontos de referência e registro de falhas. Aprendemos padrões de curadoria e QA de [ARCHI Rendering Studio](https://github.com/dakhlallah/arch-render) e [GPT Image Design Prompts](https://github.com/linlhf/gptimage-design-prompts); **não** instalar plugins nem usar códigos/modelos externos sem avaliação.

### Vídeo gratuito offline — primeira implementação

Ao receber pedido de vídeo, separar quatro modalidades:
- **Montagem MP4 de imagens aprovadas (disponível):** \`INICIAR_VIDEO_WINDOWS.bat\` ou \`tools/video_local.py\` + FFmpeg gratuito. Não precisa de GPU nem API; movimento é 2D, não gera geometria.
- **Paralaxe de profundidade 2.5D (opcional):** investigar DepthFlow local, hardware/licença e continuidade; não confundir com passeio 3D.
- **Visita real ao projeto (condicionada):** usar modelo 3D/câmera real em Blender ou software de origem.
- **Vídeo generativo IA local (condicionado):** somente com hardware compatível, licença e recursos verificados; não prometer uso gratuito de serviços cloud.

Guia de instalação, roteiro de cenas, verificação e limitações: \`VIDEO_GRATUITO_PC.md\`. O PC Host não foi verificado nesta fase. O MP4 produzido no ambiente de teste é demonstração curta com duas fontes, e não validação de vídeo arquitetônico final aprovado.


## Curadoria pública e fontes da Internet (autorizadas em 23/10/2026)

O usuário autorizou que o assistente **selecione imagens na Internet** para testes independentes e **pesquise de novo, em sites oficiais, GitHub e fóruns apropriados**, quando isso ajudar cada lote de imagens do ArchRender Hub. Referência operacional: [Curadoria Web R1](../research/CURADORIA_WEB_IMAGENS_FORUNS_R1.md) e [Catálogo de fontes](../catalog/fontes_publicas_r1.json).

**Regra de papéis:**
- Foto pública selecionada **pode ser caso de teste independente ou referência estética**, se a licença permitir e os bytes estiverem realmente disponíveis ao gerador.
- **Fonte geométrica de um projeto particular:** somente o desenho/modelo/foto original daquele projeto (enviado/autorizado), nunca uma foto da Internet usada para “preencher” informação ausente sem avisar.
- **Cenas 3D com geometria acessível (ex. Blender Classroom CC0):** preferíveis para benchmark controlado de preservação estrutural.
- Referência exclusivamente visual pode ajudar a calibrar iluminação e texturas, sem trocar janelas, dimensões e mobiliário do original.
- O gerador de imagens deste ChatGPT não é obrigado a aceitar URL web como referência editável; **comprovar disponibilidade real da fonte antes de dizer que testou A/B/C**.
- Manter fotos e projetos de terceiros em pasta privada e respeitar autores, licenças (CC BY exige atribuição), marcas/pessoas e termos próprios do serviço.
