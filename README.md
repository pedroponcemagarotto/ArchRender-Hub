# ArchRender Hub — V0.1.0

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
