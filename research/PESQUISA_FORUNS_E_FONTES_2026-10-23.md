# Pesquisa de fóruns, casos práticos e documentação — ArchRender Hub

**Data:** 23/10/2026 (America/Sao_Paulo)  
**Responsável:** curadoria inicial assistida por IA, sujeita a validação prática  
**Foco:** produzir plantas humanizadas, fachadas, interiores e apresentações para clientes usando o ChatGPT como diretor visual e gerador de imagens, sem usar a Incubadora Remote V2.  
**Estado da evidência:** leitura de fontes primárias e fóruns realizada; **nenhum benchmark próprio foi executado** neste lote.

## 1. Resposta central

Um "prompt perfeito" não equivale a um pipeline de qualidade arquitetônica. As melhores evidências encontradas apontam para **hibridização**: base geométrica/imagem original + instruções restritas sobre materiais/luz + geração/edição de imagem + correções pontuais + revisão visual. A fotografia arquitetônica de qualidade exige composição, iluminação, materiais fisicamente plausíveis, detalhamento, contexto e pós-produção.

**Aviso:** a fonte geométrica pode ser CAD/BIM/modelo 3D já fornecido. O objetivo não é exigir que o usuário use V-Ray; é aproveitar a fonte visual que ele tiver. Porém, quando só há planta raster/uma fotografia, **não é possível garantir vistas inéditas ou cotas exatas por texto**. O modo de geração nativa do ChatGPT não expõe necessariamente seed, denoise, máscara ou ControlNet; os fluxos ComfyUI servem como técnica de referência, não como ferramenta ativada dentro deste chat.

## 2. Resultados encontrados em fóruns: evidências priorizadas

### F1. r/archviz — “My experience while exploring AI as rendering tool”, abril/2026
https://www.reddit.com/r/archviz/comments/1slp022/my_experience_while_exploring_ai_as_rendering_tool/

Autor de prática de visualização compartilha experiências com Gemini. Relata que a IA ajuda na atmosfera, versões de dia/noite e texturas, mas sofre para reproduzir a mesma edificação por ângulos diferentes, respeitar escala e fazer revisões subsequentes. **Peso:** testemunho de profissional, subjetivo, com exemplos; não mede quantitativamente o desempenho médio de todos os modelos. **Conclusão útil:** nunca aceitar imagem bonita como prova de fidelidade; manter imagem-fonte e registro de cada ajuste.

### F2. r/comfyui — “ConfyUI in architectural visualization”, junho/2026
https://www.reddit.com/r/comfyui/comments/1u13ayk/confyui_in_architectural_visualization/

Relato de oficina com arquitetos. Começaram de wireframe, SketchUp, clay render, croqui ou foto. Três estágios: (1) ControlNet/condicionamento estrutural, (2) inpainting/adição localizada, (3) image-to-image/upscaling. Os participantes discutem alternativas Flux, SDXL, ZImage e suas limitações. **Peso:** demonstração prática de turma e relato direto, mas não protocolo cego padronizado. **Conclusão:** geometria/alterações devem ser separadas; iterar por região.

### F3. r/comfyui — “Sketchup + AI Rendering Workflow with Image Upscaling?”, agosto/2026
https://www.reddit.com/r/comfyui/comments/1vm9ymj/sketchup_ai_rendering_workflow_with_image/

Relato concreto de pipeline: SketchUp → linework + passe de sombra/clay → duas referências estruturais (Lineart e Depth) → geração → upscale conservador. Um comentarista relata **Lineart 0,8, Depth 0,6, denoise 0,7, upscale 1,5x** em SDXL. **Peso:** parâmetros **anedóticos e específicos daquele workflow**, jamais usar como presets universais ou afirmar que a geração nativa do ChatGPT tenha esses controles. **Conclusão:** estrutura legível antes de qualquer prompt e upscale com baixa criatividade para não deformar esquadrias.

### F4. r/Sketchup — “SKETCHUP + AI”, setembro/2026
https://www.reddit.com/r/Sketchup/comments/1wf7yk1/sketchup_ai/

Profissionais relatam que revisões de imagem gerativa podem ampliar cômodos, esticar móveis e mudar aberturas. Um deles recomenda usar IA como refinamento de render preexistente. Outro sugere manter o render 4K original e comparar esquadrias/guarda-corpos/juntas a 100% de zoom; ao alterar sombras de fato, o ideal seria mudar iluminação na cena 3D. **Peso:** vários depoimentos independentes, algumas pessoas podem ter ligação comercial com ferramentas; os testemunhos não constituem medição. **Conclusão:** preservar a fonte e nunca usar upscale como prova de fidelidade.

