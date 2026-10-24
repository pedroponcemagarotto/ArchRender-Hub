# ArchRender Hub — iniciar um teste em um novo chat

**Versão do guia:** 1.1 (2026-10-23)  
**Repositório oficial:** https://github.com/pedroponcemagarotto/ArchRender-Hub  
**Branch de conhecimento atual:** `feat/prompt-system-v1`  
**PR em revisão:** https://github.com/pedroponcemagarotto/ArchRender-Hub/pull/1

> **Importante:** o GitHub é a base versionada de instruções, templates e aprendizados, mas não substitui o envio de imagens do projeto. Um novo chat não está automaticamente conectado ao histórico completo da conversa anterior. Ler o repositório de novo é parte obrigatória da abertura do trabalho.

## Como o usuário começa

1. Abra um novo chat no ChatGPT com acesso a imagens.
2. Anexe a planta, imagem de fachada, croqui, render ou referência que deseja testar. Não envie dados pessoais ou informações confidenciais para GitHub público.
3. Copie a mensagem abaixo e ajuste a última linha para sua tarefa.
4. Se disponível, conecte/utilize o GitHub no chat para ler os arquivos da branch indicada.
5. Confira a imagem gerada e indique divergências concretas (por exemplo, uma janela extra). O objetivo é gerar a imagem, não só fornecer o prompt.

## Mensagem pronta para copiar no novo chat

~~~text
Vamos continuar o projeto ArchRender Hub.

Use como fonte de trabalho o repositório:
https://github.com/pedroponcemagarotto/ArchRender-Hub

Antes de agir, leia, na branch feat/prompt-system-v1, priorizando a pesquisa R2 e o método atualizado:
0. research/PESQUISA_FORUNS_E_FONTES_2026-10-23.md
0. research/METODO_RENDERS_CHATGPT_R2.md
0. research/PROMPTS_CHATGPT_R2.md
0. research/BENCHMARK_VISUAL_R1.md
1. PROMPT_SYSTEM_v1.md
2. knowledge/OPERACAO_COM_CHATGPT.md
3. templates/VALIDACAO.md
4. catalog/prompts.json
5. a receita em knowledge/prompts/ pertinente à minha solicitação.

A PR de referência é https://github.com/pedroponcemagarotto/ArchRender-Hub/pull/1, ainda em revisão. NÃO considere que os arquivos da PR já estão na main. Se o GitHub não estiver acessível, avise e solicite o conteúdo necessário; não invente que leu os arquivos.

Seu papel é atuar como meu diretor de visualização arquitetônica e EXECUTAR a criação de imagens com os recursos de geração disponíveis, e não apenas entregar prompts. Analise as imagens anexadas, escolha a receita apropriada, atribua papéis às referências, diferencie fatos de hipóteses e use modo F (fiel), C (conceito) ou T (técnico). Preserve geometria, portas, janelas, distribuição e demais restrições conforme o modo, sem afirmar fidelidade dimensional que a IA não pode garantir.

Depois de gerar, compare visualmente com a referência, identifique erros e sugira uma correção localizada. Não classifique como 'aprovado' um resultado que não foi gerado, inspecionado e confirmado. Registre para histórico apenas o método e metadados não confidenciais, em uma branch ou PR separada; não envie plantas, fotos, imagens privadas, nomes de cliente ou vídeos ao repositório público.

Para vídeo, use imagens aprovadas e a receita knowledge/prompts/08_video_apresentacao.md; produza um vídeo somente se realmente houver uma ferramenta compatível, caso contrário esclareça o limite e prepare o storyboard.

Não use a Incubadora Remote V2. Não altere a aplicação Python existente nem habilite GitHub Actions.

Minha tarefa atual: [ESCREVA AQUI: ex. humanizar a planta anexada com piso amadeirado e paredes preservadas; gerar fachada 3D; criar interior; preparar vídeo de apresentação].
~~~

## Como testar o método corretamente

