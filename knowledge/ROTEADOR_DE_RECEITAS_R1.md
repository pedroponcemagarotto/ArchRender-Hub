# Roteador de receitas de imagens e vídeo — ArchRender Hub

**Versão:** 1.0 · **Status:** incorporado como guia; regras aguardam benchmark visual.

| Fonte/tarefa | Receita de execução | Preservar especificamente | Falha mais perigosa |
| --- | --- | --- | --- |
| Planta 2D, solicitar humanização | \`prompts/01_planta_humanizada.md\` | paredes, portas, janelas, escada, cotas se exibidas | trocar posição ou criar ambientes |
| Planta 2D, apresentação técnica | \`prompts/02_planta_tecnica.md\` | desenho vetorial, cotas, etiquetas, norte | texto/cota inventados |
| Modelo 3D, fachada | \`prompts/03_fachada_exterior_3d.md\` | altura, número de vãos e pavimentos, volume, câmera | deslocar ou criar esquadrias |
| Interior, foto ou render | \`prompts/04_interiores.md\` | paredes, aberturas, móveis fixos, bancada, câmera | inventar prateleiras ou mudar layout |
| Croqui ou whitebox | \`prompts/05_croqui_modelo_render.md\` | volumetria principal e relações espaciais comprovadas | transformar em outro projeto |
| Paisagismo | \`prompts/06_paisagismo.md\` | caminhos, acessos e posicionamento aprovado | bloquear circulação |
| Troca de material/luz | \`prompts/07_materiais_iluminacao.md\` | todos os pixels/regiões não-alvo sempre que possível | alteração global involuntária |
| Vídeo de apresentação | \`prompts/08_video_apresentacao.md\` + \`VIDEO_GRATUITO_PC.md\` | sequência de imagens aprovadas e continuidade | vídeo inventar novo ponto de vista |
| Corrigir desvio localizado | \`prompts/09_correcao_controlada.md\` | tudo fora da região-alvo | melhorar uma coisa e estragar outra |

## Ficha rápida de execução

1. **Entrada:** uma imagem-base de geometria por vez. Só juntar fontes quando for necessário; nunca misturar dois ambientes distintos como mesma cena.
2. **Verdade da fonte:** observado / informado / proposto / não verificável.
3. **Modo:** F (fiel), C (conceito), T (técnico); o modo determina o gate geométrico.
4. **Preservações obrigatórias:** enumeração nominal de 5 a 10 âncoras verificáveis.
5. **Mudanças permitidas:** lista positiva fechada, preferencialmente separada por região.
6. **Câmera/aspecto:** mesmos pontos de fuga, verticais, recorte e proporção salvo aprovação.
7. **Realismo:** textura e escala, rugosidade/reflexos, luz e sombras plausíveis, qualidade sem sobreprocessamento.
8. **Geração:** utilizar a ferramenta real; registrar nome do modelo só se confirmado. Não simular ControlNet, máscara nem seed inexistentes.
9. **Revisão:** original e resultado, diferenças em âncoras fixas, checklist; aprovado/reprovado/não verificável.
10. **Repetição:** uma variável visual por tentativa quando viável; erros persistentes pedem método híbrido/fonte 3D, não apenas prompt maior.

Inspirado nos **conceitos gerais** de [ARCHI Rendering Studio](https://github.com/dakhlallah/arch-render) e [GPT Image Design Prompts](https://github.com/linlhf/gptimage-design-prompts), sem reproduzir templates ou código desses projetos literalmente.
