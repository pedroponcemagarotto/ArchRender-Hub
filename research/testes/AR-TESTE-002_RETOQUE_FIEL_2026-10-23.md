# AR-TESTE-002 — Correção tonal conservadora das duas imagens originais

**Data:** 2026-10-23  
**Status:** EXECUTADO — melhoria tonal conservadora, **não aprovado** como render fotorrealista premium.  
**Relacionamento:** continuidade de [AR-TESTE-001](AR-TESTE-001_IMAGENS_INTERIORES_2026-10-23.md), em que a geração recriou os ambientes e não preservou a fidelidade.  
**Privacidade:** somente documentação de método; os arquivos originais e finais permanecem fora do GitHub público.

## Método

Usou-se a imagem original de cada cena, isoladamente, sem modelo generativo de reconstrução. Com OpenCV/Pillow:
1. Correção tonal e leve abertura de médios/sombras (gamma por cena).
2. Contraste local limitado no canal de luminosidade via CLAHE.
3. Saturação levemente ajustada.
4. Nitidez moderada por unsharp mask.
5. Mesmo recorte e mesma resolução da entrada: **1536 x 864 pixels por arquivo**.

O processo **não reposiciona objetos, nem adiciona mobiliário, paredes, portas ou materiais**. Também não reconstrói textura física ausente nem produz iluminação 3D nova.

## Resultados observados

- A imagem original da lavanderia recebeu contraste tonal local mais equilibrado sem mudança de elementos.
- A imagem original de sala/cozinha recebeu abertura moderada de sombras e tratamento tonal; a luz estourada da fonte não pode ser fisicamente reconstruída pela correção.
- Foram produzidas duas imagens JPEG distintas e uma comparação visual.
- As saídas existem no ambiente da conversa, mas **não foram publicadas neste repositório**, preservando a privacidade do material enviado.
- Avaliação: integridade estrutural respeitada pelo tipo de processamento; aparência final ainda limitada pela qualidade/materialidade do render de origem. Não declarar equivalência a V-Ray/Corona/D5.

## Decisão sobre o próximo método

A seleção de técnica deve ser orientada pela restrição do projeto:
- **Fidelidade máxima:** correção fotográfica e composição em camadas sobre render original, com validação espacial.
- **Realismo significativamente mais alto:** edição generativa **separada por cena** + eventual máscara ou ferramenta que permita preservar regiões; sem garantia absoluta de geometria.
- Não repetir prompt de geração conjunto em duas imagens enquanto o sistema produzir colagens e decoração não autorizada.
- Não colocar essas tentativas no catálogo de 'aprovados' sem revisão explícita.

**Aviso:** código e imagens de cliente não foram enviados ao GitHub; sem uso de Incubadora ou GitHub Actions.
