# Integração de métodos GitHub — ArchRender Hub

**Data:** 2026-10-23 · **Versão:** R1 · **Estado:** documentação incorporada, técnicas externas ainda não executadas.

**Diretriz:** o ChatGPT produz imagens com suas ferramentas disponíveis; o Hub registra receitas, proveniência, instruções e avaliações. Adaptamos conceitos e estrutura editorial, **não copiamos nem instalamos automaticamente códigos de terceiros**. Os arquivos originais e resultados de clientes não devem ir ao GitHub público.

## 1. Correspondência entre necessidades e recursos

| Projeto de origem | O que aproveitamos AGORA | Onde entra no Hub | Não implica |
| --- | --- | --- | --- |
| [dakhlallah/arch-render](https://github.com/dakhlallah/arch-render) (MIT) | contrato de preservação de geometria, seleção de câmera, portões de QA, evidência versus hipótese e relatórios de falhas | \`knowledge/OPERACAO_COM_CHATGPT.md\`, \`templates/VALIDACAO.md\`, \`knowledge/prompts/\` | ter instalado o plugin Codex ou seus motores |
| [linlhf/gptimage-design-prompts](https://github.com/linlhf/gptimage-design-prompts) (MIT) | seleção de tipo de fonte/tarefa, lista de preservar, falhas frequentes, proposta de saída | \`knowledge/ROTEADOR_DE_RECEITAS_R1.md\` | prompts "testados" em nosso benchmark |
| [alaradirik/sd-interior-design](https://github.com/alaradirik/sd-interior-design) (MIT para código) | inpainting + máscara + linhas MLSD para interior com layout preservado | trilha técnica do método avançado, ainda opcional | ControlNet disponível no gerador nativo ChatGPT |
| [mithunparab/virtual-staging](https://github.com/mithunparab/virtual-staging) (Apache-2.0) | conceito de Canny + Depth + máscara localizada | checklist e propostas de ferramenta avançada | preservação perfeita ou inferência disponível sem instalação |
| [BASILAHAMED/visual-comparison](https://github.com/BASILAHAMED/visual-comparison) (MIT) | SSIM e imagens de diferenças; comparação regional | QA futura, além do comparador manual já existente no Hub V0.1 | SSIM prova número/posição de janelas |
| [BrokenSource/DepthFlow](https://github.com/BrokenSource/DepthFlow) (AGPL-3.0) | vídeo de paralaxe 2.5D sobre imagem aprovada | \`knowledge/VIDEO_GRATUITO_PC.md\` | vídeo generativo real ou visita 3D completa |
| [Comfy-Org/ComfyUI](https://github.com/Comfy-Org/ComfyUI) (GPL-3.0) | caminho futuro para máscaras, controle de profundidade e modelos alternativos | backlog condicionado a GPU/licença | software já instalado no PC |
| [Lightricks/LTX-Desktop](https://github.com/Lightricks/LTX-Desktop) (termos do projeto/modelos) | possível geração **local** image-to-video com modelo de IA | avaliação futura após inventário de GPU/RAM/disco e termos de licença | custo zero em cloud/API ou suporte no hardware atual |

**Nota sobre licenças:** documentos aqui são material original resumido a partir de padrões e conceitos públicos. MIT/Apache/GPL/AGPL se referem aos códigos dos projetos respectivos; arquivos de modelos/weights têm seus próprios termos. Não importar código sem revisão de licenças e dependências.

## 2. Contrato mínimo de entrada (antes de produzir imagens)

\`\`\`yaml
id: AR-CASE-001
tipo: interiores | fachada | planta | paisagismo | video
modo: F # F=fiel, C=conceito, T=tecnico
fonte:
  imagem_geometria: "arquivo privado local ou anexo"
  imagens_estilo: [] # nunca substituir a geometria
  versao_projeto: "desconhecida"
preservar:
  - paredes e seus encontros
  - portas/janelas e posicoes
  - circulacao e volumes
  - camera/perspectiva
mudar:
  - textura, luz, sombra (somente quando autorizado)
nao_gerar:
  - abertura nova
  - mobilia nao autorizada
validacao:
  gates: [geometria, camera, materiais, artefatos]
  status_inicial: candidato_nao_testado
\`\`\`

1. **Classificar intenção** e identificar todas as imagens base versus referência de estilo.
2. **Extrair inventário de geometria** com elementos visíveis e incógnitas; não inventar dimensionamento.
3. **Selecionar receita** via \`knowledge/ROTEADOR_DE_RECEITAS_R1.md\`.
4. **Executar imagem no ChatGPT** quando estiver disponível; não responder só prompt.
5. **Inspecionar original e resultado** lado a lado. Detectar novos/movidos elementos, perspectiva e padrão de materiais.
6. **Reprovar** a geração se o gate geométrico falhar em modo F/T. Não compensar falha geométrica por notas altas de estética.
7. **Registrar** ferramenta real, prompt visível, limitações, resultado (sem upload público), status e evidência.

## 3. Piloto da cozinha/sala

**Fonte:** uma imagem original de interior compacto fornecida em conversa.  
**Inventário fixo:** sofá, mesa lateral, geladeira, bancada em L, pia, janela preta, corredor, luminárias da fonte.  
**Testes:** A prompt curto; B receita AR-INT-001 com inventário; C método R2 com preservação, QA e correção local se disponível.  
**Limite:** somente vídeos a partir das imagens **aprovadas**; os testes anteriores tinham aparência atraente, mas elementos reinterpretados, portanto **não são automaticamente aprovados**.

## 4. Evidência e lacunas

O Hub V0.1 possui **comparador deslizante antes/depois**; não precisamos duplicá-lo. Faltam métricas automáticas e pontos de controle de arquitetura. A integração textual R1 está incorporada; métodos externos de difusão e DepthFlow ainda dependem de recursos locais e validação. O gerador independente de vídeo gratuito é código original em \`tools/video_local.py\`.

**Referências detalhadas e verificação inicial:** [Pesquisa GitHub](../research/PROJETOS_GITHUB_UTEIS_2026-10-23.md). Revisão de licença e versões deve ser repetida antes de instalar versões específicas.
