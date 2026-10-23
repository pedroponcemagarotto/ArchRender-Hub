# Prompts R2 — receitas originais para execução via ChatGPT

**Data:** 23/10/2026  
**Estado:** hipóteses baseadas em pesquisas e casos, **não testadas no nosso benchmark**.  
**Objetivo:** o ChatGPT deve gerar as imagens solicitadas, e não responder apenas com o texto do prompt. Este arquivo destina-se ao assistente que lê o repositório em novo chat. As receitas funcionam como checklists internos; adaptar à imagem e aos requisitos, sem despejar blocos longos desnecessários ao gerador.

## Regra de ouro para todos os casos

**Não reescrever a geometria documentada com fantasia.** Identificar a fonte de verdade, dar papel exato a outras referências, separar autorização e restrição. **Nunca tratar as instruções como garantia geométrica**. Uma bela imagem diferente do projeto é reprovada em modo fiel.

## P1 — Planta humanizada em 2D, com layout travado

**Insumo:** planta legível, de preferência CAD/PDF em vista ortogonal.  
**Escolha padrão:** técnica de humanização sobre a fonte original, se possível, conservando traços como camada. Se a ferramenta disponível gerar um raster novo integral, verificar o resultado e, se deformar paredes/vãos, voltar à base para composição.

~~~text
Usando a Imagem 1 como desenho arquitetônico autoritativo, produza uma PLANTA HUMANIZADA de apresentação e mantenha exatamente a orientação de leitura, o perímetro, o número de ambientes, as linhas de paredes, as posições de portas, janelas, escadas e circulação já presentes. A aparência deve permanecer vista superior ortográfica 2D, sem inclinação nem transformação em perspectiva. Humanize somente as superfícies de piso e elementos permitidos: [PISOS, MOBILIÁRIO EXISTENTE/AUTORIZADO, PALETA]. Crie textura natural discreta na escala do desenho, separação clara entre ambientes e sombras de contato leves, sem perder linhas de portas e divisórias. A imagem deve ser limpa, equilibrada e adequada a apresentação em [FORMATO]. Não invente texto, cotas, nomes ou áreas. Preservar o projeto é mais importante que o efeito decorativo. Gere a imagem; depois confrontaremos a contagem/posição de vãos e divisórias com a referência.
~~~

**Reprovado se:** alterar qualquer parede, abertura, escada, cotas técnicas ou orientação, ou introduzir ambiente não previsto.

## P2 — Fachada 3D altamente fotográfica a partir de referência

**Insumo:** elevação ou screenshot de modelo/whitebox. Se só houver elevação 2D, uma perspectiva tridimensional terá partes inferidas e deve ser identificada como estudo conceitual, salvo outra evidência.

~~~text
Converta a Imagem 1 em uma fotografia arquitetônica de alto padrão de [TIPO DE EDIFÍCIO], usando o volume, número de pavimentos, silhueta, portas, janelas, telhado, varanda, muros, acessos e câmera já presentes nela como referências que devem permanecer reconhecíveis. A finalidade é melhorar a APARÊNCIA desta mesma obra, não redesenhá-la.

Aplicar somente [MATERIAL A na superfície X], [MATERIAL B na superfície Y], [MATERIAL C na superfície Z], mantendo limites entre planos, escala realista da textura, juntas/veios e rugosidade coerentes. Luz [DIA NUBLADO LUMINOSO / TARDE SUAVE / HORÁRIO AUTORIZADO] com sol de direção plausível, sombras com bordas naturais, equilíbrio entre céu e fachada, vidro com reflexos ambientais críveis; evitar iluminação que apague detalhes de revestimento.

Tratamento editorial de fotografia de arquitetura: composição segura com edifício completo, verticais retas, perspectiva de dois pontos quando compatível com a Imagem 1, lente moderadamente ampla sem deformação grande-angular, cores neutras, exposição equilibrada, contraste elegante e paisagismo em escala humana [SOMENTE SE PERMITIDO]. Materiais e pessoas, quando presentes, não encobrem entradas e janelas.

Imagem 2, caso exista, é referência APENAS de [ESTILO/MATERIAL], sem transferir sua forma ou distribuição de janelas. Gere a imagem e confira no original se todos os vãos e volumes permanecem presentes.
~~~

**Nota de fotografia:** um look de iluminação difusa pode revelar materiais melhor que um pôr do sol muito laranja; tratar como variável de teste, não dogma.

## P3 — Interior editorial premium com geometria fiel

**Insumo:** foto, render bruto ou screenshot que mostre os vãos e a câmera.  
**Saída:** sala, cozinha, quarto, banheiro ou gourmet, conforme categoria real.

~~~text
Produza uma visualização de interior com aparência de fotografia profissional de design, tomando a Imagem 1 como cenário existente. Preserve as quatro bordas visíveis do cômodo, pisos/teto, portas, janelas, altura aparente, marcenaria fixa e mobiliário explicitamente preservado; a posição da câmera também permanece vinculada à referência.

Intervenções autorizadas: [PISO], [PAREDE], [MARCENARIA], [SOFÁ/CAMA/CADEIRAS], [ACESSÓRIOS]. Cada material deve ser localizado em sua superfície e ter escala coerente; madeira de veios plausíveis, cerâmica com juntas proporcionais, tecido com trama delicada, metal sem brilho plástico, vidro/espelho com reflexos consistentes. Respeitar circulação e não bloquear portas ou janelas.

