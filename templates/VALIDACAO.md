# Checklist de revisão — render, planta e vídeo

**Status default:** candidato_nao_testado. Não marcar PASS sem inspeção da saída real e comparação com a fonte.

## Portões obrigatórios (modo fiel/técnico)

- [ ] Comparar a entrada com o resultado: quantidade de pavimentos, paredes, vãos, janelas, portas, escadas, perímetros e linhas de circulação.
- [ ] Não existem dimensões, nomes de ambientes ou sistemas construtivos inventados.
- [ ] A projeção pedida foi respeitada: planta ortogonal superior permanece superior; fachada mantém verticais adequadas.
- [ ] Mudanças realizadas estão dentro do escopo permitido.
- [ ] Se a origem é parcial/ilegível, fatos não verificáveis estão identificados como tais.

**Falha em qualquer item geométrico obrigatório → REPROVADO**, mesmo que o render seja atraente. Para material conceitual, indicar 'representação ilustrativa' e avaliar com tolerância correspondente.

## Escore interno de comparação (heurístico; não científico)

| Fator | Peso |
| --- | ---: |
| Fidelidade à fonte e preservação de elementos | 40 |
| Cumprimento do briefing e alterações autorizadas | 20 |
| Materiais/luz fisicamente coerentes | 15 |
| Composição/câmera/projeção | 10 |
| Limpeza visual e ausência de artefatos | 10 |
| Legibilidade de textos/etiquetas (quando presentes) | 5 |
| **Total** | **100** |

Meta interna inicial: 90/100 **e** nenhum portão crítico falho para candidato a aprovação. O escore não substitui a revisão do profissional nem aprovação do cliente. Se não houver textos, distribuir os cinco pontos entre cumprimento do briefing e limpeza visual e anotar o ajuste.

## Checklist adicional de vídeo

- [ ] Movimentos de câmera não exigem revelar geometria oculta não verificada.
- [ ] As cenas preservam portas, janelas, materiais, número de pavimentos e orientação.
- [ ] Não houve deformações temporais perceptíveis em paredes, vidro, guarda-corpos ou mobiliário.
- [ ] Duração e ordem dos planos correspondem ao storyboard.
- [ ] Legendas, logotipos e nomes foram fornecidos/autorizados.
- [ ] O arquivo final existe, abre, tem duração/resolução/canal de áudio conferidos.
- [ ] Método identificado corretamente: vídeo gerado por modelo / animação de imagens fixas / montagem tradicional.

## Registro mínimo de cada tentativa

ID | data | tipo | modo | versão do prompt | modelo real | referência privada | parâmetros conhecidos | status | escore | falha | correção | aprovação.

Se a ferramenta/modelo não expõe parâmetro ou seed, escrever 'não disponível' — jamais inventar valores.