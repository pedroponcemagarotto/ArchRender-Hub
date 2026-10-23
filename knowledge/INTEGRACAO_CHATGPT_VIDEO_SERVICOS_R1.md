# ArchRender Hub — vídeo por conectores ChatGPT / serviços

**Verificação:** 2026-10-23. **Status:** pesquisa de preços e conectores confirmada; serviços **não conectados nem testados com arquivos privados**, nenhuma geração paga executada.

## Fluxo esperado

1. ChatGPT analisa o render original, produz uma imagem fotorrealista e confere as alterações.
2. Usuário aprova a imagem. Manter a entrada privada.
3. ChatGPT solicita a um **conector autenticado** gerar vídeo a partir da imagem, usando instruções de câmera extremamente discretas.
4. Antes de usar créditos, listar ferramenta/modelo, duração, resolução, custo estimado e saldo; **solicitar aprovação explícita de gasto**. Uma nova tentativa também consome crédito.
5. Serviço devolve MP4/asset visualizável; verificar coerência das aberturas e dos móveis no primeiro, médio e último quadros; rejeitar deformações.
6. Quando disponível, juntar as cenas em MP4 com o gerador gratuito `tools/video_local.py` ou Shotcut; nada de credenciais no GitHub.

**Limitação da integração:** o ChatGPT pode criar uma imagem e entregá-la como referência ao conector quando estiver instalado/conectado, mas a passagem automática de um arquivo gerado anteriormente depende dos formatos de entrada expostos pelo plugin; se ele não receber a imagem direta da conversa, poderá ser necessário anexá-la novamente. **A existência do conector não demonstra que o workflow ponta a ponta foi homologado.**

## Recomendação por custo e simplicidade

