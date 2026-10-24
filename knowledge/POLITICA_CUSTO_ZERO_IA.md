# ArchRender Hub — Política vinculante de custo zero adicional para inteligência artificial

**Decisão do usuário:** 23/10/2026.  
**Prioridade:** P0 (regra superior a recomendações anteriores de arquitetura e provedores).  
**Projeto:** ArchRender Hub · PR #1 Draft `feat/prompt-system-v1`.  
**Orçamento de IA adicional:** **R$ 0**. A única assinatura de IA aceita é **a assinatura do ChatGPT que o usuário já possui**.

## 1. Regra de arquitetura

**Nenhum componente do Hub pode exigir ou disparar cobrança adicional por IA.** Sem adquirir créditos, adicionar cartão ou gerar imagens/vídeos por API paga ou serviço externo cuja execução gere cobrança. Não habilitar recargas, upgrades, pagamentos, contratação de planos de teste ou consumo de créditos tarifáveis. Não criar fallback pago silencioso. Antes de integrar um motor, comprovar o custo real de uso e registrar em documentação.

**Proibido no fluxo padrão:**
- APIs pagas de geração/edição de imagem/vídeo (inclusive API OpenAI, fal.ai, Replicate, Luma API, Runway pago, Higgsfield pago, Kling pago etc.).
- Licenças, assinaturas, créditos de geração ou aluguel de GPU em nuvem **para IA** não aprovados.
- Automatizar o login pessoal do ChatGPT para contornar cobrança de API, extrair cookies/sessões/tokens ou presumir que uma assinatura pode ser reutilizada como backend externo.
- Depender de créditos gratuitos temporários de terceiros como requisito de funcionamento. Testes gratuitos podem ser considerados apenas quando não exigirem custo/contratação nem comprometerem dados, e jamais como caminho primário.

**Permitido:**
1. **Ferramentas nativas incluídas no ChatGPT**, nesta própria conversa, sujeitas à disponibilidade e limites do plano e da ferramenta. O usuário envia uma imagem, o ChatGPT cria/edita; o Hub pode receber o arquivo resultado manualmente. A transmissão direta para qualquer sistema externo **não está automaticamente disponível**.
2. **Processamento local gratuito** com modelos e licenças adequados: Krita (grátis), Krita AI Diffusion, ComfyUI, modelos locais permitidos de Stable Diffusion/ControlNet, ferramentas open-source de upscale quando necessário. GPU Dell G15 opcional. Consumo de energia, armazenamento e necessidade de equipamento não equivalem à assinatura IA, mas devem ser informados.
3. **Operações determinísticas gratuitas**, no próprio Hub ou em browser/servidor já disponível: máscaras, composição, comparação/QA R3-R5, correções de cor, redimensionamento, preparação de prompts, histórico.
4. **Integrações que usem uma franquia incluída do próprio ChatGPT**, somente quando um parceiro oficial oferecer explicitamente esse mecanismo para o **plano do usuário**, sem qualquer cobrança adicional; exigir autorização explícita, confirmação de elegibilidade, limites de uso e segurança, e nunca supor disponibilidade. Isto NÃO autoriza chamar a API paga da OpenAI sem faturamento.

## 2. Diferença técnica decisiva: assinatura ChatGPT vs API

