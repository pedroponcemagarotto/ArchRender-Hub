# Benchmark R1 — como comprovar qualidade em vez de apenas prometer

**Data:** 2026-10-23 | **Status:** planejamento **não executado**.  
**Proposta:** avaliar a produção de imagens do ChatGPT por critério de cliente e integridade do projeto, não por adjetivos do prompt.

## 1. Material de teste

Pelo menos 3 casos **com direito de uso** e origem comprovável (preferivelmente amostras fictícias/autoria própria, ou um projeto real com autorização e dados mantidos privados):

- **Caso P — planta humanizada:** planta ortográfica com 5–8 ambientes identificáveis, paredes, portas, janelas e uma escada. Incluir uma planta com linhas finas e outra vetorial/PDF quando possível.
- **Caso F — fachada:** imagem-clay de modelo 3D com 2 pavimentos, 6–10 vãos e 3–4 materiais pré-definidos. Guardar modelo ou vistas adicionais para auditar geometria.
- **Caso I — interior:** sala/cozinha com porta, janela, 4+ móveis e revestimentos. Guardar foto/render base com ângulo fixo.

**Não usar projetos de clientes como fixture público.** Armazenar originais/resultados privados; repositório guarda apenas identificadores e relatórios anonimizados.

## 2. Três abordagens a comparar

| Variante | Intervenção | Finalidade |
| --- | --- | --- |
| A — base | prompt genérico curto + referência | medir resultado sem especialização |
| B — Prompt System V1 | receita knowledge/prompts/ + referência + restrições + luz/câmera/material | verificar ganho do texto estruturado |
| C — Método R2 | mesma receita + auditoria de geometria + papéis de referência + edição/mascaramento/composição local quando disponível + QA | verificar ganho do processo completo |

**Isolar variáveis:** usar a mesma fonte, proporção de saída e ferramenta de imagem. Se houver opção de seed/modelo, registrar; caso contrário escrever "não exposto". Comparações não devem atribuir ganhos a parâmetro não controlado.

## 3. Primeira bateria

- 3 casos × 3 variantes × 2 repetições = **18 gerações** propostas.
- Inspecionar todas as 18, selecionar melhor por categoria e registrar taxa de reprovação geométrica.
- Repetir com mais entradas caso resultados sejam contraditórios; n=2 é **triagem exploratória**, não validação estatística.
- Se um caso exigir geometria dimensional exata, executar versão híbrida (camada original ou CAD/BIM) além da geração.
- Vídeos: fase separada, ao menos dois trechos com quadro inicial/final autorizados; só executar se houver ferramenta de vídeo acessível.

## 4. Avaliação objetiva e subjetiva

### Gate geométrico — primeiro critério, binário

Em modo F/T, **reprovação** por:
- novo cômodo/divisória/pavimento não autorizado;
- porta/janela removida, acrescentada ou deslocada;
- escada, pilar, piscina, cobertura ou acessos alterados;
- mudança perceptível da câmera/projeção quando fixada;
- cota textual ausente, modificada ou inventada em entrega técnica.

Se a entrada não permitir identificar esses elementos, registrar "não verificável" e **não** declarar fidelidade total.

### Escore editorial de 100 pontos (somente após gate)

| Fator | Pontos |
| --- | ---: |
| Observância de material, função e solicitações específicas | 20 |
| Fotografia/composição/câmera | 20 |
| Realismo de materiais e texturas | 20 |
| Luz, exposição, reflexos e sombras | 20 |
| Escala/contexto sem distrações | 10 |
| Artefatos, clareza visual e legibilidade | 10 |
| **Total** | **100** |

**Meta inicial proposta:** gate geométrico aprovado **e** escore >= 85 para recomendar apresentação, >= 92 para "alto padrão visual", sujeito a revisão humana. Esses limiares são definição interna experimental; **não são padrões da indústria** nem significam equivalência a V-Ray.

### Métricas a reportar

- **Taxa de retenção geométrica =** imagens que passaram gate / imagens avaliáveis.
- **Taxa de aceitação =** imagens aprovadas / imagens geradas.
- **Retrabalho =** gerações + correções por imagem aceita.
- **Consistência multivista =** pares de perspectivas consistentes quanto a janelas, materiais, volumetria e mobiliário / pares testados.
- **Resolução:** pixels reais entregues; para impressão, tamanho de papel e fonte vetorial.
- **Custo/tempo:** somente observados, nunca estimados como fatos.

### Controle de risco

Um resultado bonita mas infiel recebe "não aprovado". Se A superar C em algum caso, registrar; não manipular critérios para confirmar nossa hipótese. Imagens de modelo 3D e de IA podem ser avaliadas por duas pessoas independentes quando possível; registrar discordâncias.

## 5. Modelo de relatório para preenchimento

~~~json
{
  "benchmark_id": "AR-BENCH-R1",
  "case": "P|F|I",
  "variant": "A|B|C",
  "repetition": 1,
  "generator": "nome real, se conhecido",
  "prompt_version": "v1 ou R2",
  "input_reference_private": "ID sem dados do cliente",
  "resolution_px": null,
  "geometry_gate": "aprovado|reprovado|nao_verificavel|nao_avaliado",
  "geometry_issues": [],
  "editorial_score": null,
  "accepted": false,
  "rework_attempts": 0,
  "status": "nao_executado"
}
~~~

## 6. Evidência e interpretação

Ver [levantamento de fóruns](PESQUISA_FORUNS_E_FONTES_2026-10-23.md). O caso da competição 2024 e relatos comunitários indicam que "prompt melhor" pode não melhorar geometria sem máscara/base. Isso é precisamente a hipótese a ser medida em A/B/C.

**Estado de execução em 2026-10-23:** 0/18 gerações realizadas neste benchmark; nenhuma receita nova aprovada; sem produção de vídeo. Não afirmar o contrário.