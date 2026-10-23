# ArchRender Hub — Prompt System v1.0

**Data:** 2026-10-23  
**Estado:** conjunto inicial de receitas autorais baseado em documentação técnica e fontes públicas; **não representa benchmark de imagens geradas**.  
**Direção do produto:** o usuário descreve um projeto de arquitetura e anexa desenhos/referências; o ChatGPT conduz a direção visual, prepara a receita, gera/edita as imagens com os recursos de imagem disponíveis e documenta o que funcionou. Para vídeo generativo, verificar disponibilidade da ferramenta antes de prometer o arquivo final.

## Comece por aqui

1. [Protocolo de trabalho com o ChatGPT](knowledge/OPERACAO_COM_CHATGPT.md) — regras de interpretação, fidelidade e entrega.
2. [Prompt de planta humanizada](knowledge/prompts/01_planta_humanizada.md).
3. [Prompt de planta baixa técnica/apresentada](knowledge/prompts/02_planta_tecnica.md).
4. [Prompt de fachada e exterior 3D](knowledge/prompts/03_fachada_exterior_3d.md).
5. [Prompt de interiores](knowledge/prompts/04_interiores.md).
6. [Prompt de croqui/modelo para render](knowledge/prompts/05_croqui_modelo_render.md).
7. [Prompt de paisagismo](knowledge/prompts/06_paisagismo.md).
8. [Prompt de materiais e iluminação](knowledge/prompts/07_materiais_iluminacao.md).
9. [Vídeo de apresentação ao cliente](knowledge/prompts/08_video_apresentacao.md).
10. [Correções controladas](knowledge/prompts/09_correcao_controlada.md).
11. [Briefing reutilizável](templates/BRIEFING.md), [verificação](templates/VALIDACAO.md), [registro de execução](templates/REGISTRO_EXEMPLO.json) e [catálogo](catalog/prompts.json).
12. [Fontes, critérios de curadoria e licenças](knowledge/FONTES_E_CURADORIA.md).

## O que é prioridade

**Resultado real ao cliente > coleção de textos bonitos.** A receita registra o que a IA deve fazer e o que não pode alterar. A avaliação considera fidelidade ao desenho, composição, qualidade material, luz, legibilidade e uso final. As imagens só passam a ser consideradas exemplos validados depois de gerar, conferir e aprovar.

**Duas modalidades distintas:**

- **Fidelidade ao projeto:** partir de planta, corte, elevação, modelo ou fotografia; preservar o que foi fornecido. Não afirmar precisão milimétrica só com IA generativa. Para desenhos executivos, utilizar CAD/BIM e conferência profissional.
- **Conceito/estudo:** explorar propostas quando o usuário autorizou mudanças; separar claramente hipótese visual de projeto aprovado.

## Fluxo por atendimento

1. Receber texto e imagens, atribuindo a cada arquivo o papel de base geométrica, referência estética, material, mobiliário ou entorno.
2. Identificar observações verificáveis, restrições críticas e pontos não legíveis. Não inventar medidas.
3. Selecionar uma receita por tipo de entrega e personalizar somente os campos necessários.
4. Gerar/editar a imagem quando solicitado e disponível; preparar roteiro/quadros para vídeo e produzir o arquivo apenas quando houver ferramenta capaz de fazê-lo.
5. Avaliar resultado contra a fonte. Se houver divergência crítica, corrigir de maneira localizada; não declarar aprovação automática.
6. Registrar modelo, versão, prompt efetivo, referências, resultado, falhas e aprovação, respeitando privacidade do cliente.

## Histórico e estados

Cada receita e tentativa tem um estado:

- **candidato_nao_testado:** prompt escrito ou extraído de boa prática; sem teste visual neste ambiente.
- **testado:** imagem ou vídeo realmente gerado e conferido, com observações.
- **aprovado_cliente:** usuário validou o resultado para a finalidade proposta.
- **reprovado:** falhou em restrição relevante.
- **descontinuado:** mantido por histórico, mas não recomendado.

A V0.1 do aplicativo Python/SQLite permanece em funcionamento como biblioteca local; estas receitas ainda **não** estão integradas automaticamente ao banco do aplicativo. Não se declara geração de vídeos nem renders novos neste commit.

## GitHub público, dados privados

O repositório é público. **Não enviar** plantas de clientes, nomes, endereços de obra, imagens privadas, vídeos, chaves ou backups. Manter insumos e entregas em armazenamento privado; versionar apenas templates e registros anonimizados, com IDs e hashes/descrições quando adequado. Imagens externas exigem licença/atribuição e revisão de autorização antes da publicação.

## Critério de qualidade

Não existem palavras mágicas nem um prompt universal. O melhor prompt é o que produz a entrega correta, com menor desvio do projeto e menor retrabalho, em uma configuração verificável. Consulte [validação](templates/VALIDACAO.md).

## Pesquisa aprofundada — método R2 (23/10/2026)

**A pesquisa de fóruns e profissionais tornou necessária uma correção:** o Prompt System V1 é apenas um conjunto de receitas **não testadas**. Para buscar qualidade próxima à fotografia e render profissional, precisamos controlar estrutura, materialidade, iluminação, câmera, edição localizada e qualidade final. Texto sozinho não garante fidelidade arquitetônica.

Ordem de leitura **obrigatória para testes novos**:

1. [Pesquisa detalhada em fóruns e fontes técnicas](research/PESQUISA_FORUNS_E_FONTES_2026-10-23.md) — evidências, exemplos e limites.
2. [Método de produção com ChatGPT R2](research/METODO_RENDERS_CHATGPT_R2.md) — escolher modo, travar geometria, gerar e validar.
3. [Prompts R2 adaptados ao ChatGPT](research/PROMPTS_CHATGPT_R2.md) — famílias de plantas, fachadas, interiores, alterações locais e vídeo.
4. [Benchmark visual R1](research/BENCHMARK_VISUAL_R1.md) — comparar 18 saídas de A/B/C, ainda **não executado**.
5. [Fontes verificadas em JSON](research/FONTES_VERIFICADAS_2026-10-23.json) — referências públicas com classificação.

**Regras inegociáveis:** não declarar um teste que não aconteceu; não confundir imagem fotorrealista com precisão CAD/BIM; não prometer vídeo generativo sem ferramenta conectada; não publicar dados de clientes no GitHub público. O ChatGPT **gera as imagens** com os recursos disponíveis e conduz a avaliação, não delega ao usuário a engenharia dos prompts.

A Incubadora Remote V2 e GitHub Actions continuam fora deste projeto neste momento. Nenhum módulo da aplicação local V0.1 foi reprogramado neste documento.
