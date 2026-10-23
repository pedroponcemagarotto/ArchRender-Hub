# Curadoria web contínua — imagens públicas, fóruns e aprendizado (R1)

**Pesquisa iniciada:** 23/10/2026 · **Solicitação:** utilizar também imagens adequadas da Internet, pesquisando sites, GitHub e fóruns úteis ao ArchRender Hub em cada etapa pertinente.  
**Ramo:** `feat/prompt-system-v1` · **Status:** curadoria de fontes e metadados realizada, **sem baixar arquivos nem gerar imagens neste lote**.  
**Manifesto com sete candidatos rastreáveis:** [`catalog/fontes_publicas_r1.json`](../catalog/fontes_publicas_r1.json).

## 1. Diretriz permanente a aplicar durante o desenvolvimento

Antes de iniciar uma nova família de imagens, alterar uma receita, mudar uma ferramenta ou concluir que um método falhou:

1. Fazer uma **pesquisa atualizada e direcionada** nos sites oficiais, licenças, fóruns de profissionais, issues GitHub e documentação de modelos aplicáveis. Para pequenas alterações de texto já verificadas, reutilizar referência existente; não pesquisar repetidamente sem ganho.
2. Favorecer **evidência reproduzível**, com foto/modelo original acessível, prompt/controle, captura antes/depois, versão da ferramenta e falhas documentadas. Anotar **data de publicação, data do experimento e data de consulta** separadamente.
3. Comparar recomendação comunitária com documentação oficial e, idealmente, mais de um profissional independente; declarações comerciais e dicas de fórum **não são benchmark**.
4. Antes de baixar/usar uma foto, confirmar **licença da imagem específica**, fonte original, autor, possíveis restrições sobre marcas, arte e pessoas. Salvar o original sem sobrescrever e registrar proveniência.
5. Separar **referências estéticas** (luz, materiais, fotografia) de **referência geométrica** (a própria imagem original, CAD, modelo 3D, planta). Foto de terceiros **não substitui nem “corrige” arbitrariamente um projeto do cliente**.
6. Escolher tarefa e receita R3 (A/B/C), realizar a geração com a **imagem realmente fornecida ao gerador**, conferir saída e registrar erros, acertos, ajustes e origem.
7. Em lotes posteriores, repetir pesquisas se modelos, preços, licenças ou restrições mudarem. **“Pesquisar sempre” significa este procedimento durante o trabalho**, não vigilância automática sem agendamento/autorização.

A curadoria não dá permissão para publicar qualquer material na PR. Somente metadados, links e descrições originais são publicados. Downloads, outputs reais e dados sensíveis ficam em pasta privada local/working area, não no repositório.

## 2. Casos públicos selecionados agora

