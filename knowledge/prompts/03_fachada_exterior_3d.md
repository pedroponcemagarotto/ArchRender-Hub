# AR-EXT-3D-001 — Fachada e exterior 3D

**Versão:** 1.0 | **Estado:** candidato_nao_testado | **Modo padrão:** F (renderizar projeto existente).

## Fonte recomendada

Imagem 1 = screenshot do SketchUp, Revit, Archicad, Rhino, whitebox, render bruto ou foto do imóvel. Imagem 2 = referência apenas de material/estilo se fornecida. Para criação de fachada do zero, mudar explicitamente para modo C e tratar forma como proposta conceitual.

## Prompt-mestre — render fiel ao modelo

~~~text
TAREFA: Transforme a Imagem 1 em uma visualização arquitetônica externa fotorrealista de qualidade profissional, própria para apresentação a cliente.

FONTE DO PROJETO: Imagem 1 é a verdade de projeto quanto a geometria, volumetria, fachadas, posição e quantidade de pavimentos, portas, janelas, cobertura, marquises, sacadas, recuos e ângulo de câmera. Não faça um novo edifício e não melhore a arquitetura inventando aberturas, volumes, pergolados, telhados ou elementos estruturais.

MATERIAIS: converter as superfícies indicadas para [PAREDE PRINCIPAL: MATERIAL/ACABAMENTO], [VOLUME SECUNDÁRIO], [ESQUADRIAS], [PISO EXTERNO]. Mostrar microtextura realista e variação sutil de rugosidade, juntas plausíveis, reflexos e escala correta. A Imagem 2, quando presente, inspira apenas [ELEMENTO AUTORIZADO], sem importar sua geometria.

ILUMINAÇÃO: [MANHÃ DIFUSA / TARDE / PÔR DO SOL / BLUE HOUR], direção aparente coerente com a cena, sombras consistentes, vidro com reflexos fisicamente plausíveis e interiores discretamente visíveis apenas onde houver aberturas originais. Não adicionar luminárias ou aberturas inexistentes.

ENTORNO: [RUA/JARDIM/LOTE/CALÇADA] compatível com a cena de entrada, sem deslocar muro, terreno ou acesso. Pessoas/veículo opcionais e discretos apenas como referência de escala quando autorizados, jamais escondendo a fachada.

CÂMERA: conservar enquadramento e proporções originais. Tratamento fotográfico de arquitetura com perspectiva de dois pontos, verticais retas, aparência de lente normal a moderadamente grande-angular, sem olho-de-peixe. Se a fonte já fixa a câmera, respeitá-la.

ESTÉTICA: realismo editorial, composição limpa, luz natural, materiais distinguíveis; sem aparência plástica, sem exagero de nitidez, sem texto ou marcas d'água.

SAÍDA: uma imagem completa [16:9 / 4:3 / OUTRA], sem corte dos elementos principais; gerar o render e verificar visualmente contra a Imagem 1.
~~~

## Alternativa — conceito do zero (Modo C)

~~~text
CRIE UMA PROPOSTA CONCEITUAL de fachada [TIPO], com [NÚMERO DE PAVIMENTOS E VOLUMES CONHECIDOS], linguagem [ESTILO], materiais [2–4 MATERIAIS], entorno [CONTEXTO] e iluminação [HORÁRIO]. Perspectiva arquitetônica de dois pontos, verticais retas e materiais plausíveis. Trate qualquer arranjo dimensional ou solução estrutural não fornecida como conceito ilustrativo, não como documento executável.
~~~

## Portões

- [ ] Número de pavimentos e volumes iguais à origem no Modo F.
- [ ] Esquadrias, portas, guarda-corpos e telhados preservados.
- [ ] Materiais nos locais definidos; texturas físicas plausíveis.
- [ ] Perspectiva sem verticais acidentalmente inclinadas.
- [ ] Iluminação e sombras coerentes.

**Fonte dos princípios:** Chaos AI architecture prompts, Chaos Veras e OpenAI Image prompting; referências em ../FONTES_E_CURADORIA.md.