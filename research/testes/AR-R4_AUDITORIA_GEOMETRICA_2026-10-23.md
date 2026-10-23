# ArchRender Hub — R4, auditoria de geometria por contornos

Data: 23/10/2026. Escopo: **triagem diagnóstica; não é aprovação técnica de arquitetura**. Evidências de conteúdo, hashes privados e imagens dos clientes permanecem **fora do repositório GitHub**.

## Artefatos na PR Draft

- [Ferramenta offline de QA](../../tools/qa_geometria.py): Python com OpenCV/NumPy opcionais, compara duas imagens com Canny e tolerância espacial de 2 pixels, calcula recall/precision no quadro e em regiões retangulares especificadas pelo operador, registra dimensões e SHA-256 e gera um PNG visual com diferenças por contorno.
- [Seis testes unitários](../../tests/test_qa_geometria.py): mesma imagem, exposição ajustada, linha estrutural removida, resoluções diferentes, âncoras inválidas, fonte não modificada e proteção contra sobrescrita.
- Integridade verificada: blob da ferramenta no GitHub **97d557f2431b7516f144df23d7bd0bdb42ce4a13** e blob de testes **b5237ba1f80e52abefd2a7b482237dd9e8c32744**, ambos iguais aos resultados de git hash-object do código executado em container.
- Ferramenta separada do aplicativo V0.1: não altera SQLite, não usa rede, Docker, modelos, créditos nem GPU.

## Comandos e resultados realmente executados

Ambiente Linux, Python 3.13.5, OpenCV 4.13.0, CPU (não Windows/PC Host).

~~~bash
python -m py_compile tools/qa_geometria.py tests/test_qa_geometria.py
python -m unittest discover -s tests -v
~~~

A suíte isolada da ferramenta R4: **6/6 testes OK**. Os testes API da versão-base V0.1 (cujos blobs de app.py e test_api.py correspondem à branch): **6/6 OK**. Importante: **a suíte completa da branch não foi rodada**; esse resultado não a substitui. Também não houve homologação no Dell G15, que apareceu offline.

## Resultados mensurados sobre imagens originais privadas

Referências originais da cozinha/sala e lavanderia: 1536 x 864 px cada. Os controles fotométricos foram produzidos mantendo a resolução original e sem geração de objetos.

| Par original vs saída | Mesma resolução? | Recall de contornos (Canny, ±2px) | Precision | Classificação |
| --- | --- | ---: | ---: | --- |
| Cozinha vs refino local | sim | **99,528%** | 93,781% | conferência manual necessária |
| Lavanderia vs refino local | sim | **100,000%** | 81,241% | conferência manual necessária |
| Cozinha vs imagem gerada por texto | **não** (1672x941) | inaplicável em pixels originais | — | resoluções incompatíveis |

Uma versão redimensionada da geração textual foi processada **somente para diagnóstico**, com aviso explícito de que o redimensionamento não valida fidelidade. Nessa comparação, recall de bordas **26,455%** e precision **10,899%**; nas regiões: sofá **9,695%**, geladeira **11,527%**, janela/pia **30,370%**, bancada **10,190%**. Além disso, a imagem não possui vínculo comprovado com a fonte original, portanto foi rejeitada como teste de fidelidade. Esses números não comparam dois modelos em condições equivalentes nem provam dimensão arquitetônica.

No controle fotométrico da cozinha, recall por âncora: sofá **98,473%**, geladeira **100%**, janela/pia **99,375%**, bancada **99,211%**. Na lavanderia: vidro **100%**, tanque **100%**, lavadora **100%**. A região de parede lisa não tinha contornos suficientes: **não verificável**, em vez de aprovação falsa.

## Uso do analisador offline

~~~bash
python -m pip install numpy opencv-python
python tools/qa_geometria.py original.jpg resultado.png --anchor sofa:0.02,0.65,0.39,0.99 --anchor geladeira:0.48,0.30,0.60,0.87 --visual data/qa/diagnostico.png --json data/qa/avaliacao.json
~~~

A ferramenta não modifica originais, não sobrescreve saídas existentes e pode trabalhar sem redimensionamento. Se as dimensões não coincidirem, não calcula sobreposição, exceto com a opção explícita --resize-for-diagnostics, que mantém revisão manual obrigatória.

**Limitação fundamental:** métrica de contornos pode mudar com luz, sombras e texturas; não vê paredes sem contornos nem comprova uso efetivo da imagem pelo provedor. **Nunca converte automaticamente uma comparação em aprovação do cliente ou do projeto.** O gate de proveniência continua em tools/metodo_integrado.py.

## Pesquisa externa incorporada

- [Applied Sciences (outubro/2026), métricas de geração arquitetônica](https://www.mdpi.com/2076-3417/16/19/9877): SSIM e métricas de pixels não são a própria verificação de engenharia/arquitetura.
- [Architectural Intelligence (2026), comparação de workflows de condicionamento por imagem](https://link.springer.com/article/10.1007/s44223-026-00134-6): condicionamento da imagem é mais promissor para preservar referência visual do que texto isolado; métricas tradicionais podem divergir de avaliação visual.
- [npj Heritage Science (2026), reconstrução arquitetônica](https://www.nature.com/articles/s40494-026-02761-8): exemplo da necessidade de combinar métricas estruturais e avaliação morfológica.

As conclusões externas **não** são métricas internas do Hub.

## Gates seguintes

1. Executar suíte completa no checkout real da PR Draft (pendente).
2. Obter fluxo de edição por IA **realmente vinculado** à imagem original, não geração textual (pendente).
3. Rodar 3 métodos A/B/C, duas repetições por método, com arquivo original anexado e registro de proveniência — **0/6 tentativas válidas** neste benchmark.
4. Consolidar comparação humana e depois homologar o aplicativo e o Dell/Windows. Sem merge e sem GitHub Actions.

**Conclusão:** QA de contornos operacional e testado, dois pares fotométricos reais auditados, e um exemplo de reconstrução textual inelegível detectado. **Nenhuma renderização por IA foi homologada.**

## Adendo: nova tentativa de geração por IA após o R4

Foi realizada uma tentativa adicional de criar uma versão mais realista da cozinha no ChatGPT. A saída foi gerada com metadados da ferramenta indicando **edit_op=null** e **parent_gen_id=null**: **não há evidência de edição vinculada à imagem ORIGINAL**, mesmo que a cena descrita pareça arquitetônica.

- Fonte original privada: **1536 × 864 px**.
- Saída desta tentativa: **1672 × 941 px**.
- Gate de proveniência: **não comprovado**. A tentativa permanece **fora do benchmark A/B/C**; contagem **0/6**.
- O novo QA R4 sinalizou resoluções incompatíveis. Quando redimensionado **somente para triagem** (sem aprovação ou equivalência geométrica), registrou **Canny recall 29,081%** e **precision 10,699%**.
- Recall por âncora: **sofá 13,716%**, **geladeira 18,702%**, **janela/pia 30,995%**, **bancada 11,852%**.
- A saída textual alterou volumetria e objetos em relação à fonte. Este fracasso permanece documentado; não inventar avaliação positiva nem recomendar método vencedor.

**Próxima decisão:** interromper tentativas textuais que não conseguem anexar a imagem original como entrada real. Só retomar benchmark generativo com ferramenta que aceite explicitamente image-to-image e forneça evidência de vínculo. Enquanto isso, aprimoramentos fotométricos e QA continuam utilizáveis sem redesenho.