| ID | Cena | Material verdadeiro | Licença e autoria | Por que foi selecionado |
| --- | --- | --- | --- | --- |
| **AR-PUB-001** | [Classroom](https://www.blender.org/download/demo-files/) | Cena 3D com geometria conhecida; download pela página oficial Blender | **CC0**, Christophe Seux | **Melhor caso inicial para flagrar deformações** em aberturas, mobiliário, paredes e perspectiva; aproximadamente 72 MB do arquivo da cena |
| **AR-PUB-002** | [Barcelona Pavillion](https://www.blender.org/download/demo-files/) | Modelo 3D arquitetônico Blender | **CC BY**, eMirage; crédito obrigatório | Avaliar pilares, revestimentos, volumes, esquadrias/aberturas e reflexos; aproximadamente 24 MB |
| **AR-PUB-003** | [Cozinha e sala integradas com luz natural](https://unsplash.com/photos/modern-kitchen-and-living-area-with-natural-light-YC-TOvwaj4Y) | Fotografia, não modelo 3D | **Unsplash License**, Kailun Zhang | Benchmark de interior com bancada, móveis, janela e iluminação; **não** comprova dimensão real |
| **AR-PUB-004** | [Cozinha com pia e janela](https://unsplash.com/photos/a-kitchen-with-a-sink-a-counter-and-a-window-mNWVJ3hOCTk) | Fotografia | **Unsplash License**, Ryan Ancill | Testar luz lateral forte, reflexos, definição de materiais e permanência de esquadrias |
| **AR-PUB-005** | [Lavanderia com cuba e máquinas](https://unsplash.com/photos/a-laundry-room-with-a-sink-and-a-washer-and-dryer-upiqQpeUCYU) | Fotografia | **Unsplash License**, Zac Gudakov | Segundo ambiente com muitos elementos fixos para medir deformação em edição |
| **AR-PUB-006** | [Fachada moderna e jardim](https://www.pexels.com/photo/concept-of-modern-house-9976121/) | Fotografia, 5089 × 3393 segundo a fonte | **Pexels License**, Jonathan Borba | Avaliar volumetria visível, aberturas, jardim e continuidade de materiais |
| **AR-PUB-007** | [Fachada com portas de vidro](https://www.pexels.com/photo/exterior-of-modern-house-with-glass-doors-and-panoramic-windows-7031607/) | Fotografia, 7360 × 4912 segundo a fonte | **Pexels License**, Max Vakhtbovych | Testar preservação de grades/esquadrias e reflexos, inclusive quando um upscale alterar linhas |

**Estes são sete candidatos selecionados e com indicações de licença consultadas, mas os bytes ainda não foram adquiridos nem comparados neste lote.** A fotografia da lavanderia pública NÃO é a lavanderia enviada anteriormente pelo usuário. O piloto particular da cozinha/sala em `AR-BENCH-001` continua separado e pendente, com contador 0/6.

### Escolha prioritária

**Começar pelo AR-PUB-001 Classroom**, pois o modelo 3D serve de referência estrutural verificável. Gerar uma captura simplificada e uma referência renderizada da MESMA câmera (quando Blender estiver operacional); converter/editar a captura usando os métodos A/B/C; conferir se o resultado preservou aberturas, objetos, escala visual e linhas. Não apresentar a cena de referência como “render gerado pelo ChatGPT”.

Em paralelo, **AR-PUB-003** ajuda a calibrar acabamento fotográfico, iluminação e materiais; **AR-PUB-005** ajuda a construir casos com tanque/máquinas. Fotos demonstram controle do que é visível, não conferem acesso a geometria 3D oculta.

### O que autoriza e o que não autoriza

- [Blender Demo Files](https://www.blender.org/download/demo-files/) informa **Classroom CC0**, **Barcelona Pavillion CC BY** e também **Cozy Kitchen CC BY-SA** (este último é interessante, mas sua licença exige análise de atribuição/ShareAlike antes de redistribuir derivados).
- [Poly Haven licença](https://polyhaven.com/license): **modelos, texturas, HDRIs do catálogo CC0**, inclusive comerciais. **Imagens editoriais de exemplo, logos e trabalhos enviados por usuários no site NÃO são automaticamente CC0**; verificar tipo de asset. Evitar raspagem em massa não autorizada; API oficial tem termos próprios.
- [Unsplash licença gratuita](https://unsplash.com/license): a foto gratuita pode ser modificada; não usar imagens **Unsplash+** presumindo as mesmas regras. **Unsplash+** tem termos adicionais e restrições de tecnologia de IA — conferir. Evitar casos com pessoas, logotipos e obras protegidas.
- [Pexels licença](https://www.pexels.com/pt-br/licenca/): permite modificar fotos gratuitamente; veda revenda como stock ou conteúdo essencialmente inalterado; marcas/pessoas/obras retratadas podem exigir permissões adicionais.
- Manter crédito recomendado mesmo quando não obrigatório. **CC BY exige atribuição**. Nunca atribuir uso comercial ou redistribuição a uma licença ainda não conferida.
- Download pelo site/endpoint oficial, quando a ferramenta permitir, para área temporária privada. Não clonar imagens no repositório.
- Se o ChatGPT **não conseguir receber como referência editável a imagem da web**, não fingir que a usou: documentar limite, usar gerador/fluxo que receba o arquivo real ou solicitar anexo se estritamente necessário.

## 3. Fóruns, documentação e repositórios com sinal técnico

| Prioridade | Local e discussão verificável | Questão que ajuda a resolver | Precaução |
| --- | --- | --- | --- |
| 1 | [Blender Demo Files](https://www.blender.org/download/demo-files/) e [manual Blender](https://docs.blender.org/manual/en/latest/) | cenas com geometria auditável, câmera fixa, iluminação e render de referência | licença por cena; diferenças de versão Blender |
| 1 | [r/archviz — debate de integração de IA (fev/2026)](https://www.reddit.com/r/archviz/comments/1rbc5ge/how_has_ai_actually_integrated_into_your_archviz/) | como estúdios usam IA para luz, pessoas e vegetação preservando render base | depoimentos; não generalizar |
| 1 | [r/archviz — experiência prática (abr/2026)](https://www.reddit.com/r/archviz/comments/1slp022/my_experience_while_exploring_ai_as_rendering_tool/) | deriva geométrica, dificuldade de vários ângulos, escala e revisão | caso pessoal, não ensaio controlado |
| 1 | [r/comfyui — arquitetura](https://www.reddit.com/r/comfyui/comments/1u13ayk/confyui_in_architectural_visualization/) e [documentação ControlNet](https://docs.comfy.org/tutorials/controlnet/controlnet) | máscaras, lineart, depth, edição conservadora | opções externas ao gerador nativo ChatGPT |
| 2 | [Enscape 4.7 — anúncio oficial](https://forum.enscape3d.com/index.php?thread/29897-enscape-4-7-0-released/) e [Chaos Forums](https://forums.chaos.com/) | fluxos de dados/camadas de material e ferramentas de preservação ao integrar com Veras | suporte e preços dependem de versões/licença; não assumir que usuário possui Veras |
| 2 | [SketchUcation — ferramentas AI para render](https://community.sketchucation.com/topic/164691/ai-render-enchancer-extensions-or-tools/13) | comparação de edição pontual e alternativas para imagens Enscape/SketchUp | diferenciar usuário independente de funcionário promovendo produto |
| 2 | [SketchUp Community — feedback sobre realismo](https://forums.sketchup.com/t/need-feedback-for-rendering/269770) | sombras ausentes, escala de textura, iluminação artificial/natural | tópico não prova funcionamento de modelo de IA |
| 2 | [Chaos Forum — AI Enhancer e resolução](https://forums.chaos.com/t/chaos-corona-13-for-3ds-max-daily-builds-discussion/158434?page=12) | impactos de downscale/upscale e tamanho de entrada em render 4K | efeitos/limites mudam com versões |
| 2 | [Poly Haven](https://polyhaven.com/) | texturas PBR, HDRI, assets CC0 para elevar o render 3D antes de editar com IA | usar assets específicos, não imagens editoriais arbitrárias |
| 3 | [Archinect — materiais por IA (jan/2026)](https://archinect.com/forum/thread/150520831/ai-materials/0) | problemas de materiais com padrões precisos e limites da IA | opiniões divergentes; validação necessária |

### Aprendizado incremental — 2026-10-23

**A. Enscape/Veras já explora entradas além do JPEG.** O anúncio da 4.7 descreve camadas de *material IDs* e outros dados que ajudam a IA a respeitar a base CAD, além do controle de respeito à geometria e edição restrita a regiões no Veras. **Impacto no Hub:** prever, quando houver acesso ao Enscape, camadas de máscara/IDs e geometria como material de referência. Não afirmar que tais controles estão disponíveis no ChatGPT, ou que o Veras é gratuito.

**B. Profissionais confirmam problema concreto de derivação.** Debate no r/archviz em 2026 descreve utilidade para estudos de iluminação, elementos secundários e upscale, mas aponta alterações involuntárias em geometria, materiais e consistência. **Impacto:** manter o render de origem + teste A/B/C + QA de esquadrias.

**C. Inputs de maior resolução nem sempre dão mais qualidade após IA.** Debate de desenvolvedores do Chaos Corona sobre entrada 4K/2K e upscale ilustra que o resultado depende do pipeline, não da palavra “8K” no prompt. **Impacto:** medir pixels reais e comparar variantes também no recorte 100% de janela, canto de móveis e juntas.

**D. Qualidade da evidência:** manual oficial/licença **alta** para capacidades declaradas; repositório com código/testes **alta para mecanismo**, não para resultados do Hub; fóruns de usuários **média**; marketing/demo sem entrada original, evidência **baixa**. Registrar conflito de interesse publicitário.

## 4. Checklist de pesquisa para cada novo lote

**Busca prévia:** consultas dirigidas com data e tema; oficial da ferramenta, fóruns específicos e GitHub.  
**Seleção:** pelo menos um caso independente e um caso com geometria rastreável quando possível.  
**Custo:** priorizar imagens gratuitas/licenças compatíveis; não consumir créditos nem baixar assinaturas sem autorização.  
**Aquisição:** verificar arquivo e resolução real, licença na URL exata, autoria, URL persistente, autorização de uso e eventuais condicionantes de marcas e privacidade.  
**Benchmark:** original idêntico para A/B/C, registro de ferramenta/modelo realmente exposto, 2 repetições exploratórias, revisão geométrica antes da estética, retrabalho anotado.  
**Retenção:** registrar fonte/versão/resultado/erros em manifesto; mídias privadas em `data/`, não no GitHub; saída pública só com autorização e atribuição adequadas.  
**Atualização:** ao próximo lote relevante, verificar novos posts, atualizações de produto/licença e novos repositórios. Registrar o que mudou; não reescrever o passado.

## 5. Limites e continuidade

- Pesquisa feita **nesta interação**; **não** há tarefa agendada nem monitoramento contínuo no intervalo entre mensagens.
- Os sete itens do catálogo são **fontes prontas para aquisição/benchmark**, não benchmark realizado.
- Não existe garantia de que a ferramenta de imagem do ChatGPT receberá como fonte editável uma imagem selecionada diretamente da busca web. Garantir que bytes reais chegaram ao gerador antes de contabilizar produção.
- **Prioridade prática:** caso público CC0 `AR-PUB-001` quando houver acesso a Blender + original, e depois cotejar o aprendizado com `AR-BENCH-001` particular da cozinha/sala. O público é teste complementar, não substitui projeto real do usuário.

**Arquivo-mestre de projeto:** [Roadmap R3](../ROADMAP_OPERACIONAL_INTEGRADO_R3.md).
