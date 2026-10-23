# Projetos GitHub úteis ao ArchRender Hub — seleção verificada

**Pesquisa realizada:** 23/10/2026.  
**Status:** pesquisa técnica e verificação de metadados/README, **sem instalar, clonar, executar ou incorporar código**.  
**Objetivo do ArchRender Hub:** o ChatGPT analisa referências arquitetônicas, constrói a direção de arte, gera imagens com a ferramenta disponível, compara a fidelidade e mantém o histórico de métodos. Não usar Incubadora Remote V2, nem assumir GPU, Docker, API paga ou gerador de vídeo acessível.

## Resumo da decisão

**Aproveitar AGORA os princípios de dois projetos MIT:**
- [ARCHI Rendering Studio](https://github.com/dakhlallah/arch-render) — regras de preservar projeto antes de estilizar, avaliação geométrica, prompts por entregável e documentação.
- [GPT Image Design Prompts](https://github.com/linlhf/gptimage-design-prompts) — roteamento do tipo de imagem de entrada (planta/croqui/modelo) para um prompt especializado com limites, modos de falha e referências.

**Utilizar como referência técnica para um segundo estágio:**
- [sd-interior-design](https://github.com/alaradirik/sd-interior-design) — inpainting + máscara/segmentação + MLSD para estrutura de interiores.
- [virtual-staging](https://github.com/mithunparab/virtual-staging) — estratégia Canny + Depth + máscara de área editável.
- [visual-comparison](https://github.com/BASILAHAMED/visual-comparison) — comparação visual com SSIM e destaque de diferenças; SSIM sozinho NÃO prova fidelidade geométrica depois de alterar luz/materiais.
- [DepthFlow](https://github.com/BrokenSource/DepthFlow) — geração de movimento *2.5D parallax* a partir de imagens estáticas; NÃO é visita virtual 3D nem ferramenta de vídeo generativo; licença AGPL-3.0.

**Examinar apenas como conceito, sem conectar à conta do usuário ou copiar código:**
- [ArchRenderAgent](https://github.com/isabelaclay47-debug/arch-render-agent) — ciclo de briefing > geração via browser autenticado > comparação > retoque. Apesar de alinhado ao objetivo, usa navegador Chrome com controle via CDP/Playwright e sessão ChatGPT; exige auditoria de segurança, confiabilidade e conformidade antes de qualquer tentativa.
- [Open Wall](https://github.com/keenranger/open-wall) — combinação de 3 a 5 fotografias da **mesma sala**, com OpenAI API paga/credenciais; não se aplica diretamente às duas imagens-base do piloto, que são espaços diferentes.
- [ScribbleArchitect](https://github.com/s-du/ScribbleArchitect) — croqui em tempo real, IP-Adapter e ControlNet, mas demanda CUDA/GPU; não foi localizada licença de código declarada no registro GitHub. Não copiar implementação sem verificar direitos.
- [ComfyUI](https://github.com/Comfy-Org/ComfyUI) — plataforma poderosa para máscaras/Depth/ControlNet, mas requer outro motor e pode exigir GPU, downloads e manutenção; licença GPL-3.0. **Não adotar por padrão agora.**

## Comparação verificável

| Projeto | Uso relevante | Prontidão para 'ChatGPT gera aqui' | Pré-requisitos para rodar | Licença verificada no GitHub |
| --- | --- | --- | --- | --- |
| ARCHI Rendering Studio | preservação, câmera, qualidade, evals, receitas | **Alta para incorporar princípios textuais**; plugin Codex não é obrigatório para ler | instalar plugin Codex requer Node 20+ e Git; **não instalaremos** | MIT |
| GPT Image Design Prompts | templates especializados de sketch/model/plan e diretrizes de falha | **Alta** para ler e adaptar o método | Codex é opcional; usar apenas o conhecimento | MIT |
| sd-interior-design | preservar layout com MLSD e inpainting | **Média como referência técnica**, não plugin nativo do ChatGPT | Cog + Docker, modelo próprio / GPU ou serviço | MIT (modelos têm licenças separadas) |
| virtual-staging | ControlNet estrutural + máscara localizada | **Média como referência técnica** | PyTorch, modelos, recursos de inferência/treino | Apache-2.0 |
| visual-comparison | SSIM e imagens de diferença | **Alta como técnica leve de QA futura** | Python 3.9+ e dependências; sem geração de imagem | MIT |
| DepthFlow | produzir vídeo com parallax de uma imagem | **Opcional e condicionado à instalação**, não walkthrough real | instalação e capacidade de render gráfico/ffmpeg | AGPL-3.0 |

A "prontidão" é **nosso julgamento sobre aplicar o conhecimento**, não certificação de que o projeto passou em testes.

## Achados específicos ao examinar os arquivos

### ARCHI Rendering Studio: mais útil que um conjunto de adjetivos de render

- \`references/automatic-prompt-pack.md\` distingue 20 possíveis entregáveis sem fabricar os que não são sustentados pelas fontes.
- \`references/image-generation-quality-engine.md\` separa provedor de imagem, estrutura/projeção, escala nativa versus upscale e avaliação a 100% de zoom.
- \`evals/EVALS.md\` tem testes específicos: documento em outra proporção não virar 16:9, não mover esquadrias, não inventar vista traseira, não prosseguir com arquivos confidenciais ou execução sem autorização.
- **Sugestão ao ArchRender Hub:** adaptar a verificação de "fonte documentada / hipótese" e o roteiro de inspeção, sem copiar blocos extensos literalmente.

### GPT Image Design Prompts: roteador de casos de uso

- \`references/prompt-patterns.md\` tem seções como \`sketch-to-render\`, \`model-to-render\` e \`plan-to-colored-plan\`.
- Cada receita declara gatilho, entradas, preservações, falhas recorrentes, vocabulário e sugestão de saída.
- **Sugestão:** nossas nove receitas devem compartilhar essa mesma taxonomia, além de contrato geométrico e relatório de falhas.

### Técnicas de preservação: sd-interior-design e virtual-staging

- A primeira usa máscaras/segmentação e ControlNet MLSD (linhas), não somente instrução textual.
- A segunda adiciona Canny (arestas), Depth (profundidade) e máscara de região modificável.
- Esses mecanismos **não estão acessíveis automaticamente** pelo gerador nativo do ChatGPT. A estratégia alternativa imediata é imagem original única + alterações localizadas + QA; quando indispensável, compor camadas preservadas deterministicamente ou escolher um motor externo após autorização.
- **Não afirmar** que esses projetos garantem 100% de geometria. Os próprios fluxos exigem verificação.

### Controle de qualidade e vídeo

- \`visual-comparison\` calcula SSIM e marca regiões diferentes. Quando o objetivo é trocar material ou luz, diferenças são esperadas: comparação de pixels não equivale a contagem de paredes/janelas. O QA deve comparar **marcos arquitetônicos** além de semelhança de imagem.
- DepthFlow cria animação de profundidade/parallax 2.5D sobre imagem; pode contribuir para apresentações sem vídeo generativo, mas não revela corretamente outras faces do edifício. Sua licença AGPL precisa ser revisada se código for redistribuído num sistema.

### Navegador automatizado: cuidado com ArchRenderAgent

O README apresenta um ciclo diretamente inspirado no que queremos, com Chrome logado e Playwright/CDP. Como a automação ganha acesso poderoso a um navegador com sessão autenticada, **não instalar, rodar ou vincular a credenciais sem revisão de código e consentimento claro**. A interface do ChatGPT pode mudar e quebrar a automação. Considerar ideias de validação, não como dependência do ArchRender Hub.

## Priorização para nosso primeiro teste formal: cozinha/sala

1. **Primeira rodada A:** prompt-base curto com apenas a imagem ORIGINAL do ambiente.
2. **Segunda rodada B:** receita de interiores do ArchRender Hub, enriquecida com inventário de vãos, câmera e materiais, inspirada no roteamento do GPT Image Design Prompts.
3. **Terceira rodada C:** aplicar o protocolo de preservação/QA do ARCHI Rendering Studio: identificar imagens-fonte, itens imutáveis, variações autorizadas e comparação de marcos arquitetônicos. Se a geração continuar inventando objetos, recorrer a edição localizada ou imagem original com camada de acabamento.
4. **Avaliação:** mesmo recorte de entrada, mesmo gerador, mesmas referências e número de tentativas por variante, quando a ferramenta permitir. O prompt efetivamente visível/indicações enviadas são registradas. **Não inventar** parâmetros internos do gerador, seeds, qualidade nativa ou texto completo de prompt que a ferramenta não expôs.
5. **Saída:** imagens aprovadas somente após conferência; arquivos privados fora do GitHub público, registrar relatório anonimizado.

**Lição importante:** estudar um repositório de geração não é executar o código nem obter resultado de imagem com aquela ferramenta. O objetivo imediato é aproveitar o **método operacional** dos melhores exemplos, mantendo o ChatGPT como executor principal das imagens.

## Verificação

- Metadados, repositórios, licenças e README checados por GitHub em 23/10/2026.
- Conteúdo de \`references/prompt-patterns.md\`, \`references/automatic-prompt-pack.md\`, \`references/image-generation-quality-engine.md\`, \`evals/EVALS.md\`, exemplos do \`visual-comparison\` e README do DepthFlow inspecionados.
- Não há medições independentes nossas de qualidade nem comprovação de desempenho superior de um motor sobre outro.
- A aplicação V0.1 não foi modificada. Sem Incubadora, sem GitHub Actions.
