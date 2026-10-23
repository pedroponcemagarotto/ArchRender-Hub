# AR-WHITEBOX-001 — Croqui / whitebox / screenshot de modelo para render

**Versão:** 1.0 | **Estado:** candidato_nao_testado | **Modo:** F.

## Caso ideal

O usuário fornece uma imagem exportada de SketchUp, Revit, Rhino, Archicad, Blender ou desenho perspectivado. O objetivo é enriquecer a aparência **sem reinterpretar a massa construída**. Arquivo nativo pode exigir exportação para imagem antes de chegar ao modelo visual.

## Prompt-mestre

~~~text
TAREFA: Converta a Imagem 1, que é um [CROQUI / PRINT DE MODELO 3D / WHITEBOX], em uma imagem de visualização arquitetônica realista adequada à fase [ESTUDO / APROVAÇÃO].

LEITURA: trate linhas de contorno, junções, recessos, vazios, aberturas, pisos, coberturas e altura relativa mostrados no insumo como dados de projeto. Quando uma linha ou elemento estiver ambíguo, evite atribuir função estrutural não confirmada.

PRESERVAÇÃO: manter topologia visual e enquadramento, proporções relativas, níveis, posição das paredes, volumes, portas e janelas, telhados/lajes e direção das perspectivas. Não completar a face oculta do edifício como fato; se uma vista diferente for solicitada sem geometria 3D, avisar que será hipótese.

ACABAMENTO: paredes [MATERIAL], madeira [MATERIAL], piso [MATERIAL], vidros/metais [MATERIAL]. Diferenciar discretamente juntas, rugosidade, reflexos e sujeição de materiais sem alterar volumes.

ENTORNO: completar apenas elementos secundários autorizados [VEGETAÇÃO / PISO / CÉU / MOBILIÁRIO SOLTO] onde a fonte deixa espaço. Não inserir edifícios vizinhos, muros, piscinas, acessos ou patamares não informados.

LUZ E CÂMERA: câmera compatível com a fonte, sombras naturais, verticais coerentes; iluminação [HORA] com exposição equilibrada. Resultado fotográfico sem aparência de maquete digital.

SAÍDA: gerar uma imagem no mesmo sentido de enquadramento, com os mesmos volumes legíveis e aumento perceptível de realismo. Depois identificar diferenças em relação à Imagem 1.
~~~

## Correções comuns

- Se uma janela desaparecer: corrigir apenas região correspondente a partir do original; nunca redesenhar a fachada toda como primeira tentativa.
- Se linhas estruturais se tornarem decorativas: recuperar a linha do input e restringir criação de texturas à superfície.
- Se material migrar para local errado: usar referência com papel explícito e alvo local.

## Aprovação

A qualidade visual não compensa divergência geométrica. Se o render altera planta, número de vãos ou volumes, reprová-lo.