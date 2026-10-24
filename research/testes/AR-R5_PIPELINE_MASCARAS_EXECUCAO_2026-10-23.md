# ArchRender Hub — R5: execução real de máscaras e QA integrado

**Data:** 23 de outubro de 2026.  
**Branch:** `feat/prompt-system-v1`, PR #1 Draft, sem merge na `main`.  
**Status técnico:** nova proteção por máscaras e pipeline offline implementados. **Ainda não há geração de imagem por IA vinculada ao original homologada**; benchmark generativo A/B/C permanece **0/6**.

## 1. Componentes integrados

| Componente | Implementação | Testes executados |
| --- | --- | ---: |
| API V0.1 original (intacta) | `app.py`, `tests/test_api.py` | 6 |
| Roteador de receitas e proveniência R3 | `tools/metodo_integrado.py`, `tests/test_metodo_integrado.py` | 11 |
| Catálogo de licenças/fontes públicas | `tests/test_fontes_publicas.py` | 5 |
| Ajuste fotométrico local sem IA | `tools/refino_fotometrico.py`, `tests/test_refino_fotometrico.py` | 4 |
| Detecção diagnóstica de contornos R4 | `tools/qa_geometria.py`, `tests/test_qa_geometria.py` | 6 |
| Compositor de pixels e máscaras R5 | `tools/compor_edicao_mascarada.py`, `tests/test_compor_edicao_mascarada.py` | 12 |
| Orquestrador de composição/QA R5 | `tools/pipeline_img2img_r5.py`, `tests/test_pipeline_img2img_r5.py` | 8 |
| **Total executado** | **ambiente Linux, Python 3.13.5** | **52/52 OK** |

**Limite metodológico da execução:** foi utilizada uma reconstrução local dos **arquivos de código/teste com hashes Git idênticos aos da PR**, mas os nove arquivos Markdown de receitas e o catálogo de fontes públicas foram substituídos por **fixtures compatíveis** para testar lógica e segurança. Não chamar isso de execução da árvore completa exata do repositório. Os testes de vídeo e a homologação no Windows/PC Host não entraram nesta bateria. A comparação do comportamento das receitas originais com seus conteúdos completos continua pendente.

**Código verificado:**
- `tools/metodo_integrado.py` Git blob `60cffab196b78c0c4c758b501ce9ef0235d09373`;
- `tests/test_metodo_integrado.py` Git blob `00fffa5f141b6631346c3f03732bd7e649c38087`;
- `tools/qa_geometria.py` `97d557f2431b7516f144df23d7bd0bdb42ce4a13`;
- `tools/refino_fotometrico.py` `180c090077ed8c5d1fec9251e5939754b8d33fcc`;
- `tools/compor_edicao_mascarada.py` `9bdb6f40b02d0a8e1ca1661ebc1114681dee2db1`;
- `tests/test_compor_edicao_mascarada.py` `15ec72471e1aa2a212f8126126c40242ed12705f`;
- `tools/pipeline_img2img_r5.py` `9432602605ed01ac0ddb51a7034a72c7b8301abb`;
- `tests/test_pipeline_img2img_r5.py` `c1a159882a467bed1da006fe75dda52f29299d14`.

Hashes acima são de **código e testes públicos**, não de imagens particulares.

## 2. Primeiro piloto do orquestrador, com imagens privadas e sem IA generativa

Entrada real: **cozinha original**, 1536 × 864. Candidata: ajuste **fotométrico local** do mesmo render, sem novos objetos. Máscara branca autorizou uma região da parede; máscara protegida vermelha bloqueou completamente o sofá, mesmo quando parte dele estava sobre a região editável.

**Resultado mensurado:**
- 31,5079% dos pixels ficaram na área de edição autorizada depois da proteção.
- Houve **418.142 posições de pixel alteradas** no total; todas dentro das áreas autorizadas.
- **0** posições de pixel alteradas fora da máscara; **0** dentro da máscara protegida.
- Resolução final manteve **1536 × 864**; entrada preservada.
- QA por contornos Canny, tolerância ±2 pixels: `recall` global **1,00000** e `precision` **0,99675**. Três âncoras (sofá, geladeira, janela/pia) tiveram recall **1,00000** no par analisado. **Isto não equivale a certificar a arquitetura** — textura/sombra/áreas lisas influenciam contornos.
- O pipeline registrou status **`aguarda_revisao_humana`**; `client_approved=false`, `benchmark_completed=false`, `generation.mode=local_color`, `binding_status=nao_comprovado` (não é IA img2img).

**Mídias e relatórios detalhados ficam fora do GitHub público**; apenas resumo sem imagens e sem hash de imagem foi publicado.

## 3. Comando operacional do pipeline

Exige Pillow, OpenCV e NumPy. O original, a candidata e a máscara precisam existir, estar acessíveis **localmente** e manter as mesmas dimensões.

```bash
python tools/pipeline_img2img_r5.py \
  --original data/privado/original.jpg \
  --candidate data/privado/versao-editada.png \
  --mask data/privado/area-editavel.png \
  --protected-mask data/privado/area-bloqueada.png \
  --output data/privado/versao-final.png \
  --reference-id ref-cozinha-001 \
  --task interiores --variant C \
  --preserve "geladeira e janela originais" \
  --anchor sofa:0.01,0.62,0.41,0.99 \
  --candidate-mode unknown
```

A opção `--candidate-mode unknown` **não prova uso da fonte**. Somente marcar `image_edit` quando a ferramenta externa realmente tiver editado a imagem original e houver evidência para inspeção manual; ainda assim a aprovação não ocorre automaticamente.

## 4. Próximos gates — não homologados

1. Recuperar checkout exato com 9 receitas reais, manifesto real, testes de vídeo e executar **toda a suíte**; depois repetir no Dell/Windows.
2. Instalar/validar Krita AI Diffusion + ComfyUI com entrada real da imagem, máscara e modelo compatível com RTX 3060 6GB/16GB RAM (PC Host estava offline).
3. Registrar metadata de input/output reais, engine, modelo, parâmetros, custo, hashes privados e diagnóstico com âncoras.
4. Rodar **6 edições reais A/B/C** com fonte vinculada e comparar as falhas estruturais e a qualidade fotográfica. **0/6** nesta fase.
5. Manter a PR #1 Draft, sem GitHub Actions, sem merge e sem upload de imagens pessoais/arquitetônicas privadas.

**Referências técnicas:** [Krita AI Diffusion](https://github.com/Acly/krita-ai-diffusion), [instalação](https://docs.interstice.cloud/installation/), [ComfyUI img2img](https://docs.comfy.org/tutorials/basic/image-to-image), [ComfyUI inpainting](https://docs.comfy.org/tutorials/basic/inpaint). A implementação detalhada está em [PIPELINE_IMG2IMG_LOCAL_R5.md](../../knowledge/PIPELINE_IMG2IMG_LOCAL_R5.md).
