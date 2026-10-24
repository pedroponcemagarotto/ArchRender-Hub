# AR-MAT-LUZ-001 — Troca de materiais e estudos de luz

**Versão:** 1.0 | **Estado:** candidato_nao_testado | **Modo:** F.

## Subcaso A — troca de revestimento localizado

Imagem 1 = cena base com arquitetura fixada. Imagem 2 = referência de material (somente cor, textura, junta e acabamento). Sempre descrever a área-alvo em palavras; se houver máscara, utilizá-la para limitar a edição.

### Prompt A

~~~text
EDITE A IMAGEM 1, QUE É A BASE GEOMÉTRICA E DE CÂMERA. Imagem 2 é referência EXCLUSIVAMENTE para textura, material, cor e acabamento; NÃO transfira a geometria, o mobiliário nem a arquitetura da Imagem 2.

ALTERAÇÃO ÚNICA: substitua o acabamento da superfície [DESCREVER ALVO EXATO] por [MATERIAL], com tonalidade [COR], rugosidade [ACABAMENTO], juntas [PADRÃO/ESCALA SE EXISTIREM], coerência de perspectiva e iluminação.

PRESERVAÇÃO: mantenha exatamente o posicionamento e a forma aparente de paredes, portas, janelas, telhado, pisos fora do alvo, móveis, iluminação, paisagismo e enquadramento da Imagem 1. Não edite superfícies vizinhas, não adicione objetos nem elimine texturas do resto da cena.

RESULTADO: imagem realista, juntas bem orientadas, escala do material plausível e bordas da aplicação precisas. Gere a edição e compare especificamente a região do alvo e suas bordas com a imagem de origem.
~~~

## Subcaso B — versão de iluminação sem reforma

Quando se muda o horário, **sombras e reflexos podem mudar**; o que deve permanecer é geometria, materiais e posição física de luzes, não as sombras antigas.

### Prompt B

~~~text
EDITE A IMAGEM 1 PARA UM ESTUDO DE LUZ DE [HORÁRIO: MANHÃ / TARDE / ENTARDECER / NOITE]. Preserve a mesma arquitetura, móveis, materiais, paisagismo, câmera, volumes, vãos e fontes físicas de iluminação existentes.

ALTERE SOMENTE A ILUMINAÇÃO E OS EFEITOS RESULTANTES: temperatura, intensidade, cor do céu, contraste, sombra projetada e reflexos plausíveis para [CONDIÇÕES ESPECÍFICAS]. Não introduza postes, luminárias, fitas LED ou janelas inexistentes. Se interiores com iluminação artificial forem visíveis, use apenas fontes de luz existentes/confirmadas.

VISUAL: fotografia arquitetônica realista, exposição equilibrada, vidros sem brilho artificial, luminosidade física coerente. Gere nova variante mantendo enquadramento e objetos.
~~~

## Subcaso C — comparação de três opções

Usar exatamente a mesma base, enquadramento e iluminação para alternativas A/B/C de material; registrar cada alteração com ID. Não misturar dois materiais novos em um único teste se o objetivo for avaliar qual funcionou.

## Portão

- [ ] Máscara/área alterada respeitada, quando disponível.
- [ ] Material novo tem dimensão/textura coerente com a superfície.
- [ ] Não houve geometria nova.
- [ ] Comparação é justa: somente variável declarada mudou.

**Fonte dos princípios:** OpenAI prompts de edição local, Adobe Firefly (referência) e Chaos (materiais/luz).