A assinatura pessoal/de workspace do ChatGPT e a plataforma API da OpenAI possuem **faturamentos separados**, segundo [OpenAI Help Center — Managing billing for ChatGPT and the API platform](https://help.openai.com/en/articles/9039756-managing-billing-for-chatgpt-and-the-api-platform). Logo:

- Um aplicativo independente no browser **não pode simplesmente utilizar a assinatura do ChatGPT como chave de API gratuita**.
- A geração/edição feita **nesta conversa** pode usar os recursos do ChatGPT, mas deve respeitar limites de uso e a possibilidade de a ferramenta não receber corretamente a imagem original como entrada.
- [Entrar com o ChatGPT — uso do plano em apps/sites participantes](https://help.openai.com/pt-br/articles/20001542-using-your-chatgpt-plan-in-other-apps-and-sites) é uma capacidade **condicional**, disponível somente nas ferramentas, planos e usos elegíveis e mediante autorização do usuário. **NÃO considerar integrada nem disponível no ArchRender Hub** sem homologação específica; não contar com ela para a arquitetura atual.

## 3. Arquitetura aprovada, sem compromisso com pagamento

```text
                 USUARIO (web/celular)
                         |
                 ARCHRENDER HUB
             /                           \
     Preparar e validar              Escolher caminho
    mascaras, QA, arquivos                 |
            |                  +-----------+------------+
            |                  |                        |
            |         CHATGPT NESTA CONVERSA       IA LOCAL GRATUITA
            |        criacao/edicao dentro        ComfyUI + Krita
            |         do plano existente         GPU Dell opcional
            |          (transferencia manual)     (quando online)
            |                  |                        |
            +------------------+------------------------+
                         |
              Compositor R5 + QA R4
                         |
              Revisao humana e arquivo
```

**Sem PC Host:** pode-se desenvolver e usar o Hub para preparar/validar imagens, máscaras e relatórios; a IA do ChatGPT continua acessível nesta conversa, com eventual transferência manual de arquivos. **Não prometer geração automática pelo website fora do ChatGPT sem um provedor realmente gratuito e disponível.**

**Com PC Host:** integrar o ComfyUI em backend local após instalação, permitindo futuras operações image-to-image automáticas sem crédito por geração. Dell G15: RTX 3060 ~6GB, 16GB RAM; desempenho real e capacidade de modelos ainda exigem teste no Windows. Não expor endpoints locais à Internet sem autenticação e proteção.

**UI independente:** pode existir e ser publicada sem API paga; não deve mostrar botão de geração automática na nuvem que silenciosamente falhe, simule a geração ou acione cobrança.

## 4. Política verificável de engenharia

- Em catálogos e configurações de provedores, `ai_extra_budget_brl=0` e `allow_paid_ai=false` são condições imutáveis até **nova autorização explícita do usuário**.
- Modos iniciais permitidos: `chatgpt_manual`, `comfyui_local` (desabilitado até homologação), `offline_editing`. Todo motor remoto pago ou não comprovadamente gratuito deve permanecer `disabled`.
- Não armazenar tokens de APIs de terceiros, nem adicionar métodos de pagamento ou tarefas pagas.
- Toda futura proposta de conector inclui custos, limites, licença, privacidade e prova de não cobrança. Se uma operação passar a exigir pagamento, **bloqueie-a e ofereça opção gratuita**, nunca troque de provedor automaticamente.
- Custos de **hospedagem/domínio/armazenamento** não são custos diretos de IA, mas também não devem ser assumidos sem orçamento e autorização próprios; priorizar recursos existentes e gratuitos.
- Arquivos de projetos de clientes ficam privados; não os publicar em GitHub, sites externos ou fóruns sem autorização.
- No QA, melhorar uma cena sem provar uso da referência original ou respeitar regiões protegidas não constitui homologação; benchmark A/B/C permanece 0/6 enquanto não houver seis edições elegíveis.

## 5. Consequências no roadmap

| Frente | Decisão |
| --- | --- |
| R3-R5 — receitas, comparação, QA e máscaras | **Manter e desenvolver**, sem GPU e sem API paga |
| Interface web independente | **Manter**, preparada para geração manual via ChatGPT e motor local futuro |
| ComfyUI + Krita AI Diffusion | **Manter como único backend generativo automatizável principal** no desenho atual, pendente de PC |
| API OpenAI Images / Responses paga | **NÃO integrar ou contratar** |
| fal.ai / Replicate / Luma / Runway / Higgsfield pagos | **NÃO integrar nem comprar créditos** |
| Serviços em nuvem somente com créditos promocionais | **Não usar como dependência estrutural** |
| Benchmark público/privado e pesquisas em fóruns | **Continuar**, com modelos, imagens e operações realmente gratuitos |

## 6. Fontes e rastreabilidade

- [OpenAI: faturamento ChatGPT × API](https://help.openai.com/en/articles/9039756-managing-billing-for-chatgpt-and-the-api-platform), verificado em 23/10/2026.
- [OpenAI: usar plano do ChatGPT em apps participantes](https://help.openai.com/pt-br/articles/20001542-using-your-chatgpt-plan-in-other-apps-and-sites), verificado em 23/10/2026. Elegibilidade do Hub **não verificada**.
- [Krita AI Diffusion, projeto aberto](https://github.com/Acly/krita-ai-diffusion).
- [ComfyUI Image-to-Image](https://docs.comfy.org/tutorials/basic/image-to-image).

**Esta é uma política de orçamento, não uma afirmação de que ChatGPT possui geração ilimitada nem de que ComfyUI já está instalado no PC Host.**
