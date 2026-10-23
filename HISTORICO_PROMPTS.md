# Histórico do Prompt System

## 2026-10-23 — V1.0 — baseline editorial

**Natureza:** documentação/receitas; nenhum arquivo de cliente incluído.

- Definido o objetivo correto: ChatGPT como produtor das imagens, não apenas um banco de prompts.
- Criado protocolo de fidelidade versus conceito versus desenho técnico.
- Criadas nove receitas especializadas com campos variáveis e revisões por categoria.
- Adicionado pipeline responsável de vídeo de apresentação, condicionado a ferramenta realmente disponível.
- Criados briefing, checklist, registro JSON e catálogo de receitas com estados.
- Consolidadas fontes oficiais e repositórios públicos para manutenção e curadoria.

**Validação:** verificação de estrutura, presença de receita, URLs e JSON; nenhum teste de qualidade de imagem/vídeo foi realizado. O aplicativo V0.1 não foi alterado.

**Próxima comprovação necessária:** testar com pelo menos uma planta, fachada e interior de referências autorizadas; comparar entradas/saídas; documentar limites, falhas e correções; só então promover receitas para 'testado' e depois 'aprovado_cliente'.

## 2026-10-23 — Complemento R1: projetos externos + vídeo gratuito local

- Consulta e estudo de projetos GitHub para preservar arquitetura antes da estética, selecionar receita conforme imagem-fonte e criar rotinas de QA. Fichas em \`knowledge/INTEGRACOES_GITHUB_R1.md\` e \`knowledge/ROTEADOR_DE_RECEITAS_R1.md\`.
- Criados \`tools/video_local.py\` (FFmpeg sem API, custo zero de licenciamento) e \`tools/video_local_gui.py\`, além de \`INICIAR_VIDEO_WINDOWS.bat\` e manual para o disco D.
- A geração básica é **animação de imagens estáticas**, não inteligência artificial de vídeo. DepthFlow (paralaxe 2.5D) e geração IA local exigem verificação de hardware e licenças; não executadas/instaladas no PC Host.
- Um ensaio **manual** do pipeline FFmpeg no ambiente de teste usou duas imagens de referência e gerou um MP4 com 1280×720, 24 FPS, 7,5 segundos, H.264, sem áudio. O arquivo privado não foi publicado no GitHub. Em teste de montagem surgiu um erro de frame-rate ao adicionar \`fps,settb,setpts\` ao xfade: corrigido mantendo timebase dos clips previamente normalizados. A transição passou a funcionar nos testes manuais.
- Criados testes automatizados em \`tests/test_video_local.py\` para validações, composição e execução em ambiente com FFmpeg. **Ainda não executados no PC Host; não declarar aprovação operacional Windows.**
- Aplicativo Python V0.1 e API existentes preservados; nenhum pacote pesado, código de terceiro ou GitHub Actions instalado. A PR #1 continua Draft.

## 2026-10-23 — R3 — roadmap e método integrado da PR Draft

- Roadmap operacional unificado: entrada, roteador de nove receitas, geração de imagens, gate de geometria, comparador existente, registro privado e backlog controlado para máscaras/profundidade.
- Novo auxiliar `tools/metodo_integrado.py` com roteamento determinístico, preparação de variantes A/B/C e avaliação manual registrada na pasta privada `data/workflows/`.
- Testes do auxiliar adicionados a `tests/test_metodo_integrado.py`. **Não anunciar que passaram sem execução efetiva.**
- Caso piloto `AR-BENCH-001` criado, com seis tentativas **pendentes**: 0/6 nesta nova bateria. Não contar experimentos anteriores como repetição.
- **Sem instalação de repositórios terceiros**, sem alteração do app/base local V0.1, sem ações pagas ou GitHub Actions.
- Próximo bloqueio factual: localizar o arquivo original da cozinha/sala no contexto de execução e realizar comparações visuais reais; apenas a documentação não prova ganho de qualidade.



## 2026-10-23 — Curadoria pública de imagens e fóruns

- Autorização do usuário para **selecionar imagens públicas adequadas** e consultar de forma recorrente sites/fóruns/GitHub ao realizar lotes futuros do ArchRender Hub.
- [Manifesto das fontes](catalog/fontes_publicas_r1.json) contém 7 itens **com licença, autoria e origem documentadas**: 2 cenas 3D Blender (Classroom CC0 e Barcelona Pavillion CC BY) e 5 fotografias de cozinha, lavanderia e fachadas (Unsplash/Pexels).
- Documento [Curadoria Web R1](research/CURADORIA_WEB_IMAGENS_FORUNS_R1.md) fixa prioridade de evidência, revisão de licenças e diferencia referência geométrica, estética e foto de terceiros.
- `tools/metodo_integrado.py sources` lista as fontes offline; [testes estáticos de catálogo](tests/test_fontes_publicas.py) adicionados. **Nenhuma imagem baixada ou renderizada nesta etapa.**
- Discussões r/archviz, SketchUcation, Enscape/Chaos, documentação Blender/Poly Haven e licenças foram consultadas. Pesquisa pública reforça preservação de geometria e regras de QA; **relatos de fórum não são prova estatística de qualidade**.
- O benchmark privado da cozinha/sala continua 0/6 e não será contabilizado como concluído por esta curadoria.
