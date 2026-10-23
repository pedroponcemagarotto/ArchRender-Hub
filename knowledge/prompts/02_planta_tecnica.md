# AR-PLAN-TEC-001 — Planta baixa apresentada / técnica

**Versão:** 1.0 | **Estado:** candidato_nao_testado | **Modo:** T (técnico) ou F (apresentação fiel).

## Quando usar

**Apresentação:** aplicar hierarquia gráfica, paleta e layout editorial a uma planta técnica existente.  
**Documento cotado/executivo:** manter original CAD/BIM como fonte autoritativa; a imagem de IA **não certifica cotas nem escala**. Não utilizar saída generativa como único documento técnico de obra.

## Prompt-mestre

~~~text
TAREFA: Produza uma prancha clara de PLANTA BAIXA a partir da Imagem 1, sem redesenhar a arquitetura. O objetivo é [APRESENTAÇÃO DE CLIENTE / APOIO EXPLICATIVO], não criar um novo projeto.

REFERÊNCIA AUTORITATIVA: Imagem 1 contém o layout aprovado. Preserve o contorno, orientação, paredes, portas com giros quando visíveis, janelas, escadas, pilares, áreas molhadas e quaisquer símbolos técnicos legíveis. Elementos não identificados devem continuar neutros; não inferir estrutura, dimensões, unidades ou orientação geográfica.

PROJEÇÃO: vista superior ortogonal 2D. Linhas firmes com hierarquia de espessura apropriada, fundo [BRANCO/CLARO], áreas diferenciadas sutilmente, legendas distribuídas sem cobrir paredes ou portas. Evite volume, perspectiva e sombras dramáticas.

CAMADAS: mantenha paredes e vãos como leitura dominante. Mobília [PRESERVAR EXISTENTE / USAR APENAS A AUTORIZADA / NÃO ADICIONAR]; piso [ESPECIFICAÇÃO]; cores [PALETA]. Os elementos não especificados devem usar convenções gráficas simples.

DIMENSÕES E TEXTOS: transcrever apenas dados claramente fornecidos e verificáveis no desenho original ou briefing. Não calcular, arredondar, corrigir ou inventar cotas, áreas, norte ou nomes de ambiente. Para informação não legível, deixar sem rótulo e reportar fora da imagem.

SAÍDA: uma vista completa e sem recortes, apropriada para [A4 / A3 / PAINEL], priorizando legibilidade em tamanho real. Gerar imagem ilustrativa somente; o CAD/BIM continua sendo a base dimensional oficial. Compare a saída com a imagem de entrada.
~~~

## Fluxo quando há exigência de precisão

1. Solicitar/exportar PDF vetorial, DWG/DXF ou desenho técnico legível.
2. Renderizar/apresentar o desenho original em vez de recriar toda a geometria por IA.
3. Se necessário, aplicar cores, pictogramas ou mobiliário em camadas separadas sobre a base.
4. Conferir medidas e proporções no documento técnico, não visualmente estimando pixels.

## Checklist

- [ ] 100% das divisórias, acessos, aberturas e escadas rastreáveis à base.
- [ ] Nenhum texto/cota fictício.
- [ ] Contraste e hierarquia de linhas adequados.
- [ ] Escala documental respeitada na fonte original, sem afirmação indevida de precisão no raster.

**Fonte técnica:** orientação de separação entre descrição criativa, desenho-base e limites de geometria em OpenAI/Chaos; ver ../FONTES_E_CURADORIA.md.