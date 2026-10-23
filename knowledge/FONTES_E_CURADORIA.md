# Fontes e curadoria — registro inicial

**Pesquisa consolidada em:** 2026-10-23. Fontes oficiais fundamentam **boas práticas**, não comprovam que qualquer prompt deste repositório tenha sido testado ou seja o 'melhor' em todas as ferramentas. Não copiar exemplos externos sem verificar a licença.

## Oficiais e de autores das ferramentas

1. **OpenAI — Image prompting:** https://developers.openai.com/api/docs/guides/image-prompting
   - Contribuição: resultado e composição explícitos; distinguir mudança de preservação; dar papéis às imagens; iterar com controle.
   - Limite: recomendações dependem de modelo e versão.
2. **Chaos — AI architecture prompts:** https://blog.chaos.com/ai-architecture-prompts
   - Contribuição: quando há SketchUp/Revit/croqui, usar o desenho para geometria e prompt para materiais, luz, entorno, câmera.
   - Limite: recomendações orientadas ao ecossistema Chaos; texto não garante fidelidade absoluta.
3. **Chaos — How to master Veras AI:** https://blog.chaos.com/how-to-master-veras-ai-architects-prompt-guide
   - Contribuição: estrutura tarefa + atributos + restrições, câmera e refinamento por variável.
4. **Google — Gemini image prompt tips:** https://blog.google/products-and-platforms/products/gemini/image-generation-prompting-tips/
   - Contribuição: sujeito, composição, estilo, local, ação e instruções diretas para edições.
5. **Adobe Firefly — Referência de composição:** https://helpx.adobe.com/br/firefly/web/work-with-images/generate-images/match-image-composition-to-reference-image.html
   - Contribuição: diferenciar estrutura da cena e estilo; referência e intensidade de aderência.
6. **Midjourney — Image Prompts:** https://docs.midjourney.com/hc/en-us/articles/32040250122381-Image-Prompts
7. **Midjourney — Style Reference:** https://docs.midjourney.com/hc/en-us/articles/32180011136653-Style-Reference
   - Contribuição: imagem como inspiração de composição versus referência de estilo. Parâmetros só valem no produto e versão correspondentes.
8. **Runway — Gen-4 Video Prompting Guide:** https://help.runwayml.com/hc/en-us/articles/39789879462419-Gen-4-Video-Prompting-Guide
9. **Runway Academy — Prompting Guide:** https://academy.runwayml.com/guides/prompting-guide
   - Contribuição: texto para image-to-video descreve movimento, câmera e progressão temporal; shots simples e curtos.

## Repositórios de referência técnica

- **Awesome Nano Banana Spatial Design:** https://github.com/qzh3722/awesome-nano-banana-spatial-design — exemplifica receitas por atividade de projeto. README menciona CC BY 4.0; exigir atribuição se derivar conteúdo.
- **GPT Image Design Prompts:** https://github.com/linlhf/gptimage-design-prompts — exemplo de classificação de insumo (planta, foto, whitebox) e objetivo antes de criar prompt; revisar a licença no repositório.
- **ARCHI Render:** https://github.com/dakhlallah/arch-render — exemplo de distinção observado/inferido e regras de preservação do projeto.

**Atribuição:** os prompts desta V1 são redigidos originalmente para o ArchRender Hub, baseados em princípios gerais de documentação. Links são referências, não endosso e não autorização para republicar imagens.

## Critérios de qualidade das futuras fontes

Classificar cada exemplo pesquisado com:
- URL original e data de observação;
- ferramenta/modelo e versão verificáveis;
- prompt completo, entradas e configurações;
- presença de pares antes/depois, quando a tarefa é edição;
- clareza sobre pós-produção e intervenção humana;
- licença, crédito e autorização para reuso;
- falhas relatadas e condições de replicação.

**Não promover** um prompt a 'aprovado' só por likes, estrelas, imagem bonita ou propaganda. Considerar resultados consistentes em pelo menos duas entradas independentes para recomendação ampla. Registrar failures/custos também.

## Técnicas por problema

| Problema | Técnica preferida | Falha comum |
| --- | --- | --- |
| Planta humanizada de layout aprovado | Base em vista superior + preservação + verificação visual | Abrir/fechar paredes ou mover portas |
| Fotografia da fachada → nova pintura | Edição local/material reference | Deformar aberturas |
| Modelo cinza → exterior realista | Materiais e luz sem redesenhar volumes | Inventar pavimentos e inclinações |
| Interior existente → conceito de decoração | Definir elementos fixos e alterações permitidas | Ampliar cômodo ou mover esquadrias |
| Imagem → vídeo curto | Shot único, movimento de câmera suave | Alucinar face oculta da construção |
| Planta técnica cotada | CAD/BIM/fonte dimensional e revisão humana | IA inventar cotas |

## Limites honestos

Nenhuma combinação de palavras elimina sozinha deriva geométrica, erros de escala, textos ilegíveis, inconsistência temporal ou risco de copyright. Avaliar sempre a saída real.