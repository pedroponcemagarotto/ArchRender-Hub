# ArchRender Hub — iniciar um teste em um novo chat

**Versão do guia:** 1.0 (2026-10-23)  
**Repositório oficial:** https://github.com/pedroponcemagarotto/ArchRender-Hub  
**Branch de conhecimento atual:** \`feat/prompt-system-v1\`  
**PR em revisão:** https://github.com/pedroponcemagarotto/ArchRender-Hub/pull/1

> **Importante:** o GitHub é a base versionada de instruções, templates e aprendizados, mas não substitui o envio de imagens do projeto. Um novo chat não está automaticamente conectado ao histórico completo da conversa anterior. Ler o repositório de novo é parte obrigatória da abertura do trabalho.

## Como o usuário começa

1. Abra um novo chat no ChatGPT com acesso a imagens.
2. Anexe a planta, imagem de fachada, croqui, render ou referência que deseja testar. Não envie dados pessoais ou informações confidenciais para GitHub público.
3. Copie a mensagem abaixo e ajuste a última linha para sua tarefa.
4. Se disponível, conecte/utilize o GitHub no chat para ler os arquivos da branch indicada.
5. Confira a imagem gerada e indique divergências concretas (por exemplo, uma janela extra). O objetivo é gerar a imagem, não só fornecer o prompt.

## Mensagem pronta para copiar no novo chat

~~~text
Vamos continuar o projeto ArchRender Hub.

Use como fonte de trabalho o repositório:
https://github.com/pedroponcemagarotto/ArchRender-Hub

Antes de agir, leia, na branch feat/prompt-system-v1:
1. PROMPT_SYSTEM_v1.md
2. knowledge/OPERACAO_COM_CHATGPT.md
3. templates/VALIDACAO.md
4. catalog/prompts.json
5. a receita em knowledge/prompts/ pertinente à minha solicitação.

A PR de referência é https://github.com/pedroponcemagarotto/ArchRender-Hub/pull/1, ainda em revisão. NÃO considere que os arquivos da PR já estão na main. Se o GitHub não estiver acessível, avise e solicite o conteúdo necessário; não invente que leu os arquivos.

Seu papel é atuar como meu diretor de visualização arquitetônica e EXECUTAR a criação de imagens com os recursos de geração disponíveis, e não apenas entregar prompts. Analise as imagens anexadas, escolha a receita apropriada, atribua papéis às referências, diferencie fatos de hipóteses e use modo F (fiel), C (conceito) ou T (técnico). Preserve geometria, portas, janelas, distribuição e demais restrições conforme o modo, sem afirmar fidelidade dimensional que a IA não pode garantir.

Depois de gerar, compare visualmente com a referência, identifique erros e sugira uma correção localizada. Não classifique como 'aprovado' um resultado que não foi gerado, inspecionado e confirmado. Registre para histórico apenas o método e metadados não confidenciais, em uma branch ou PR separada; não envie plantas, fotos, imagens privadas, nomes de cliente ou vídeos ao repositório público.

Para vídeo, use imagens aprovadas e a receita knowledge/prompts/08_video_apresentacao.md; produza um vídeo somente se realmente houver uma ferramenta compatível, caso contrário esclareça o limite e prepare o storyboard.

Não use a Incubadora Remote V2. Não altere a aplicação Python existente nem habilite GitHub Actions.

Minha tarefa atual: [ESCREVA AQUI: ex. humanizar a planta anexada com piso amadeirado e paredes preservadas; gerar fachada 3D; criar interior; preparar vídeo de apresentação].
~~~

## Como testar o método corretamente

**Teste A — planta humanizada:** anexar planta legível; escolher \`knowledge/prompts/01_planta_humanizada.md\`; registrar contorno, paredes, portas, janelas e eventuais elementos inventados. Se a saída alterar geometria, marcar **reprovado** e corrigir a técnica, não apenas a descrição textual.

**Teste B — fachada 3D:** anexar screenshot/elevação/modelo; usar \`03_fachada_exterior_3d.md\`; comparar pavimentos, janelas, portas, volumes e ângulo de câmera. Materiais e luz podem variar se autorizados.

**Teste C — interiores:** anexar foto/render/modelo do ambiente; usar \`04_interiores.md\`; verificar posição de aberturas, escala visual e itens fixos.

**Teste D — vídeo:** começar por uma ou mais vistas aprovadas; usar \`08_video_apresentacao.md\`; montar planos curtos e conferir se a ferramenta disponível realmente gera vídeo, distinguindo animação de fotos de vídeo generativo.

## Como registrar um aprendizado

- Usar campos de \`templates/REGISTRO_EXEMPLO.json\` (preencher dados reais disponíveis, sem fabricar seed/modelo).
- Aplicar portões de qualidade de \`templates/VALIDACAO.md\`.
- Estados válidos: \`candidato_nao_testado\`, \`testado\`, \`aprovado_cliente\`, \`reprovado\`, \`descontinuado\`.
- O repositório **é público**. Não publicar originais, renders de cliente, localização/endereço, logotipos, documentos confidenciais ou qualquer identificação pessoal. Histórico público só com conteúdos seguros e anonimizados; armazenar mídias privadas fora do GitHub público.
- Preferir alteração em branch + PR, mantendo \`main\` intacta até revisão.
- Registrar tanto sucessos quanto falhas, incluindo qual detalhe do prompt e/ou técnica resolveu o problema.

## Convenção para chats posteriores

Enquanto a PR #1 não for incorporada, utilizar explicitamente a branch \`feat/prompt-system-v1\`. Quando incorporada à \`main\`, o novo chat poderá usar \`main\`, mas deve verificar a revisão efetiva antes de agir. Caso a receita seja alterada, consultar a versão mais recente e não reutilizar cegamente comandos antigos.

## O que não é garantido

- A documentação não cria uma memória permanente automática entre chats.
- Um prompt textual nunca assegura geometria ou medidas exatas; materiais técnicos exigem conferência com CAD/BIM.
- A V0.1 do aplicativo local ainda não gera imagens ou vídeos diretamente; o ChatGPT pode gerar imagens no contexto da conversa com as ferramentas disponíveis.
- Criação de vídeo MP4 depende de acesso a ferramenta de vídeo; ter a receita não equivale a ter esse recurso.