### F5. r/Sketchup — “GPT Render”, junho/2025
https://www.reddit.com/r/Sketchup/comments/1lfwvbs/gpt_render/

Usuários discutem o problema de atender revisões pequenas: reduzir uma janela, manter os mesmos materiais, entorno e câmera, ou apresentar a mesma arquitetura de três pontos de vista. **Peso:** caso real de debate comunitário, não teste controlado. **Conclusão:** pedir mudanças localizadas; para novas perspectivas, preferir views exportadas do mesmo projeto 3D.

### F6. r/Homebuilding — “Using AI to create renders from design sketches”, junho/2025
https://www.reddit.com/r/Homebuilding/comments/1lc40o9/using_ai_to_create_renders_from_design_sketches/

Usuário publicou exemplo com ChatGPT: partiu de elevação/croqui, especificou materiais e iluminação fotográfica. Mesmo com um prompt detalhado, relata janelas e cotas afetadas; outros comentaristas alertam que insistir em correções pode piorar a geometria. **Peso:** experimentador com exemplos e prompt, desempenho anecdótico de versão antiga do modelo. **Conclusão:** além de boa direção de materiais, restaurar a origem em tentativas novas quando a edição começa a divergir.

### F7. r/StableDiffusion — “SD + Controlnet for Architecture/Interiors”, maio/2023
https://www.reddit.com/r/StableDiffusion/comments/13w2pyk

Relato de arquitetura: exportar vista lineart do Revit, aplicar ControlNet e evoluir prompts/linhas. Autor comenta que preparações estruturais levam tempo, podendo superar o ganho prometido. **Peso:** experiência direta, mas antiga e dependente da tecnologia de 2023. **Conclusão:** automatização só vale se reduzir retrabalho real; projeto simples pode ser mais rápido por IA nativa.

## 3. Teste técnico publicado com relevância elevada

**Generative Interior Design Challenge 2024 — solução de 2º lugar (Bartosz Ludwiczuk e equipe)**  
https://medium.com/@melgor89/generative-interior-design-challenge-2024-2nd-place-solution-6338f19f6fe3

- Baseline gerou bom estilo, mas deslocou uma parede e apagou uma porta.
- Equipe descreve segmentação de ambiente, máscaras de janelas/portas, ControleNet, testes de intensidade/strength, modelagem de profundidade, múltiplas tentativas e revisão humana.
- Autor afirma que engenharia de prompt por si só trouxe pouco avanço para preservação geométrica.
- A intensidade 0,9 foi relatada **no pipeline específico** com máscaras para preservar certas partes: não extrapolar para outros geradores.
- Avaliadores e métricas automáticas tinham limitações; realisticidade da textura e manutenção dos vãos podem falhar mesmo quando imagem é bonita.

**Força de evidência:** metodologia técnica reproduzível e competição externa, acima de dica avulsa. **Limites:** modelos e dados de 2024, objetivo restrito a interiores.

## 4. Documentação oficial — mecanismos que valem adaptar

### OpenAI, image prompting e edição por referências
https://developers.openai.com/api/docs/guides/image-prompting

Nomear a entrega, sujeito, composição e materiais; dar a cada imagem anexada uma função explícita; separar o que mudar do que preservar; iterar uma coisa por vez, conferindo a saída. A documentação da API descreve seleção/qualidade de modelos, mas **não significa que o usuário ou esta conversa disponham dos mesmos controles na interface do ChatGPT**.

### Chaos, realismo profissional
https://blog.chaos.com/7-essential-steps-to-creating-realistic-renderings
https://blog.chaos.com/ai-architecture-prompts
https://blog.chaos.com/how-to-master-veras-ai-architects-prompt-guide

Fotografia arquitetônica: composição visual, boa base geométrica, escala dos objetos, balanceamento de luz natural e artificial, microtextura e juntas, materialidade, câmera, contexto e pós-produção. Ao partir de Revit/SketchUp, não descrever geometria contraditória no prompt: pedir materiais, atmosfera e luz sobre a base existente. A sugestão de listar poucos materiais é uma **heurística de clareza**, não norma universal.

