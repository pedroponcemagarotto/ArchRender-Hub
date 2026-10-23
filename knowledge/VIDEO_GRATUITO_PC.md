# Como criar vídeos arquitetônicos GRATUITOS no próprio PC

**Rota recomendada:** imagens aprovadas pelo usuário + ArchRender Hub + FFmpeg local.  
**Sem mensalidade, conta de API, créditos, marca-d'água ou upload automático.** Custos materiais da máquina (energia, disco, conexão inicial para instalar programas) são de responsabilidade do usuário.

## Tipo de vídeo e custo

| Caminho | Resultado possível | Hardware | Situação no ArchRender Hub |
| --- | --- | --- | --- |
| **FFmpeg** (gratuito) | apresentação MP4 com pans, zooms suaves e transições de renders aprovados | CPU comum, Windows com Python e FFmpeg; sem GPU obrigatória | **Implementado** em \`tools/video_local.py\` + GUI |
| [Shotcut](https://shotcut.com/) (grátis/código aberto) | editar cortes, texto, músicas próprias/licenciadas, correção de cor, exportação | PC comum | indicado para finalização, sem integração automática |
| [DepthFlow](https://github.com/BrokenSource/DepthFlow) (AGPL-3.0) | paralaxe 2.5D a partir de imagem e profundidade estimada | exige recursos gráficos compatíveis; depende de requisitos do programa | integração **planejada**, não instalada |
| [Blender](https://www.blender.org/) (grátis) | movimento de câmera 3D autêntico com modelos .blend/FBX/GLB etc | depende da cena; render CPU é possível, GPU pode acelerar | fluxo futuro quando houver modelo 3D |
| [LTX Desktop](https://github.com/Lightricks/LTX-Desktop) | IA local para image-to-video se hardware/licenças permitirem | **GPU forte e muito espaço no SSD**, recursos variam por versão | **não instalado**, avaliar após inventário |

**Vídeo local FFmpeg não é vídeo generativo**: não gera pessoas andando, folhas se movendo ou novas perspectivas. Pan e zoom percorrem os pixels da imagem original; ao aproximar, bordas podem sair do enquadramento. Para um passeio arquitetônico real, use um modelo 3D e a câmera do Blender/SketchUp (conforme exportações permitidas). Vídeo generativo pode inventar objetos e cômodos; exigir aprovação frame a frame.

## Instalação Windows — caminho simples

1. Tenha Python 3.9+ instalado (o Hub V0.1 já usa Python; confira \`py -3 --version\`).
2. Baixe FFmpeg exclusivamente pelo site [ffmpeg.org/download.html](https://ffmpeg.org/download.html), seguindo um distribuidor Windows listado oficialmente. Extraia e adicione a pasta \`bin\` com \`ffmpeg.exe\` ao PATH, ou selecione o executável na interface do Hub. Confira \`ffmpeg -version\` no terminal.
3. Use uma pasta do **disco D:** para projetos e MP4, se existir.
4. No repositório, dê dois cliques em **\`INICIAR_VIDEO_WINDOWS.bat\`**. Não precisa de \`pip install\`, Docker, chave de API, GitHub Actions nem GPU.
5. Clique **Adicionar** para selecionar PNG/JPG. Suba/desça arquivos para definir a ordem. Escolha \`720p\` para começar, 4–5 segundos por imagem, transição \`dissolve\` e movimento \`auto\`.
6. Clique **Gerar vídeo MP4**. Escolha uma pasta de destino (exemplo: \`D:\ArchRender\Videos\apresentacao.mp4\`). Arquivos preexistentes **não serão substituídos**.
7. Abra o MP4 em um player; se quiser títulos, identidade visual e música licenciada, use Shotcut. Nunca insira trilha sem direito de uso.

### Linha de comando (opcional)

~~~bat
py -3 tools\video_local.py -o "D:\ArchRender\Videos\apresentacao.mp4" --size 720p --seconds 4 --transition dissolve "D:\ArchRender\Imagens\fachada.png" "D:\ArchRender\Imagens\sala.jpg"
~~~

Formatos: entrada PNG, JPG, WebP e BMP; saída MP4 H.264 sem áudio por padrão. Aceita música local autorizada com \`--audio caminho.mp3\`. Para vertical social, \`--size vertical\` (1080x1920). \`--size preview\` (640x360) é exclusivo da CLI para testes. Máximo 20 imagens, 2–12 segundos por imagem. \`--motion still\` desliga o movimento.

O pipeline produz arquivos de vídeo intermediários em pasta temporária, com \`ffmpeg\`, e a remove automaticamente. **Nada é enviado à internet pelo script**. A licença do FFmpeg depende da build baixada; a do nosso código é a licença MIT do Hub.

## Opcao com IA real: FramePack (RTX 3060)

**Verificado nas especificacoes oficiais em 23/10/2026:**
- A Dell informa que o G15 5515/5511 com **RTX 3060 possui 6 GB de VRAM GDDR6** (o modelo G15 exato do usuario ainda nao foi consultado).
- O autor do [FramePack (GitHub OFICIAL)](https://github.com/lllyasviel/FramePack) exige **NVIDIA RTX 30xx/40xx/50xx com ao menos 6 GB VRAM**; laptops RTX 3060 sao contemplados. Ele tambem afirma que esses laptops sao varias vezes mais lentos do que um desktop RTX 4090; o tempo real depende de RAM, drivers e disco.
- Windows e Linux suportados. O pacote Windows instala modelos **acima de 30 GB** por download; nao instalar sem checar espaco livre e memoria RAM. Com 16 GB de RAM, offloading pesado pode causar lentidao ou falta de memoria; 32 GB ou mais e recomendacao operacional prudente, nao requisito minimo oficial confirmado.
- **Licenca:** o codigo FramePack foi identificado como Apache-2.0 no GitHub, **mas** os pesos HunyuanVideo seguem a [Tencent Hunyuan Community License](https://huggingface.co/tencent/HunyuanVideo/raw/main/LICENSE), diferente de Apache. Conferir direitos de uso, territorios e termos se for usado comercialmente.
- Os autores **alertam sobre sites falsos** que se passam por FramePack; baixar apenas em https://github.com/lllyasviel/FramePack . Nao abrir pacotes de sites "framepack-ai" nao oficiais.
- O modelo realmente **sintetiza frames novos** a partir de uma imagem, como movimento de camera e elementos. E muito mais proximo de video generativo que FFmpeg/DepthFlow, mas pode distorcer esquadrias, mudar superficies e inventar geometria oculta. Testar curtas sequencias de 3 a 5 segundos com camera discreta, e inspecionar quadros inicial, medio e final contra referencia.

**Decisao:** FramePack e o primeiro **candidato local gratuito de IA gerativa de video** a ser homologado no Dell G15 RTX 3060; **nao instalado, nao executado, sem promessa de qualidade ou velocidade**. Medir RAM, VRAM, SSD livre em D:, driver/CUDA e versao real do Windows primeiro. Nao alterar outros projetos do PC.

**Caminho de producao quando o PC estiver disponivel:**
1. ChatGPT gera/refina imagens e usuario aprova o layout.
2. FramePack gera planos individuais curtos a partir dessas imagens (IA, com aviso de possiveis alteracoes).
3. DepthFlow e a alternativa **nao generativa** com paralaxe quando a preservacao importa mais.
4. Hub/FFmpeg une planos em MP4, exporta e valida duracao/fps/resolucao; Shotcut adiciona titulos e trilha licenciada.

A qualidade editorial vem principalmente da **imagem-base**, da fidelidade das vistas e da continuidade entre planos. **Ter RTX 3060 nao melhora sozinho qualidade da fonte ou "transforma 720p em 4K real".** O gerador atual \`tools/video_local.py\` usa libx264 na CPU; a GPU NVENC ainda nao esta integrada nesse script. NVENC acelera codificacao, nao adiciona realismo.

## Etapas para elevar a qualidade sem pagar

**Nível 1 — imediato e leve:** FFmpeg + ChatGPT gera/avalia as imagens + Shotcut edita o MP4.

**Nível 2 — maior profundidade:** instalar e testar DepthFlow localmente, exportar shots curtos com pequena paralaxe e juntar os MP4 finais. Verificar requisitos de placa gráfica e licença AGPL antes de incorporar ou distribuir código.

**Nível 3 — movimento real da câmera:** usar Blender com o arquivo 3D de origem, evitando geometria inventada. Renderizar shots na resolução alvo e editar no Shotcut/FFmpeg.

**Nível 4 — IA geradora de vídeo no PC:** avaliar LTX Desktop conforme GPU NVIDIA/CUDA, memória VRAM, RAM, espaço livre e licença vigente. Versões oficiais publicadas em 2026 pedem recursos altos para execução local (em geral dezenas de GB de VRAM e armazenamento extenso). Recursos de API/cloud podem cobrar; **não utilizar** em nosso modo 'custo zero'. Não instalar modelos pesados antes da conferência real do PC.

## Validação antes da entrega

- [ ] Todas as imagens usadas estavam aprovadas (geometria e uso permitido).
- [ ] Nenhum shot mostra vistas/cômodos não documentados.
- [ ] O vídeo mantém a sequência aprovada e não estica/recria pixels estruturalmente.
- [ ] MP4 existe e foi reproduzido; largura/altura, duração, FPS e áudio conferidos.
- [ ] Títulos são corretos; trilhas e fontes têm licença apropriada.
- [ ] Método declarado: animação 2D de imagens; paralaxe 2.5D; passeio 3D; ou geração IA.
- [ ] Imagens e MP4 de clientes estão armazenados fora do GitHub público.

## Limitações e privacidade

- O programa não recupera materiais além do que aparece nas fotos nem pode comprovar dimensões da arquitetura.
- O método preserva pixels existentes e **não produz** animação dos objetos. Algumas bordas saem de quadro durante zoom/pan; o shot ainda é uma edição da imagem original.
- A interface não é serviço web: o vídeo é renderizado no computador onde o programa foi aberto.
- Se FFmpeg não for encontrado, informe o caminho para o \`ffmpeg.exe\` em vez de baixar executáveis de fontes desconhecidas.
- Antes de rodar DepthFlow, LTX Desktop ou Blender, verifique hardware, licenças e segurança; eles **não** são dependências obrigatórias do Hub.

**Estado do PC Host em 23/10/2026:** conector Desktop Commander informou o PC como offline no momento da verificação. Não foi possível conferir GPU, RAM ou espaço livre; por isso a implantação nesse PC não foi testada. Nenhum programa foi instalado nele.

**Fontes:** [FFmpeg](https://ffmpeg.org/ffmpeg-filters.html), [Shotcut](https://shotcut.com/), [Blender](https://www.blender.org/features/video-editing/), [DepthFlow](https://github.com/BrokenSource/DepthFlow), [LTX Desktop](https://github.com/Lightricks/LTX-Desktop).
