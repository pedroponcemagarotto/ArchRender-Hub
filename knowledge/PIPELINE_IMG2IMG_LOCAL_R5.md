# ArchRender Hub — R5: edição por imagem original + máscaras (gratuita/local)

**Situação em 23/10/2026:** opção pesquisada, módulo de composição implementado e testado com referências reais. **O motor de IA local Krita/ComfyUI não foi instalado nem homologado no Dell G15.** Não afirmar que houve geração de IA fiel aprovada.

## 1. Por que esta arquitetura?

Testes anteriores com o gerador do ChatGPT retornaram metadados `edit_op=null` e produziram **cenas novas**, não versões comprovadamente editadas do render original. A etapa A/B/C real permanece **0/6**.

Para obter referência visual vinculada, o motor deve trabalhar com **imagem de entrada efetiva** e, quando necessário, máscara/contornos. O fluxo escolhido é:

**render original (privado) → Krita AI Diffusion/ComfyUI (imagem de entrada, máscara e condicionamento) → candidato gerado → compositor R5 que preserva pixels fora da máscara → comparador R4 e revisão humana → relatório R3 com proveniência real → aprovação opcional.**

> Compor uma imagem não demonstra que a IA usou a referência, nem garante que uma parede dentro da área editada ficou correta. Por isso permanecem separados os gates de **vínculo ao original**, **impossibilidade de alterar áreas bloqueadas** e **correção arquitetônica**.

## 2. Opção recomendada: Krita AI Diffusion + ComfyUI

**Documentação oficial consultada:**

