# ArchRender Hub — ROADMAP OPERACIONAL INTEGRADO R3

**Atualizado:** 23/10/2026  
**Projeto:** \`pedroponcemagarotto/ArchRender-Hub\`  
**Ramo de trabalho:** \`feat/prompt-system-v1\` · **PR:** [#1 — Draft](https://github.com/pedroponcemagarotto/ArchRender-Hub/pull/1)  
**Decisão central:** primeiro fidelidade arquitetônica; depois aparência fotográfica. Imagem bonita com janela deslocada é REPROVADA.  
**Escopo atual:** imagens arquitetônicas. Vídeos/Enscape são trilha futura, não bloqueiam o método de imagens.  
**Restrições:** sem Incubadora Remote V2, sem GitHub Actions, sem publicação de imagens/dados de clientes, sem assumir GPU/API, sem merge automático em \`main\`.

## A. Arquitetura integrada e REAL estado

| Camada | Recurso integrado | Fonte inspiradora | Entrega verificável | Estado |
| --- | --- | --- | --- | --- |
| **1. Entrada** | Foto, screenshot de Enscape/SketchUp, croqui, planta; classificar modo F/C/T; separar fonte geométrica de referência estética | ARCHI Rendering Studio | \`knowledge/OPERACAO_COM_CHATGPT.md\` e \`templates/BRIEFING.md\` | Documentada |
| **2. Roteador** | Regras determinísticas para escolher uma das 9 receitas; não chamar isso de IA ou classificação visual automática | GPT Image Design Prompts | \`catalog/prompts.json\`, \`knowledge/ROTEADOR_DE_RECEITAS_R1.md\`, \`tools/metodo_integrado.py\` | Código e roteiro, sem análise automática de imagens |
| **3. Execução visual** | ChatGPT gera a imagem referenciada; variantes A, B, C com controles textuais progressivos | ARCHI / GPT Image Design | \`knowledge/prompts/01..09\`, \`research/BENCHMARK_VISUAL_R1.md\` | Prompts candidatos; benchmark ainda não executado |
| **4. Controle geométrico** | Checklist de pontos fixos, câmera, materiais; reprovação por falha crítica; máscaras/linhas/profundidade são opção externa | sd-interior-design / virtual-staging / ARCHI | \`templates/VALIDACAO.md\`, \`tools/metodo_integrado.py\` | Gate humano estruturado; **sem ControlNet/MLSD/Canny/Depth executando** |
| **5. Comparação visual** | Comparador deslizante antes/depois do app V0.1; controle humano de âncoras, sem tratar SSIM como garantia geométrica | visual-comparison | \`static/app.js\` (existente); \`templates/VALIDACAO.md\` | Comparador existente; métricas automatizadas pendentes |
| **6. Registro** | Receitas cadastradas em SQLite local; relatório de execução/QA com ID privado em \`data/\` | ARCHI + benchmark interno | \`app.py\` (existente), \`templates/REGISTRO_EXEMPLO.json\`, \`tools/metodo_integrado.py\` | Biblioteca existe; relatório adicional via CLI, sem banco unificado |
| **7. Vídeos (depois)** | Renders aprovados → storyboard → FFmpeg/DepthFlow → vídeo; modelos generativos quando hardware permitir | DepthFlow + gerador local | \`knowledge/VIDEO_GRATUITO_PC.md\`, \`tools/video_local.py\` | Complemento local opcional; fora da prioridade |

**O que “integrado” significa nesta fase:** documentação autoral, roteamento reproduzível, estrutura de prompts, registro de provas, testes de código. **NÃO** significa que repositórios de terceiros foram clonados, que a geração é invocada automaticamente pelo app, que modelos de IA passaram no benchmark ou que ferramentas de máscara estão disponíveis nativamente no ChatGPT.

## B. Método do primeiro resultado, em 8 ações

1. **Receber referência ORIGINAL e autorização de uso.** Marcar \`ref-01\` = geometria mestre; outros arquivos servem apenas de estilo/material, quando autorizados. Arquivos privados fora do GitHub público.
2. **Inventariar o que é imutável** por inspeção real da imagem — posição e número de paredes/vãos, câmera, corredor, marcenaria, mobiliário fixo. Distinguir \`observado\`, \`informado\`, \`desconhecido\`. **Não inferir dimensões** de pixels.
3. **Escolher uma das 9 receitas** em \`catalog/prompts.json\`. O roteador seleciona o documento, não interpreta pixels sozinho.
4. **Preparar contrato de geração:** tarefa, modo F/C/T, referência, âncoras, alterações autorizadas, materiais, iluminação, câmera e critérios de saída.
5. **Executar A/B/C com o gerador nativo do ChatGPT**, sempre partindo do ORIGINAL, preferencialmente duas repetições por variante e mantendo proporção de saída. Não dizer “mesma seed” quando ela não está exposta.
6. **QA cego em relação a estética:** gate geométrico/câmera primeiro. Se alterou porta, janela ou parede → \`reprovado\`. Depois medir realismo/luz/texturas/artefatos. Documentar resultado e variáveis disponíveis.
7. **Corrigir somente região afetada** com ferramenta nativa quando possível; falhas persistentes → tratamento híbrido CAD/máscara/camada original ou ferramenta externa, **com decisão/autorizações separadas**.
8. **Guardar imagens/resultados privados e registrar conclusão** por método, custo/tempo real, falhas e efeito. Jamais anunciar “aprovado” sem inspeção da saída e decisão compatível do responsável.

## C. Sprint de execução — sem tarefas ficticiamente concluídas

| Ordem | ID | Entrega | Critério de aceite / evidência | Status |
| --- | --- | --- | --- | --- |
| 0 | R3-00 | Confirmar branch, PR Draft, restrições e que \`main\` não mudou | Metadados reais do GitHub antes dos commits | **Revalidado** em 23/10/2026 |
| 1 | R3-01 | Consolidar roadmap rastreável | Este arquivo, links cruzados e convenções de status | **Incorporado na PR #1** |
| 2 | R3-02 | Fazer o roteador de método reproduzível | CLI Python sem bibliotecas extras; \`list\`, \`prepare\`, \`assess\`; relatório privado | **Incorporado como ferramenta isolada**, testar localmente |
| 3 | R3-03 | Testes de regressão do roteador e privacidade | Tests do CLI; nenhuma chamada de rede, sem mudar \`app.py\`/SQLite; nenhum dado sensível público | **Adicionados à PR; ver relatório de validação** |
| 4 | R3-04 | Rodada de cozinha/sala original | 3 variantes × 2 repetições = **6 imagens**, original → saída pareada, 6 registros auditados | **Pendente — 0/6 nesta bateria** |
| 5 | R3-05 | Escolher técnica vencedora por evidência | Comparar taxa de reprovação geométrica, realismo, retrabalho; registrar quem ganha, inclusive A | **Pendente, depende R3-04** |
| 6 | R3-06 | Reproduzir na lavanderia original | Mais 6 imagens auditadas; material e perspectiva preservados | **Pendente — 0/6 nesta bateria** |
| 7 | R3-07 | Homologação por categoria | Fachadas, plantas, croquis e materiais com exemplos autorizados | **Pendente** |
| 8 | R3-08 | Automação geométrica opcional | Comparação por âncoras/silhueta/máscara e benchmark; instalar só se realmente necessário | **Backlog — sem dependência agora** |
| 9 | R3-09 | Integração plena na GUI | Levar seleção/preparo/QA ao \`app.py\`/UI após estabilidade do CLI; persistência segura e migração reversível | **Backlog — app V0.1 preservado** |
| 10 | R3-10 | Vídeos | Retomar com vídeo real de Enscape/Blender, sem comprometer o trabalho de imagens | **Pausado por decisão do usuário** |

### Definição de “concluído”

- **Documentado:** tem especificação, não implica execução.
- **Implementado:** arquivo/função integrada ao ramo, não implica que foi rodada no PC Host.
- **Testado localmente:** ambiente, comando e resultado real registrados.
- **Homologado:** imagem gerada/inspecionada, gate aprovado e método repetível no cenário; cliente aprova entrega quando aplicável.
- **Instalado no PC Host:** somente após confirmação de instalação e testes naquele computador.

## D. Protocolo do piloto de cozinha/sala — AR-BENCH-001

**Imagem mestre:** única referência original do usuário, nunca uma imagem já modificada pela IA. O arquivo **não** será versionado.  
**Modo:** F — fiel, sem redesenho.  
**Inventário preliminar (a verificar visualmente contra o original no início do benchmark):** sofá à esquerda; geladeira inox ao centro; cozinha com armários verde-azulados à direita; bancada clara; bancada/pia, corredor ao fundo, janela de esquadria escura à direita, vegetação decorativa. Não pressupor medidas nem posição exata sem abrir a fonte.

| Variante | Gerador | Instruções | Prova |
| --- | --- | --- | --- |
| A — base | ferramenta nativa disponível do ChatGPT | fotorrealismo + referência original com pouca especificação | observar alterações espontâneas |
| B — receita especializada | mesma ferramenta e original | \`AR-INT-001\` + preservações, luz, materiais, mesma câmera | verificar melhora com prompt |
| C — protocolo completo | mesma ferramenta e original | mesmas restrições + âncoras inspecionadas + execução em modo fiel + QA e correção apenas quando necessária | verificar ganho do fluxo disciplinado |

**Avaliação:** primeiro \`geometria_gate = passou / falhou / nao_verificavel / nao_avaliado\`. Se \`falhou\`, \`aceito=false\` independentemente de nota estética. Se \`nao_verificavel\`, não contar como aprovado. Avaliar realismo com rubrica em \`research/BENCHMARK_VISUAL_R1.md\` **somente após gate**. Registrar parâmetros disponíveis, resolução real e número de tentativas, sem prometer fixação de semente ou controle que o gerador não expõe.

**Proporção & privacidade:** mesma proporção do original quando a ferramenta permitir; não fazer upload público ou transcrever arquivo privado para a PR. Metadados devem ser anonimizados.

### Por que NÃO usar o sd-interior-design ou virtual-staging como motor principal imediatamente?

Esses repositórios usam ecossistema de inferência/segmentação, máscaras e controles (MLSD, Depth, Canny). São úteis quando a IA altera paredes/vãos, mas requerem outro motor/execução real, licenças e requisitos. **O ChatGPT Image nativo não expõe ControlNet nesses mesmos parâmetros.** Portanto: usar os princípios de correção localizada já; avaliar implementação externa só após medir falhas recorrentes.

### Por que o visual-comparison não aprova sozinho?

Diferença de pixels e SSIM podem mudar por luz, material e cor mesmo com geometria correta. O objetivo é comparar âncoras arquitetônicas além do visual; o Hub V0.1 já possui um comparador antes/depois funcional. O SSIM é futuro complemento diagnóstico.

## E. Saídas objetivas que o usuário receberá por lote

1. **Render/artefato** realmente produzido, quando a fonte e ferramenta existirem.
2. **Pareamento de referência × resultado** e observações de alterações concretas.
3. **Planilha ou relatório de QA** (gate, erro, escore, histórico de retrabalho, custo se aplicável).
4. **Versão de prompt** e aprendizado reutilizável, em GitHub sem imagens privadas.
5. **Posição real do roadmap**, citando a etapa atual e pendências; nunca contagem inventada.

## F. Comandos do modo operacional local (sem instalar GPU/Docker)

\`\`\`bash
python tools/metodo_integrado.py list
python tools/metodo_integrado.py prepare --task interiores --variant C \
    --reference-id ref-cozinha-001 \
    --preserve "janela preta no lado direito" \
    --preserve "geladeira inox no centro" \
    --change "corrigir apenas luz e textura"
python tools/metodo_integrado.py assess --file data/workflows/<arquivo.json> \
    --geometry passou --camera passou --materials passou --artifacts passou --score 89
python -m unittest discover -s tests -v
\`\`\`

\`prepare\` **não** lê, gera ou edita imagens; apenas prepara contrato/prompt para uso no ChatGPT. Os JSONs gerados ficam em \`data/workflows/\`, ignorada pelo Git. \`assess\` recebe avaliações humanas e **não concede aprovação de cliente automaticamente**.

## G. Referências de implementação

- [Fontes GitHub verificadas](research/PROJETOS_GITHUB_UTEIS_2026-10-23.md)
- [Mapeamento de integrações](knowledge/INTEGRACOES_GITHUB_R1.md)
- [Roteador de receitas](knowledge/ROTEADOR_DE_RECEITAS_R1.md)
- [Protocolo de produção](knowledge/OPERACAO_COM_CHATGPT.md)
- [Portões de qualidade](templates/VALIDACAO.md)
- [Benchmark R1](research/BENCHMARK_VISUAL_R1.md)
- [Prompt System v1](PROMPT_SYSTEM_v1.md)
- [Fluxo de novo chat](INICIAR_NOVO_CHAT.md)

**Continuidade:** não reiniciar pesquisa de ferramentas a cada novo chat. Abrir esta PR, confirmar HEAD, verificar estados e avançar no primeiro item pendente que não dependa de material privado inexistente. **Sem merges e sem ações pagas automáticas.**
