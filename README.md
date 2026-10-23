# ArchRender Hub — V0.1.0


> **Fluxo visual com ChatGPT:** a V0.1 abaixo é um catálogo local. O novo [Prompt System v1](PROMPT_SYSTEM_v1.md) reúne receitas especializadas para produção assistida de plantas humanizadas, plantas baixas, fachadas, interiores, paisagismo e vídeos; consulte [protocolo](knowledge/OPERACAO_COM_CHATGPT.md) e [fontes](knowledge/FONTES_E_CURADORIA.md). **O usuário solicita a imagem e o ChatGPT a cria com ferramenta disponível; o banco local não gera imagens nem vídeos sozinho.** Prompts do V1 estão em status de candidatos até passarem por testes reais.

Biblioteca **local e privada** de prompts e receitas para visualização arquitetônica. Interface em português do Brasil. Não precisa de Docker, GPU, API paga ou conta na nuvem. Construída com Python (biblioteca padrão), SQLite, HTML, CSS e JavaScript.

> **Estado:** MVP local para uso individual. As receitas de demonstração são exemplos autorais sem renders gerados. Os resultados dos prompts não foram testados em serviços externos. Não é CAD/BIM e nenhuma regra textual garante a preservação de geometria: valide a imagem gerada contra os desenhos do projeto.

## Primeiros passos no Windows

1. Instale **Python 3.9 ou superior**, com o lançador `py` ou Python no PATH. Para verificar, abra o Terminal e execute `py -3 --version` ou `python --version`.
2. Extraia este ZIP, preferencialmente em uma pasta do disco D, por exemplo `D:\Projetos\ArchRender-Hub\`. Não execute o app de dentro do ZIP.
3. Dê dois cliques em **`INICIAR_WINDOWS.bat`**. O navegador deverá abrir em **http://127.0.0.1:8765/**.
4. **Mantenha a janela de terminal aberta** enquanto estiver usando a plataforma. Para encerrar, pressione `Ctrl+C`.
5. Para salvar backups, vá a **Backup e dados → Baixar backup**.

Em Linux/macOS: `./iniciar_linux_mac.sh`. Em qualquer sistema: `python3 app.py --no-browser` e abra manualmente o URL informado.

Se a porta 8765 estiver em uso: `python app.py --port 8766`. Para evitar abrir o navegador: `python app.py --no-browser`.

## Localização dos dados

O banco SQLite e os arquivos de imagem ficam em `data/`, **fora** do repositório versionado. Para escolher outro local use a variável de ambiente `ARCHRENDER_DATA_DIR`. Exemplo PowerShell:

```powershell
$env:ARCHRENDER_DATA_DIR = 'D:\Dados\ArchRender-Hub'
py -3 app.py
```

O servidor escuta exclusivamente em `127.0.0.1` e não transmite prompts/imagens a terceiros. Isto **não significa criptografia dos arquivos no disco**: proteja o computador e os backups. Evite salvar imagens de clientes sem autorização.

## Funcionalidades V0.1

- Biblioteca com busca instantânea, filtros por categoria/ferramenta, ordenação e favoritos.
- 10 receitas autorais de exemplo, sem resultados artificiais atribuídos a testes inexistentes.
- Cadastro/edição/exclusão/duplicação de receitas, etiquetas, detalhes de materiais, iluminação, restrições e anotações.
- Imagens antes/depois (PNG, JPEG, WebP até 8 MB cada), com comparador visual deslizante.
- Criador local de prompts estruturados a partir de formulário, com cópia e opção de salvar na biblioteca.
- Backup portátil em JSON contendo receitas, favoritos e imagens (limites atuais: até 90 MB de imagens na exportação e arquivo de restauração até 120 MB).
- Funciona offline após ser instalado. **Não gera imagens por IA** nesta versão.

## Segurança e limitações

- A aplicação foi desenhada para **uma única pessoa, no próprio PC**. Não a exponha diretamente na internet nem altere o bind para `0.0.0.0`.
- Sem login/múltiplos usuários. Backups não são criptografados; exportações podem conter imagens privadas.
- O importador repõe registros pelo ID: IDs coincidentes são substituídos. Faça uma exportação antes da restauração.
- Limite de exibição inicial: 2.000 receitas. A limpeza de imagens órfãs e backups grandes via streaming estão previstas para versões futuras.
- No Windows, se `app.py` rodar a partir de uma pasta protegida, extraia o projeto para uma pasta em que você tenha permissão de gravação.
- Licença: MIT para o código deste MVP. Prompts e imagens enviados por usuários são de seus respectivos titulares.

## Testes

```bash
python -m unittest discover -s tests -v
python -m py_compile app.py
```

A suíte abre um servidor temporário e usa um banco em uma pasta temporária; **não modifica seus dados reais**.

## Estrutura

```
archrender-hub-v0.1.0/
  app.py                      # servidor HTTP local e API JSON
  static/index.html           # interface em pt-BR
  static/style.css            # visual responsivo
  static/app.js               # interações e criador de prompts
  static/favicon.svg
  tests/test_api.py           # testes de API e regressão
  data/.gitkeep               # banco e uploads surgem no primeiro uso
  INICIAR_WINDOWS.bat         # atalho de execução Windows
  iniciar_linux_mac.sh