- [Krita AI Diffusion — projeto oficial](https://github.com/Acly/krita-ai-diffusion)
- [Instalação e requisitos do Krita AI Diffusion](https://docs.interstice.cloud/installation/)
- [ComfyUI — Image to Image](https://docs.comfy.org/tutorials/basic/image-to-image)
- [ComfyUI — Inpainting e edição de máscara](https://docs.comfy.org/tutorials/basic/inpaint)
- [ComfyUI — ControlNet](https://docs.comfy.org/tutorials/controlnet/controlnet)

**Características relevantes:** Krita fornece canvas editável, seleção, máscaras e correção localizada; ComfyUI executa modelos locais com nó **Load Image**, força **denoise** e modelos de inpainting/ControlNet. É possível editar sem transmitir arquivos a um gerador na nuvem usando backend local, mas o usuário precisa baixar programas e pesos de modelos. Em Krita AI Diffusion, o servidor local é opção independente do serviço em nuvem.

**Hardware do usuário:** Dell G15, NVIDIA RTX 3060 ~6 GB VRAM, 16 GB RAM. A documentação do Krita indica NVIDIA RTX 2060 ou melhor, mas **isso não comprova desempenho estável deste Dell**. Em 16 GB de RAM, começar com **um único processo, modelo SD 1.5 pequeno compatível, canvas reduzido e uma região**. Não instalar grandes modelos Z-Image/Flux ou SDXL como primeiro teste. Manter arquivos e cache no disco D: quando este for SSD e tiver espaço disponível.

### Checklist do PC Host, quando estiver acessível

1. Conferir disponibilidade, espaço no D:, controlador NVIDIA e RAM; fechar aplicativos pesados quando necessário. Não apagar nem mover arquivos sem inventário/segurança.
2. Instalar Krita oficial e plugin oficial Krita AI Diffusion, usar **servidor local** (não assinatura em nuvem). Confirmar licenças de cada modelo selecionado, incluindo usos comerciais.
3. Instalar somente o conjunto de modelos necessário para **SD 1.5 inpainting**. Evitar 4K no primeiro teste; começar com **512 a 768 px** na maior dimensão de uma **região/crop**. Documentar dimensões, VRAM e tempo reais. Não assumir que o serviço preserva integralmente as áreas não mascaradas.
4. Abrir o **arquivo original**, não render IA modificado. Delimitar **uma área pequena** que possa receber microtextura/luz sem mudar paredes, vãos ou mobiliário fixo. Capturar máscara binária como PNG grayscale **no mesmo tamanho do original**.
5. Gerar um candidato com ferramenta verdadeira img2img/inpaint, registrar o modelo/código/versão/caminho privado, denoise escolhido e um identificador de execução. **Escolha inicial de pesquisa (não homologada): denoise 0,15 a 0,35**; observar deriva. Escolher intensidade pela inspeção, não por promessa de fidelidade.
6. Exportar candidato e máscara para 1536 × 864 (resolução exata do original), **sem reposicionar, distorcer ou aplicar crop independente**. Se o processo gerar crop local, reintegrá-lo na tela original no Krita antes de exportar. O compositor R5 recusará dimensões divergentes.
7. Usar o compositor R5 para recuperar os pixels originais fora das regiões autorizadas. Eventualmente usar segunda máscara **protected** para bloquear geladeira, esquadrias, sofá, porta, banca, janela e outros elementos sensíveis, mesmo que cruzem a região editável.
8. Executar **QA R4** por contornos global + âncoras e conferência visual da imagem em 100% de zoom. Se qualquer alteração de geometria visível ocorrer, reprovar e ajustar regiões/denoise.
9. Registrar `bind`/QA do R3 com evidência **real** de carga da imagem original no gerador. O sistema jamais concede aprovação do cliente automaticamente.

**Importante:** Krita, ComfyUI e modelos podem mudar de disponibilidade. A documentação de instalação menciona downloads de pelo menos **10 GB**, podendo exceder **50 GB** com pacotes opcionais. Evitar instalação indiscriminada.

## 3. Compositor de pixels R5 — implementado

Ferramenta: [`tools/compor_edicao_mascarada.py`](../tools/compor_edicao_mascarada.py). Usa apenas Pillow; **não gera imagem por IA**, apenas combina um candidato existente e a referência original, com permissão explícita por máscara.

**Entradas:**
- `original`: JPG/PNG/WebP privado, câmera/geometria mestre;
- `candidate`: resultado real de IA img2img ou edição local, **exatamente a mesma resolução**;
- `mask`: PNG em grayscale (branco pode alterar; preto impede qualquer alteração);
- `protected-mask` opcional: branco/tom positivo significa **bloqueio rígido**; tem prioridade sobre a máscara de edição.

**Saída:** PNG sem perdas e relatório com hashes SHA-256 e contagem zero de pixels alterados em zonas bloqueadas. A verificação é feita sobre os **pixels decodificados RGBA**, e não por bytes do arquivo original JPEG. Máscara autorizada limitada a 50% da área por padrão, com ajuste explícito do teto até 95%; feather suaviza somente **dentro** das regiões autorizadas. Nunca sobrescreve entrada nem resultado já existente.

```bash
python -m pip install pillow
python tools/compor_edicao_mascarada.py \
  data/privado/cozinha-original.jpg \
  data/privado/cozinha-candidato.png \
  data/privado/mascara-editavel.png \
  data/privado/cozinha-final.png \
  --protected-mask data/privado/mascara-ancoras-bloqueadas.png \
  --feather 9 \
  --report data/privado/relatorio-compositor.json
```

**Condicionante crucial:** a máscara é um artefato de **autorização de edição**, não uma prova de que a imagem candidata é correta. Se o gerador alterar uma porta **dentro** da área branca, o compositor a aceitará; o QA manual continua obrigatório. Preferir áreas pequenas e proteger todos os elementos arquitetônicos fixos.

## 4. Piloto realmente executado, sem IA generativa

Para validar o mecanismo antes de instalar ComfyUI, foi usada a **cozinha original privada de 1536 × 864 px** e uma imagem candidata produzida anteriormente por **ajustes locais não generativos de luz/cor**, ambas exatamente na mesma vista. A máscara editável de demonstração cobriu uma região ampla da parede esquerda; a proteção por polígono blindou o sofá.

Resultado validado numericamente: **418.142 pixels** alterados **dentro** da região autorizada, **zero pixels** alterados **fora** dela, **zero pixels** alterados na máscara protegida; dimensão final **1536 × 864**. Preservados os bytes do arquivo original. Esse resultado só comprova a proteção de pixels, **não o desempenho de modelo de IA ou fidelidade de geometria editada**.

- Testes do R5: **10/10 aprovados** localmente no Python 3.13.5 (Linux).
- Testes de QA R4: **6/6 aprovados** localmente (mesma cópia verificada).
- Integridade do código: SHA do blob GitHub `ebb3f725e208fd31e102540c5c815fabf5a16ec9`; arquivo de testes `51b892719f0f331f63ded36256e641a64bcf5dab`, ambos confrontados com `git hash-object` do código executado localmente.
- **Não** significa que a suíte completa de todas as ferramentas da PR foi validada no checkout real.

## 5. Segurança, licenças e escopo

Não copiar imagens de clientes para GitHub público, não fazer upload involuntário para serviços de IA, não expor interface ComfyUI na rede local/internet sem autenticação, não colocar tokens/chaves no repositório. As cópias de demo, máscaras, arquivos intermediários e hashes de mídia privada permanecem fora do GitHub. Se o usuário preferir ChatGPT somente, a edição nativa pode ser tentada quando o contexto aceitar **a imagem original como entrada real**, mas **não simular** esse vínculo por texto.

Não instalar modelos nem frameworks até verificação de recursos no PC Host e eventual consentimento do usuário caso haja licenças, download substancial, uso de rede ou custo. **Sem GitHub Actions, sem merge da PR, sem dependência da Incubadora Remote V2.**

## 6. Próximo gate e status

| Etapa | Status |
| --- | --- |
| R5 script de composição e regras de proteção | **implementado**, teste local 10/10 |
| R5 exemplo com original/candidato não generativo | **executado**, 0 alterações fora das máscaras |
| R5 plugin/ComfyUI no Dell G15 | **não instalado, não testado**, host indisponível |
| R3 benchmark A/B/C com fonte vinculada | **0/6**, não iniciado validamente |
| QA arquitetônico completo de gerações com IA | **não homologado** |

**Princípio:** não transformar uma cena completamente diferente em suposto projeto aprovado. A geração deve operar **na imagem fonte original** e a máscara deve limitar o que pode aparecer no resultado.
