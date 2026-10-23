# AR-TESTE-001 — Primeiras tentativas de refino de duas cenas de interiores

**Data:** 2026-10-23  
**Status final:** REPROVADO (fidelidade / separação de cenas)  
**Tipo:** teste exploratório de geração e edição usando recursos de imagem do ChatGPT.  
**Privacidade:** nenhum arquivo original ou resultado enviado para este GitHub público. O registro é genérico e não identifica cliente, projeto ou localização.

## Caso

Duas imagens-base enviadas na conversa para estudo do ArchRender Hub:
- Cena A: lavanderia compacta com abertura superior, porta de vidro lateral, tanque e máquina de lavar.
- Cena B: sala/cozinha integrada com sofá, bancada, geladeira, esquadria escura e corredor ao fundo.

### Resultado de referência — primeira geração, antes deste lote
A geração anterior elevou visualmente a apresentação e a materialidade aparente, mas a avaliação por observação identificou reinterpretações de acabamentos e objetos. Fidelidade exata não comprovada.

### Lote atual — aprimoramento visual solicitado
Três saídas geradas no mesmo turno tentaram refinar realismo, textura, iluminação e preservação. O resultado repetiu indevidamente o formato de díptico de ambas as cenas, quando o desejado eram edições **independentes**, e introduziu/adaptou itens não solicitados (por exemplo prateleiras, plantas, luminárias e detalhes de bancada). Alterações de enquadramento impediram alegar que a geometria e a composição foram preservadas.

| Dimensão avaliada | Conclusão |
| --- | --- |
| Existência de imagem gerada | Sim, três composições conjuntas |
| Uma saída por arquivo de entrada | **Não** |
| Preservação de geometria/composição | **Não demonstrada; alterações visíveis** |
| Acabamentos e iluminação | Estudo visual realizado; sem avaliação de qualidade independente |
| Prompt exato/seed/modelo explícitos | Não disponibilizados pela interface de geração; **não inventar** |
| Aprovação para apresentação fiel a projeto | **Não** |

**Limite da revisão:** avaliação visual qualitativa sem auditoria pixel a pixel nem geometria vetorial. Não atribuir percentual de fidelidade.

## Hipótese técnica revisada

Repetir geração integral com descrição de duas cenas privilegia estilo/collage e não fixa o layout. Frases genéricas como "preservar estrutura" não são bloqueios reais. As novas tentativas devem isolar cada imagem original em uma sessão/tarefa de edição, preferencialmente por máscara ou composição sobre a origem; quando o gerador não demonstrar controle local, usar correção em camadas sobre a imagem-base e manter imutáveis a estrutura e posição dos elementos documentados.

## Próximo teste recomendado

1. Trabalhar com **somente a cena A** como referência ativa; não incluir a outra cena ou colagens geradas em contexto de geração.
2. Autorizar apenas mudanças verificáveis de luz/contraste/cor/textura; proibir adição de prateleira, plantas, nichos ou luminárias.
3. Preservar literalmente o ponto de vista, o recorte, a porta envidraçada, o tanque, a máquina e a forma aberta para o céu.
4. Se a geração insistir em mover/introduzir objetos, priorizar retoque determinístico (curvas, balanço de branco, contraste local, ajustes regionais) da imagem original; isso melhora apresentação sem reconstruir o espaço.
5. Repetir, em operação **separada**, com a cena B, protegendo geladeira, sofá, corredor, janela, bancada e pia.
6. Comparar arquivos originais com saídas individuais e registrar mudanças, dimensões reais e aprovação; somente então promover status a testado/aprovado_cliente.

## Interpretação

Esta tentativa é um **teste de falha valioso**, não evidência de que um modelo específico não consiga produzir boas imagens arquitetônicas. A incapacidade de realizar as edições separadas com fidelidade nesta interação indica que a estratégia utilizada foi inadequada. Não promover o Prompt System R2 a "validado" por este resultado.

**Acordos:** sem Incubadora Remote V2, sem GitHub Actions; sem fotos privadas no GitHub público.