```

## Integração futura e GitHub

Este ZIP está pronto para ser iniciado em um repositório Git próprio. Para publicação, **não** envie a pasta `data/`. A versão 0.2 pode oferecer geração por provedor selecionável (Gemini, OpenAI ou outro) mediante chave própria, autorização e limites explícitos de custo. Nenhuma chamada externa é feita na V0.1.

## Fontes e licença do conteúdo

As receitas de demonstração foram escritas para este projeto e não são reproduções de prompts de repositórios alheios. Antes de importar receitas ou imagens de outras fontes, verifique atribuição, termos de uso e autorização do autor.


## Novo complemento experimental: vídeos gratuitos no próprio PC

Além da biblioteca V0.1, esta branch disponibiliza um **gerador independente de MP4 offline**, com interface Windows em \`INICIAR_VIDEO_WINDOWS.bat\`, GUI Python e FFmpeg. É opcional, **não substitui** o app atual, não requer GPU, Docker, assinatura nem API paga e não envia imagens para a internet. Usa fotos/renders aprovados e realiza *pan*, *zoom* suave e transições; **não** gera vídeo com IA, pessoas em movimento nem visita 3D autêntica.

**Como usar no Windows:** instale o FFmpeg gratuito pelo site oficial https://ffmpeg.org/download.html, configure-o no PATH (ou selecione o executável na GUI), execute \`INICIAR_VIDEO_WINDOWS.bat\`, selecione imagens, ordene os planos, escolha 720p/1080p e salve o MP4. Para títulos/músicas, use o editor gratuito [Shotcut](https://shotcut.com/). Para animação de profundidade opcional, investigamos [DepthFlow](https://github.com/BrokenSource/DepthFlow) sob sua licença AGPL-3.0; não está instalado ou integrado como dependência.

- [Manual do vídeo gratuito](knowledge/VIDEO_GRATUITO_PC.md)
- [Métodos de projetos GitHub incorporados](knowledge/INTEGRACOES_GITHUB_R1.md)
- [Roteador de receitas do ChatGPT](knowledge/ROTEADOR_DE_RECEITAS_R1.md)
- [Testes do complemento](tests/test_video_local.py) — verificação local com FFmpeg quando presente; não há GitHub Actions.

**Status:** este complemento entrou como código na PR de desenvolvimento e o fluxo de FFmpeg foi experimentado no ambiente de teste com 2 imagens e um MP4 de 7,5 s/720p. **O PC Host não foi homologado** (conector desconectado na verificação). As imagens e o vídeo de demonstração não foram enviados ao GitHub público. Não confundir o novo gerador com função do banco local V0.1: o inicializador de vídeo é separado.

## Método integrado R3 — imagens arquitetônicas primeiro

O [Roadmap Operacional Integrado R3](ROADMAP_OPERACIONAL_INTEGRADO_R3.md) organiza o aprendizado dos repositórios externos numa sequência auditável: **entrada original → receita apropriada → prompt A/B/C → gate geométrico → comparação visual → registro privado**. A integração atual utiliza **conceitos autorais e arquivos locais**; não instala automaticamente ControlNet, modelos terceiros ou conectores pagos.

O novo roteador **isolado do aplicativo V0.1** está em `tools/metodo_integrado.py` (Python 3.9+, somente biblioteca padrão). Ele lista as nove receitas, prepara contratos de prompts e registra avaliação humana em `data/workflows/`, pasta ignorada pelo Git. **Não** analisa pixels sozinho, não gera imagem, não concede aprovação de cliente e não modifica a base SQLite.

```bash
python tools/metodo_integrado.py list
python tools/metodo_integrado.py prepare --task interiores --variant C --reference-id ref-cozinha-001 --preserve "janelas originais" --preserve "geladeira original" --change "melhorar luz"
python -m unittest discover -s tests -v
```

O primeiro experimento comparativo está definido em [AR-BENCH-001 (cozinha/sala)](research/testes/AR-BENCH-001_CASO_INTERIORES_R3.md), com **seis gerações A/B/C pendentes** (não confundir com os experimentos exploratórios anteriores). Imagens privadas não entram no repositório.

**Situação:** documentação e ferramenta auxiliar incorporadas à PR Draft; o benchmark R3 não foi executado. Interface local V0.1 permanece inalterada. A homologação no PC Host e o acoplamento do roteador à interface são fases posteriores.


## Curadoria pública de imagens e atualização de fóruns — R1

O Hub agora inclui um [catálogo de sete fontes públicas rastreáveis](catalog/fontes_publicas_r1.json) com duas cenas 3D (geometria verificável) e cinco fotografias de interiores/lavanderia/fachadas, mais uma [política de pesquisa de fóruns e licenças](research/CURADORIA_WEB_IMAGENS_FORUNS_R1.md).

```bash
python tools/metodo_integrado.py sources
python tools/metodo_integrado.py sources --category fachadas
python tools/metodo_integrado.py sources --json
```

O comando **só consulta metadados locais**; não acessa a internet, não baixa fotos, não gera render e não substitui os originais particulares do usuário. O GitHub contém links e crédito, **não imagens de terceiros**. As fontes serão usadas em benchmarks públicos **se e quando o gerador receber o arquivo de entrada real**, observadas as condições de licenciamento. Para cada lote relevante, a pesquisa de fóruns e documentos oficiais passa a ser etapa regular.

**Status inicial:** 7 fontes curadas; **0 fontes baixadas, 0 testes públicos R1 executados**, R3-04 cozinha/sala privada ainda 0/6.