### ComfyUI — ControlNet e preprocessadores
https://docs.comfy.org/tutorials/controlnet/controlnet
https://docs.comfy.org/tutorials/controlnet/depth-controlnet
https://docs.comfy.org/tutorials/utility/preprocessors

Lineart/Canny preservam contornos, Depth condiciona perspectiva/profundidade, máscaras/segmentação limitam edição. É um mecanismo **não nativo do gerador de imagens deste chat**. Para uso só com ChatGPT, reproduzir o princípio prático: base fiel em alta qualidade + papéis de referência + alterações locais + conferência; quando viável, fazer composição por camadas e sobreposição de linhas/cotas verificadas.

### Runway — vídeos image-to-video
https://help.runwayml.com/hc/en-us/articles/48324313115155-Image-to-Video-Prompting-Guide
https://help.runwayml.com/hc/en-us/articles/39789879462419-Gen-4-Video-Prompting-Guide

A imagem aprovada já comunica o visual; texto do vídeo deve informar movimento de câmera/cena e tempo. Um plano curto, pouca parallax e movimento sutil exigem menos conteúdo geométrico inventado do que um grande voo orbital a partir de uma foto única. **A ferramenta de vídeo não está automaticamente conectada por se ter lido a documentação.**

## 5. Código aberto — princípios inspecionáveis, sem copiar a implementação

- https://github.com/alaradirik/sd-interior-design — inpainting, segmentação e MLSD para redesenho de interiores.
- https://github.com/mithunparab/virtual-staging — Canny+Depth+segmentação/máscaras, com pipeline de staging.
- https://github.com/s-du/ScribbleArchitect — desenho/croqui e referência de estilo com ControlNet/IP Adapter.

**Estado:** lidos para entender mecanismos; NÃO instalados, executados, benchmarkados nem incorporados ao produto. Qualquer cópia de código exige verificação individual de licença e compatibilidade.

## 6. Diferença entre alegação e comprovação

| Afirmação | O que temos | Posição |
| --- | --- | --- |
| Prompt pode melhorar realismo de uma fachada | exemplos comunitários, orientações oficiais | plausível, exige teste no caso real |
| Prompt sozinho preserva cada porta/parede/cota | contraexemplos fortes | **não confiar** |
| ControlNet ajuda manter contornos e profundidade | documentação oficial + oficinas | fato do mecanismo; controle imperfeito |
| ChatGPT consegue igualar V-Ray em toda a obra | nenhum benchmark próprio ou prova geral | **não demonstrado** |
| Uma fachada única permite vídeo 360° fiel | depende de faces invisíveis | **não prometer** |
| Imagem AI '8K' porque o prompt diz '8K' | não há garantia de dimensão em pixels | **medir o arquivo real** |
| Uma renderização perfeita = aprovação técnica | não; imagens bonitas podem conter erros | **revisão indispensável** |

## 7. Síntese operacional priorizada

**Alta confiança por convergência:** base visual governando composição, papéis explícitos às referências, materiais/luz/câmera precisos, retoque localizado, guarda da origem, revisão antes de cliente.

**Alta utilidade, mas dependente de ferramenta:** ControlNet, segmentação, máscaras editáveis, profundidade, seed/denoise e upscale não generativo. Aprender o princípio sem alegar que controles estão disponíveis no ChatGPT nativo.

**Não comprovado aqui:** vantagem estatística de um prompt, de um modelo ou de um renderizador sobre todos os outros. O vencedor será medido em nossos materiais pela proporção de imagens aceitas com fidelidade preservada e retrabalho mínimo.

**Próximos passos:** usar [MÉTODO](METODO_RENDERS_CHATGPT_R2.md) e [BENCHMARK](BENCHMARK_VISUAL_R1.md). Nenhum cliente nem imagem sensível deve ser publicado neste GitHub público.

## 8. Transparência da pesquisa

O levantamento passou por 16 consultas exploratórias/temáticas no buscador Exa (até 160 resultados brutos solicitados, com muitos retornos repetidos ou marketing), complementadas por buscas direcionadas e abertura do Reddit e de documentações originais. Os exemplos nomeados acima foram selecionados **por relevância e rastreabilidade**, não por número de likes. Não houve inspeção de arquivos privados nem execução de geradores externos; nenhum nível de qualidade foi certificado por nós.