| Opção | Integração no ChatGPT | Custos verificados | Prioridade |
| --- | --- | --- | --- |
| **[Runway](https://runway.com/pt-br/mcp/chatgpt)** | **Plugin disponível no Diretório**; o usuário deve instalar e conectar a própria conta Runway, sem chave de API | Conta Free: **125 créditos única vez**; não renovam, acesso a modelos limitado e vídeo com marca d'água. Standard: **US$15/mês mensal** ou equivalente **US$12/mês no plano anual**, 625 créditos por mês. Vídeo Gen-4 Turbo consta no help como **25 créditos por 5s** (crédito e disponibilidade variam; confirmar no painel). | **1 — primeira homologação com créditos gratuitos** |
| **[Higgsfield](https://higgsfield.ai/mcp)** | Plugin disponível no Diretório; login Higgsfield | **Gerações via MCP/ChatGPT usam créditos sempre**. Gerações gratuitas ou ilimitadas do website **não se transferem ao conector**. Planos/promoções variáveis. | **2 — comparar se for usar créditos pagos** |
| **[Luma Ray 3.2 API](https://lumalabs.ai/api)** | **Não foi identificado plugin nativo Luma** na busca atual; requer uma integração/custom bridge/API key para trabalhar automaticamente a partir do ChatGPT | Cobrança por uso sem mensalidade: **US$0,15/5s em 540p, US$0,30/5s em 720p, US$1,20/5s em 1080p**. Tarifas e disponibilidade podem mudar. | **3 — economicamente interessante para produção regular, porém exige trabalho de integração** |
| **DepthFlow / FFmpeg locais** | Não funcionam por plugin remoto; acessados no PC por fluxo de trabalho local | **R$0 por geração**, custos de energia/PC; DepthFlow é parallax 2.5D, FFmpeg é edição e movimentos 2D, nenhum cria movimento de cena por difusão | Alternativa sem gasto de créditos |

**Importante:** para economia real, não apresentar preços de créditos de serviços diferentes como comparáveis diretamente. "125 créditos" da Runway não equivalem a 125 créditos de outro provedor. Preços em US$ sem conversão cambial.

## Runway — primeira experiência sugerida

- Instalar o plugin Runway no ChatGPT e conectar o login do usuário. Conferir conta gratuita/saldo; **não pedir cartão** para o teste se a plataforma não exigir.
- Testar **um único vídeo curto (5s)** com a imagem **aprovada da cozinha/sala**, após conferir sua capacidade de receber o arquivo, modelo habilitado e o custo mostrado. Se Gen-4 Turbo não estiver permitido no Free ou no plugin, não assumir alternativa sem custo.
- Prompt de movimento curto: `Use this supplied approved interior image as the exact first frame. A gentle slow 5-second push-in, almost imperceptible movement. Keep the existing sofa, refrigerator, L-shaped counter, sink, windows, walls and corridor structurally unchanged. No furniture appearing or disappearing; no new windows, doors or rooms. Preserve exposure and material identity; stable geometry, no wobble. Cinematic architectural photography.`
- Confirmar se imagem do ChatGPT passa automaticamente ou precisa de reanexo.
- Analisar artefatos no quadro 0, centro e final; nomear resultado como **vídeo gerado por IA, fidelidade não garantida**, até avaliação profissional.
- **Não usar todo o saldo** numa comparação; reter crédito para repetição após encontrar falha.

## Higgsfield — ressalva de custo

A [documentação oficial da integração](https://higgsfield.ai/creator-hub/help-center/integrations/how-do-i-connect-higgsfield-to-ai-agent) e [explicação de créditos](https://higgsfield.ai/creator-hub/help-center/credits/how-credits-work) dizem que **todas as gerações pela integração MCP/ChatGPT consomem créditos**, mesmo quando o website oferece gerações grátis/ilimitadas. O modelo, resolução e duração definem preço. Não vender como solução gratuita automática.

## Luma — alternativa barata por vídeo, mas não um plugin pronto

A [tabela de preços oficial](https://docs.agents.lumalabs.ai/guides/pricing) apresenta custo por vídeo sem compromisso mínimo. Para automatizar, precisaria desenvolver uma interface autorizada que receba a imagem do ChatGPT, armazene temporariamente em localização segura acessível ao provedor e chame a API com conta/chave do usuário; retorno/gestão de falhas e revisão do custo precisam ser implementados. **Não desenvolver nem ativar cobranças sem autorização explícita**. Nunca enviar projeto de cliente para endpoint público sem política de privacidade aprovada.

## Regras do ArchRender Hub para plugins externos

- Não transmitir imagem de cliente antes da autorização do usuário e da ciência de que o arquivo sai do ambiente ChatGPT para o provedor.
- Nunca assumir que o plano do ChatGPT concede créditos gratuitos no Runway, Higgsfield ou Luma; contas independentes.
- Enviar imagem de **um ambiente só** por vez, não uma colagem involuntária de lavanderia e cozinha; prever um take por cena.
- Evitar cenas que revelam geometria fora do enquadramento quando não existir modelo 3D; para walkthrough real usar CAD/BIM/Blender.
- Sem assinatura automática, sem refil automático de créditos, sem compra de créditos não autorizada.
- Registrar status `pesquisado` / `conector_disponivel` / `conectado` / `imagem_enviada` / `video_gerado` / `QA_aprovado`; nunca saltar etapas.
- Manter fotos, renders, prompts privados e MP4 fora do repositório público.

## Fontes oficiais consultadas (23/10/2026)

- Runway: [integração ChatGPT](https://runway.com/pt-br/mcp/chatgpt), [free plan](https://help.runwayml.com/hc/en-us/articles/50404627334547-Free-plan-details), [preços](https://runway.com/pricing), [Gen-4 Turbo 5s](https://help.runwayml.com/hc/en-us/articles/37327109429011-Creating-with-Gen-4-Video), [MCP e créditos](https://help.runwayml.com/hc/en-us/articles/51931843164691-Connecting-to-Runway-MCP).
- Higgsfield: [ChatGPT plugin](https://higgsfield.ai/mcp), [geração por agentes sempre desconta créditos](https://higgsfield.ai/creator-hub/help-center/integrations/how-do-i-connect-higgsfield-to-ai-agent).
- Luma: [API](https://lumalabs.ai/api), [preços detalhados](https://docs.agents.lumalabs.ai/guides/pricing).
