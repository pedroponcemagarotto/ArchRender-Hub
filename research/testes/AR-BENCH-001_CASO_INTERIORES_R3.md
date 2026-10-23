# AR-BENCH-001 — primeiro benchmark de imagens (cozinha/sala)

**Data:** 2026-10-23  
**Estado:** PREPARADO, NÃO EXECUTADO. **0/6 imagens** produzidas nesta bateria; nenhum resultado aprovado.  
**Metodologia:** [Roadmap operacional R3](../../ROADMAP_OPERACIONAL_INTEGRADO_R3.md), [Benchmark visual R1](../BENCHMARK_VISUAL_R1.md), [receita de interiores](../../knowledge/prompts/04_interiores.md).

## Identidade e fonte

- `input_reference_private`: `REF-COZINHA-ORIGINAL-001` (identificador abstrato; **não** o nome de cliente ou URL de foto).
- Fonte verdadeira: imagem ORIGINAL (antes de qualquer geração de IA), armazenada fora do GitHub público.
- Objetivo: transformar visualização em fotorrealismo, mantendo a cozinha e sala como desenhadas.
- Modo: **F** (fiel), não é proposta de reforma/redesenho.
- Imagens de estilo auxiliares não podem substituir geometria, câmera ou mobiliário.
- Inspecionar a fonte ao iniciar; não presumir medidas.

## Inventário preliminar — validar contra os pixels originais

| Ponto de controle | Exigência | Status |
| --- | --- | --- |
| Sofá à esquerda | mesmo formato, posição e cor definida | não verificado nesta bateria |
| Geladeira inox central | mesmo alinhamento e proporção | não verificado nesta bateria |
| Bancada e pia | posições inalteradas | não verificado nesta bateria |
| Armários verde-azulados | volumes, portas e posicionamento estáveis | não verificado nesta bateria |
| Janela de esquadria escura à direita | número e posição idênticos | não verificado nesta bateria |
| Corredor/fundo | mesma abertura e geometria | não verificado nesta bateria |
| Iluminação e decoração visíveis | sem acrescentar novas luminárias/objetos | não verificado nesta bateria |
| Câmera | mesmo ângulo, recorte e pontos de fuga | não verificado nesta bateria |

Se o original revelar diferença, **corrigir este inventário ANTES de gerar**. Não confundir a cozinha/sala com a outra imagem de lavanderia; são trabalhos independentes.

## Três hipóteses que vamos testar

### A — prompt mínimo (baseline)

```text
Parta exclusivamente da imagem ORIGINAL anexada e transforme sua aparência em
uma visualização arquitetônica fotorrealista. Melhore apenas realismo dos
materiais e iluminação natural. Preserve a composição geral, o desenho e a câmera.
Não adicione elementos.
```

### B — receita especializada

Usar `AR-INT-001` de `knowledge/prompts/04_interiores.md`, com papéis de fontes, lista de elementos protegidos, especificação de luz/material e câmera. Não alterar a arquitetura. Gerar a partir da MESMA imagem original.

### C — método completo com QA

Usar a mesma receita de B, mas acrescida do contrato de âncoras arquitetônicas, limites precisos do que pode variar e revisão comparativa de original e resultado; corrigir só quando uma região definida puder ser tratada sem deformar o restante.

**Controle:** mesmas referência, ferramenta real, proporção de saída e intenção estética nos testes. Não afirmar seed/modelo interno se não informado pela ferramenta. Duas repetições por variante são exploratórias, sem inferência estatística.

## Execuções planejadas — registrar sem fabricar resultados

| Tentativa | Abordagem | Resultado | Gate geométrico | Nota editorial | Observações |
| --- | --- | --- | --- | --- | --- |
| AR-I-A-01 | A | não gerado | não avaliado | — | — |
| AR-I-A-02 | A | não gerado | não avaliado | — | — |
| AR-I-B-01 | B | não gerado | não avaliado | — | — |
| AR-I-B-02 | B | não gerado | não avaliado | — | — |
| AR-I-C-01 | C | não gerado | não avaliado | — | — |
| AR-I-C-02 | C | não gerado | não avaliado | — | — |

## Protocolo de inspeção após cada geração

1. Conferir imagem, proporção, resolução real e se a ferramenta foi de fato utilizada.
2. Alinhar visualmente original versus resultado e contar vãos, paredes, marcenaria, mobiliário fixo e linhas de perspectiva.
3. Gate crítico F: **falha em qualquer âncora estrutural → REPROVADO**; nunca compensar falha por nota de realismo.
4. Só com geometria aprovada avaliar luz, sombras, reflexos, textura, materiais, composição, artefatos em nota 0–100 (rubrica no Benchmark R1).
5. Registrar retrabalho e problemas específicos em relatório privado, sem imagens de cliente no GitHub.
6. Comparar medianas/taxas exploratórias; declarar vencedor somente após seis resultados inspecionados e registrar também quando A superar B/C.

## Critério de saída do lote

- **6/6 imagens** geradas e inspecionadas de forma rastreável.
- Quadro com divergências estruturais por tentativa.
- Melhor variante escolhida por evidência; registrar revisão do prompt se necessária.
- Nenhuma imagem ou registro com cliente publicado no repositório.
- A próxima bateria na lavanderia só começa depois de consolidar aprendizados desta.

**NOTA:** Os testes `AR-TESTE-001` e `AR-TESTE-002` anteriores foram experimentos distintos. NÃO contabilizá-los como execução do benchmark A/B/C aqui.