**Teste A — planta humanizada:** anexar planta legível; escolher `knowledge/prompts/01_planta_humanizada.md`; registrar contorno, paredes, portas, janelas e eventuais elementos inventados. Se a saída alterar geometria, marcar **reprovado** e corrigir a técnica, não apenas a descrição textual.

**Teste B — fachada 3D:** anexar screenshot/elevação/modelo; usar `03_fachada_exterior_3d.md`; comparar pavimentos, janelas, portas, volumes e ângulo de câmera. Materiais e luz podem variar se autorizados.

**Teste C — interiores:** anexar foto/render/modelo do ambiente; usar `04_interiores.md`; verificar posição de aberturas, escala visual e itens fixos.

**Teste D — vídeo:** começar por uma ou mais vistas aprovadas; usar `08_video_apresentacao.md`; montar planos curtos e conferir se a ferramenta disponível realmente gera vídeo, distinguindo animação de fotos de vídeo generativo.

## Como registrar um aprendizado

- Usar campos de `templates/REGISTRO_EXEMPLO.json` (preencher dados reais disponíveis, sem fabricar seed/modelo).
- Aplicar portões de qualidade de `templates/VALIDACAO.md`.
- Estados válidos: `candidato_nao_testado`, `testado`, `aprovado_cliente`, `reprovado`, `descontinuado`.
- O repositório **é público**. Não publicar originais, renders de cliente, localização/endereço, logotipos, documentos confidenciais ou qualquer identificação pessoal. Histórico público só com conteúdos seguros e anonimizados; armazenar mídias privadas fora do GitHub público.
- Preferir alteração em branch + PR, mantendo `main` intacta até revisão.
- Registrar tanto sucessos quanto falhas, incluindo qual detalhe do prompt e/ou técnica resolveu o problema.

## Convenção para chats posteriores

Enquanto a PR #1 não for incorporada, utilizar explicitamente a branch `feat/prompt-system-v1`. Quando incorporada à `main`, o novo chat poderá usar `main`, mas deve verificar a revisão efetiva antes de agir. Caso a receita seja alterada, consultar a versão mais recente e não reutilizar cegamente comandos antigos.

## O que não é garantido

- A documentação não cria uma memória permanente automática entre chats.
- Um prompt textual nunca assegura geometria ou medidas exatas; materiais técnicos exigem conferência com CAD/BIM.
- A V0.1 do aplicativo local ainda não gera imagens ou vídeos diretamente; o ChatGPT pode gerar imagens no contexto da conversa com as ferramentas disponíveis.
- Criação de vídeo MP4 depende de acesso a ferramenta de vídeo; ter a receita não equivale a ter esse recurso.


## Atualização R2 — como buscar qualidade profissional

Leia também:
- [Pesquisa de fontes e fóruns (23/10/2026)](research/PESQUISA_FORUNS_E_FONTES_2026-10-23.md)
- [Método R2 voltado ao ChatGPT](research/METODO_RENDERS_CHATGPT_R2.md)
- [Prompts originais R2](research/PROMPTS_CHATGPT_R2.md)
- [Benchmark A/B/C — planejamento](research/BENCHMARK_VISUAL_R1.md)

**Prioridade:** o ChatGPT gera as imagens e conduz os refinamentos, em vez de apenas fornecer prompts. O método de maior qualidade exige preservar a fonte geométrica, especificar materiais/luz/câmera e conferir o resultado. Plantas técnicas precisam usar a geometria vetorial autorizada; renders bonitos com portas ou paredes deslocadas são reprovados. Alguns mecanismos pesquisados (ControlNet/seed/denoise) pertencem a outras ferramentas e não devem ser apresentados como controles disponíveis no gerador nativo do ChatGPT.

A PR #1 segue em revisão. Sem Incubadora, sem GitHub Actions, sem dados privados no GitHub público. Nenhum benchmark ou vídeo generativo foi executado neste trabalho de documentação.


## Repositórios GitHub avaliados (23/10/2026)

Além do Prompt System R2, consulte a [comparação de projetos GitHub e decisão de adoção](research/PROJETOS_GITHUB_UTEIS_2026-10-23.md). O levantamento distingue soluções aplicáveis como **metodologia textual agora** e ferramentas que exigem GPU, Docker, API paga ou automação de navegador.

