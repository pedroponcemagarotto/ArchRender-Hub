# R3-04 — diagnóstico com fontes originais e controle fotométrico

**Data:** 23/10/2026 · **Natureza:** relatório de experimento inicial, sem imagens publicadas no GitHub.  
**Status de benchmark oficial A/B/C:** ainda **0/6 imagens válidas para a rodada A/B/C**. O que aparece abaixo é uma **investigação prévia de conectividade da referência** e um **controle não generativo**. **Nenhum método vencedor declarado.**

## 1. Fontes verdadeiras e privacidade

Duas fontes originais do usuário foram encontradas no ambiente de trabalho privado:

- `AR-SRC-COZINHA-001`: 1536 × 864 px, cena de sala/cozinha integrada.
- `AR-SRC-LAVANDERIA-001`: 1536 × 864 px, lavanderia com tanque e lavadora.

**Arquivos binários, nomes originais, hashes de fontes e imagens de resultado ficaram fora do repositório público.** Não usar imagem recriada pela IA como se fosse original.

## 2. Diagnóstico de geração IA — obrigatório reprovar

O mecanismo de geração tentou produzir imagens de cozinha/sala, mas os dois arquivos gerados retornaram **`edit_op: null` / `parent_gen_id: null`** no metadata da ferramenta, e foram apresentados como **gerações novas por texto**, não edições comprovadamente ancoradas nos pixels originais.

Na comparação visual com a referência real, as saídas apresentam diferenças estruturais evidentes: **armários superiores, novas portas e corredores, novas esquadrias, alteração da posição/dimensões aparentes do sofá e bancada, novos aparelhos/mobiliário**, além de ângulo de câmera diferente. **Gate geométrico: FALHOU** para qualquer alegação de fidelidade ao projeto original.

Foi produzida ainda uma ilustração de quadro comparativo gerado automaticamente com pontuações e método vencedor. **Ela NÃO representa mensuração**, pois a base apresentada não corresponde às fontes originais, e as notas foram fabricadas pelo gerador. Desconsiderar totalmente essas notas e NÃO publicar a ilustração como prova.

**Consequência no código:** `tools/metodo_integrado.py` adicionou o registro de SHA-256 real de entrada e saída (`bind`) e um gate **`nao_elegivel_sem_referencia`** quando não há vínculo entre arquivo editado, metadados de ferramenta e inspeção humana da origem. `text_to_image` e `unknown` nunca são aprovados como testes de fidelidade geométrica. Uma afirmação humana de vínculo não equivale a uma verificação criptográfica do provedor; a revisão humana continua obrigatória.

## 3. Controle reproduzível sem IA — refino de pixels

Para não ficar parado com a falha de vínculo na IA, foram criados **dois resultados reais** com operações locais determinísticas, não generativas:

| Cenário | Fonte (px) | Resultado (px) | Método | Diagnóstico técnico |
| --- | --- | --- | --- | --- |
| Cozinha/sala | 1536 × 864 | 1536 × 864 | brilho, contraste, saturação, gamma e nitidez muito leve | ~**99,6%** dos contornos do original encontrados a até **2 px** no resultado; diferença média absoluta RGB = **(11,446; 9,454; 8,039)** por canal |
| Lavanderia | 1536 × 864 | 1536 × 864 | ajustes fotométricos conservadores | ~**99,9%** dos contornos do original encontrados a até **2 px** no resultado; diferença média absoluta RGB = **(3,065; 4,606; 4,114)** |

**Métrica:** OpenCV Canny, limiares (60,135), dilatação binária de 2 pixels no mapa de bordas da saída, fração das bordas da fonte cobertas. **Essa medição não prova geometria idêntica em IA**; é um diagnóstico de retenção visual no processo fotométrico cujo algoritmo não altera posição de objetos.

**Ferramenta reprodutível:** `tools/refino_fotometrico.py` (Pillow opcional, sem rede), com presets `interior`, `lavanderia`, `equilibrado`; saída com mesmo tamanho, original não sobrescrito. A versão testada localmente foi o script de desenvolvimento equivalente; a suíte completa da PR e o PC Host ainda exigem homologação.

O controle fotométrico é mais seguro para pequenas correções de luz/cor do que redesenhar a cena por texto. Ele **não** produz novos reflexos fisicamente corretos, reiluminação por path-tracing ou acabamento fotorrealista completo; para isso permanece necessária a renderização 3D ou um editor de imagem adequadamente condicionado.

## 4. Fontes públicas e fórum no lote

- Licença da cena [Blender Classroom](https://www.blender.org/download/demo-files/) (autor Christophe Seux) conferida: **CC0**.
- Tentativa de aquisição de [uma fachada residencial pública do Pexels](https://www.pexels.com/photo/concept-of-modern-house-9976121/) pela URL de download oficial encontrou **limitação de rede/transferência** no ambiente; não salvar como adquirida.
- Novo achado técnico: fórum [EvolveLAB Veras v7](https://forum.evolvelab.io/t/what-is-the-specific-advantage-of-v7-over-standalone-nano-banana/11231) descreve captura de *material IDs*, *object IDs*, câmera e máscaras para edições com inteligência CAD. Trata-se de recurso do ecossistema Veras, **não uma opção disponível no imagegen nativo**.
- Outro caso publicado de [oito edições consecutivas](https://nuit.archi/benchmarks/sequential-editing/) mostra que edições sucessivas gerativas sofrem deriva. **Dados do autor não devem ser apresentados como métricas do ArchRender Hub.**

## 5. Gate real e próximos passos

1. Executar `python -m unittest discover -s tests -v` **no checkout exato da PR atual**; os testes `test_metodo_integrado`, `test_fontes_publicas` e `test_refino_fotometrico` foram adicionados/alterados, mas este documento não afirma aprovação da suíte completa.
2. Confirmar um canal que realmente faça **edição da imagem enviada**, com a fonte anexa como *input image* e evidência de uso. Registrar metadados, IDs da geração, arquivo-fonte e resultado privados.
3. Gerar as seis tentativas A/B/C a partir do mesmo original, cada uma realmente vinculada; avaliar portas/janelas/mobiliário/câmera ANTES de nota editorial. Corrigir apenas via método que mantenha a base.
4. Adquirir as fontes públicas CC0/CC BY quando houver download real e confirmar o uso pela ferramenta; imagens públicas são casos independentes, não substituem o projeto do usuário.
5. Não colocar material privado, screenshots com clientes, renders, nem arquivos binários no GitHub público; não executar ações pagas ou merges.

**Resultado útil desta etapa:** detectamos um problema de validade metodológica e o transformamos em um gate de produto; também produzimos **duas versões conservadoras das imagens originais** disponíveis diretamente nesta conversa, sem transformar isso em vitória falsa de um modelo gerativo.