Iluminação natural [CONDIÇÃO] entrando exclusivamente pelos vãos documentados, complementada por [LUMINÁRIAS EXISTENTES/AUTORIZADAS]. Fotografia com verticais retas, ângulo de altura dos olhos, perspectiva moderadamente ampla sem transformar a sala em uma área maior, exposição com detalhes visíveis nas sombras e janelas sem luz estourada. Editorial contemporâneo, composição sem excesso de ornamentos e sem padrão repetitivo artificial.

Se a Imagem 2 existir, usá-la apenas como amostra de paleta/tecido/revestimento e NÃO copiar as dimensões ou posições de objetos desse segundo ambiente. Gere uma imagem e compare estrutura, reflexos e objetos com a Imagem 1.
~~~

**Reprovado se:** sala mais larga, teto alterado, porta desaparecida, janela nova ou circulação bloqueada.

## P4 — Troca de material / reparo LOCALIZADO

**Insumo:** original + área-alvo descrita; máscara de edição quando suporte real estiver disponível.

~~~text
Edite exclusivamente [ÁREA ESPECÍFICA] na Imagem 1. Altere o revestimento atual dessa região para [MATERIAL], [TOM], [ACABAMENTO], com textura e direção de juntas/veios corretas, sombras de contato naturais e reflexos condizentes com a iluminação que já existe. Conserve enquadramento, linhas estruturais, janelas, portas, piso e todas as regiões fora do alvo, preservando a integridade do projeto. Se a segunda imagem foi enviada, usar apenas seu material/tonalidade como referência, não sua geometria. Gere a edição localizada, e confira se nada fora da região solicitada foi indevidamente modificado.
~~~

**Se falhar:** usar composição sobre a fonte original ou reiniciar a partir dela, em vez de pedir cinco correções globais sequenciais.

## P5 — Vídeo de apresentação arquitetônica derivado de imagem aprovada

**Insumo:** uma ou mais imagens já aprovadas; total de shots definido. A receita é para ferramenta de vídeo de verdade, **não** gera MP4 por si só.

~~~text
Imagem de abertura: utilizar a renderização arquitetônica APROVADA como primeiro quadro. Movimento único: dolly-in muito lento e curto em direção à fachada, velocidade uniforme e cinematográfica; leve oscilação de folhagem apenas onde há plantas existentes. Manter números/posições das aberturas, materiais, volumes, linhas verticais, iluminação e escala visual coerentes durante todo o plano. Não revelar fachadas/cômodos ocultos que a imagem de entrada não documenta. Duração [5–8] segundos, enquadramento [16:9 / 9:16], movimento suave e profissional.
~~~

**Para interior:** substituir dolly-in por pan horizontal de pequena amplitude na mesma sala, sem criar nova porta, sala anexa ou móvel.  
**Para percurso real:** solicitar vistas ou modelo adicionais, pois um único quadro não fornece 3D verificável.  
**Se não existir gerador de vídeo acessível:** montar storyboard e, quando possível, animação 2D de imagens estáticas claramente identificada; nunca chamar isso de walkthrough 3D fidedigno.

## P6 — Prompts de correção pós-QA

~~~text
O resultado anterior apresentou [FALHA ESPECÍFICA] na região [REFERÊNCIA]. Use a imagem original do projeto como evidência de como deve ser [PAREDE/VÃO/DETALHE]. Corrija APENAS essa região, restaurando posição, contorno e proporção vistos na origem. Preserve todas as outras superfícies, iluminação, materiais, objetos e composição. Se a ferramenta não conseguir editar só essa região, refaça a partir do original em vez de ampliar a alteração. Após a edição, compare as partes alteradas e as preservadas.
~~~

## Como escolher e evoluir

1. Aplicar P1/P2/P3/P4/P5 ao trabalho correto.
2. Antes da primeira imagem, listar só as 3–7 proteções críticas para aquele arquivo e a mudança permitida.
3. Fazer **uma imagem inicial**, avaliar e registrar.
4. Em vez de pedir dez variações sem controle, alterar **um fator por vez**: luz, material, câmera ou decoração.
5. Evitar listas infladas de motores de render e sufixos como "8K, 32K, award-winning, masterpiece" como substitutos de um briefing.
6. Se P1/P2/P3 falhar em geometrias, usar método híbrido e não promovê-lo a receita aprovada só porque a imagem parece bonita.
7. Registrar resultado no catálogo com status real e versão do prompt. Não publicar mídias privadas.

## Fontes da lógica

- https://developers.openai.com/api/docs/guides/image-prompting
- https://blog.chaos.com/ai-architecture-prompts
- https://blog.chaos.com/7-essential-steps-to-creating-realistic-renderings
- https://www.reddit.com/r/comfyui/comments/1u13ayk/confyui_in_architectural_visualization/
- https://www.reddit.com/r/archviz/comments/1slp022/my_experience_while_exploring_ai_as_rendering_tool/
- https://help.runwayml.com/hc/en-us/articles/48324313115155-Image-to-Video-Prompting-Guide

Este é um **texto original de síntese**, sem reprodução literal dos prompts de terceiros.