**Prioridade para novos chats:** aproveitar primeiro os princípios de preservação e QA do ARCHI Rendering Studio e a seleção de receitas do GPT Image Design Prompts. **Não instalar** automaticamente ferramentas de terceiros e não conceder acesso a uma sessão autenticada do navegador sem autorização e revisão de segurança. Continuar produzindo imagens no ChatGPT com os recursos disponíveis. As amostras do usuário são privadas e não devem ser publicadas no GitHub público.


## Complemento de vídeos gratuitos / integrações GitHub (23/10/2026)

Antes de começar um trabalho sobre vídeos, leia \`knowledge/VIDEO_GRATUITO_PC.md\`; para escolha de receitas, leia \`knowledge/ROTEADOR_DE_RECEITAS_R1.md\`; para atribuição e aproveitamento criterioso de projetos externos, leia \`knowledge/INTEGRACOES_GITHUB_R1.md\`.

O modo imediato no Windows é **\`INICIAR_VIDEO_WINDOWS.bat\` + FFmpeg instalado localmente**. Cria MP4 com zoom/pan e transição, sem GPU obrigatória, sem API e sem vídeo IA. O ChatGPT continua gerando as imagens iniciais e acompanhando o storyboard; apenas imagens aprovadas alimentam o renderizador gratuito. DepthFlow é opção futura para paralaxe 2.5D e Blender para passeio com geometria 3D real.

Status verificado: ensaio manual de FFmpeg no ambiente de desenvolvimento (vídeo curto 1280x720/24 FPS/7,5 s), **sem implantação no PC Host**. Não enviar imagens privadas ou MP4 a este GitHub público. PR #1 segue Draft; não presumir merged.


## Video por servicos conectados no ChatGPT (23/10/2026)

O guia [Integracao ChatGPT > Runway / Higgsfield / Luma](knowledge/INTEGRACAO_CHATGPT_VIDEO_SERVICOS_R1.md) registra opcoes reais de **image-to-video por conector**, custos confirmados, creditos e requisitos. **Runway** e a primeira recomendacao, com plugin ChatGPT disponivel mas que exige conexao pelo usuario e saldo no Runway; o plano Free possui creditos unicos, nao renovaveis. **Higgsfield** consome creditos no plugin, mesmo quando ha geracoes gratuitas no website. **Luma** pode ser barata por video, mas precisa de bridge/API propria: nao fingir que ja ha plugin nativo operacional.

Regras: ChatGPT cria a imagem > usuario aprova > verificar se o conector realmente pode receber o anexo > consultar custo/creditos e pedir aprovacao antes de gastar > gerar um take curto > checar fidelidade > montar o MP4. **Nao afirmar que o workflow ponta a ponta foi executado** enquanto a conta do usuario nao estiver conectada. Proteger projetos de cliente fora do GitHub publico.

## Ordem R3 — metodologia integrada para imagens

**Arquivo primário:** [ROADMAP_OPERACIONAL_INTEGRADO_R3.md](ROADMAP_OPERACIONAL_INTEGRADO_R3.md).

Para continuar sem reiniciar o trabalho, leia o roadmap R3, o [piloto da cozinha/sala](research/testes/AR-BENCH-001_CASO_INTERIORES_R3.md) e os arquivos da PR Draft. Revalide o HEAD antes de alterar qualquer arquivo. As nove receitas e o comparador estão no projeto; o roteador de fluxo `tools/metodo_integrado.py` prepara prompts e relatórios privados, sem gerar imagens sozinho.

**Prioridade ativa:** primeiro executar o benchmark real de cozinha/sala (A/B/C, duas repetições por variante), depois lavanderia, depois fachadas/plantas. Iniciar cada geração a partir da imagem ORIGINAL acessível na conversa, nunca de um render já adulterado. Se não houver o original visível/anexado, não inventar que há arquivo ou que a geração foi feita.

**Restrições em vigor:** sem Incubadora Remote V2, sem GitHub Actions, sem uso obrigatório de Docker/GPU, sem dados de cliente na PR pública, sem merge não aprovado. Vídeos ficaram em segundo plano por decisão do usuário.


## Autorização permanente de fontes públicas — 23/10/2026

O usuário **autorizou expressamente** selecionar imagens adequadas na Internet e **solicitou pesquisas técnicas de sites e fóruns** ao longo do desenvolvimento. Esta diretriz deve ser aplicada em cada lote relevante, com fontes atuais e credíveis, sem esperar por imagens privadas para iniciar **testes públicos** seguros.

Antes de continuar, ler:
- `research/CURADORIA_WEB_IMAGENS_FORUNS_R1.md` — procedimento de curadoria, direitos, fontes/forum e seleção;
- `catalog/fontes_publicas_r1.json` — 7 fontes públicas selecionadas e rastreáveis (2 cenas 3D e 5 fotografias), sem arquivos baixados;
- `ROADMAP_OPERACIONAL_INTEGRADO_R3.md` — status/etapas e distinção entre benchmarking privado e público;
- `research/PESQUISA_FORUNS_E_FONTES_2026-10-23.md` — pesquisa anterior e contraexemplos de deriva geométrica.

O roteador offline conta com `python tools/metodo_integrado.py sources` e `sources --category interiores`. **Ele só lê o manifesto, não baixa imagens.**

**Obrigatório:** sempre apontar a origem, a licença, o autor, o status real (selecionado/baixado/editado/revisado) e não confundir licença de banco de imagem com domínio público. Jamais fingir que uma foto da busca web já chegou ao gerador nativo de imagens. Caso a edição não possa usar uma fonte web diretamente, informar a limitação e escolher via outro fluxo real.


## Correção de validade — fonte obrigatória e benchmark R3-04

No diagnóstico de 23/10/2026, imagens de cozinha geradas pela IA apareceram **como text-to-image** (`edit_op=null`, `parent_gen_id=null`), **não como edições vinculadas à imagem original**. As saídas trocaram mobiliário, aberturas, câmera e layout. Um infográfico de pontuações gerado por IA continha notas sem medição e é **INVÁLIDO** para qualquer decisão. Relatório verificado: `research/testes/AR-R3-04_DIAGNOSTICO_IMAGENS_ORIGINAIS_2026-10-23.md`.

As fontes originais privadas (cozinha/sala e lavanderia, ambas 1536 × 864 px) foram encontradas no ambiente de trabalho da conversa que produziu o relatório, mas **não** devem ser presumidas montadas em outro chat. Se não estiverem acessíveis, confirmar antes de rodar imagens.

O novo `tools/metodo_integrado.py bind` registra hashes dos arquivos originais e gerados com status de vínculo de fonte; `assess` agora recusa candidato sem referência comprovada. `tools/refino_fotometrico.py` oferece alternativa de correção de luz/cor sem geração IA, foi utilizada em dois exemplos reais sem sobrescrever originais (os binários NÃO estão no GitHub). Não confundir controle fotométrico com benchmark A/B/C; **0/6** imagens válidas ainda.

Próximo trabalho com segurança: executar suíte atualizada no checkout real; estabelecer edição **imagem-para-imagem** com fonte verdadeiramente transmitida e metadados; depois A/B/C. Fontes públicas Blender/Pexels seguem opcionais, com direitos e links registrados.


## Continuidade a partir da auditoria R4 — 23/10/2026

**R4 implementado em PR Draft:** ler [relatório de QA R4](research/testes/AR-R4_AUDITORIA_GEOMETRICA_2026-10-23.md), [código de auditoria](tools/qa_geometria.py) e [testes R4](tests/test_qa_geometria.py). O programa detecta indícios de alteração estrutural em quadro e ancoras individuais, sem decidir sozinho se o projeto está correto.

**Executado nesta etapa:** seis testes de QA R4 e seis testes API da versão-base passaram no container Linux; resultados reais em duas imagens originais privadas sob refino fotométrico, com alta retenção de bordas, e um falso render gerado por texto corretamente identificado como incompatível com o original. **Não afirmar que a suíte completa da branch passou**, nem que houve render AI fiel homologado: A/B/C ainda **0/6**.

**Ordem agora:** (1) executar toda a suíte da PR no checkout exato sem Actions, (2) garantir transmissão/edição real da imagem mestre ao gerador e registrar seu vínculo, (3) seis variações A/B/C, com QA, (4) ampliar para lavanderia e fontes públicas. Sem merge na main, sem alterações a dados de clientes e sem usar Incubadora Remote V2.


## Continuidade R5 — pipeline auditável de imagens

**Arquivos obrigatórios para retomar**:
1. `knowledge/PIPELINE_IMG2IMG_LOCAL_R5.md` — estratégia Krita AI Diffusion/ComfyUI, custo local, condições de hardware e máscara rígida;
2. `tools/compor_edicao_mascarada.py` + `tests/test_compor_edicao_mascarada.py` — preservar exatamente os pixels fora da região editável;
3. `tools/pipeline_img2img_r5.py` + `tests/test_pipeline_img2img_r5.py` — integração com contratos R3, SHA e QA R4;
4. `research/testes/AR-R5_PIPELINE_MASCARAS_EXECUCAO_2026-10-23.md` — relatório real do piloto, testes e suas limitações;
5. `ROADMAP_OPERACIONAL_INTEGRADO_R3.md` — escopo, cronograma e restrições anteriores.

**Status:** 52/52 testes locais em módulos correspondentes às versões GitHub dos scripts/testes; as receitas/catálogo de fontes testadas foram fixtures, e vídeo ficou fora da bateria. Piloto de imagem protegida com cozinha original realmente executado, **zero alterações em pixels não autorizados**. Todos os registros privados ficaram fora da PR. **Não há render generativo image-to-image homologado nem vitória de A/B/C; 0/6**. 

Quando o PC Host ficar online, escolher Krita AI Diffusion + ComfyUI **local**, iniciando modelo leve SD1.5 e região pequena com arquivo original realmente importado e máscara. Antes de qualquer instalação/download massivo, verificar SSD D:, NVIDIA RTX 3060 6 GB e RAM 16 GB; não habilitar serviços de rede desprotegidos nem consumir créditos pagos. **Continuar na PR #1 Draft; não mesclar a main e não usar GitHub Actions ou Incubadora Remote V2**.


## Regra P0 irrevogável sem autorização: IA extra R$ 0

**Diretriz expressa do usuário em 23/10/2026:** "O único gasto com ia que aceito é a assinatura do chatgpt que já tenho aqui". Esta decisão prevalece sobre propostas anteriores de integração de APIs/serviços de IA pagos. Ler **antes de qualquer alteração**:
- [Política de Custo Zero](knowledge/POLITICA_CUSTO_ZERO_IA.md)
- [Catálogo de motores permitidos](catalog/motores_ia_custo_zero.json)

**Obrigatório:** nenhum cartão, crédito pago, plano mensal adicional, API cobrada, aluguel de GPU na nuvem ou fallback pago de IA. Orçamento de IA adicional **R$ 0**. Não considerar uma franquia gratuita temporária como componente obrigatório. O Hub deve trabalhar com (1) ChatGPT desta conversa, com geração dentro do plano disponível e eventual transferência manual, (2) processos determinísticos gratuitos no Hub, e (3) ComfyUI/Krita AI Diffusion **local e gratuito, opcional, não instalado**. Não assumir que um web app externo pode usar a assinatura do ChatGPT via API sem custo: faturamentos separados. Ferramentas de Sign in with ChatGPT com compartilhamento de franquia só poderão ser examinadas mediante compatibilidade efetiva com o plano do usuário e autorização, **não homologadas aqui**.

Próximos lotes: R6 suíte completa, R7 interface web integrada, R8 preparar adaptador local, R9 testes Windows quando PC conectar. R3-R5 permanecem e a PR #1 segue Draft sem merge/Actions. Não mudar para modelo API paga para destravar imagem generativa.
