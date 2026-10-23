# ArchRender Hub R3 — verificação operacional inicial

**Data:** 2026-10-23  
**PR:** https://github.com/pedroponcemagarotto/ArchRender-Hub/pull/1  
**Nível:** verificações estruturais + *smoke test* local isolado de uma **reconstrução do módulo**, não homologação do app inteiro nem do PC Host.

## Verificações de GitHub (fonte original)

- PR #1: **aberta, Draft**, destino `main`; a branch de trabalho estava **38 commits à frente, zero atrás**, no momento da verificação.
- Repositório contém as **nove receitas** do catálogo, com IDs únicos e caminhos válidos.
- As nove receitas possuem ao menos um bloco textual de prompt reconhecível pelo extrator `~~~text`.
- Foram verificados na branch: `ROADMAP_OPERACIONAL_INTEGRADO_R3.md`, `tools/metodo_integrado.py`, `tests/test_metodo_integrado.py`, `research/testes/AR-BENCH-001_CASO_INTERIORES_R3.md` e ligações de documentos de entrada.
- Código do novo módulo se limita à biblioteca padrão do Python, grava em `data/workflows/` e não chama provedor/API de IA.
- **Nenhum merge**, nenhuma alteração a `main`, nenhum GitHub Actions.

## Smoke tests executados localmente

Em ambiente Linux Python 3.13, usando uma **cópia reconstruída** de `tools/metodo_integrado.py` com fixtures mínimas artificiais para as nove receitas (não os arquivos reais do repositório), foram executados:

| Check | Resultado | O que prova |
| --- | --- | --- |
| `python -m py_compile` da cópia | PASS | Sintaxe da reconstrução aceita pelo Python 3.13 |
| `list` | PASS | Mostra as nove rotas simuladas |
| `prepare --task interiores --variant C` | PASS | Cria JSON privado, prompt C e gates em `nao_avaliado` na reconstrução |
| `assess --geometry falhou ... --score 100` | PASS | Reprova apesar de nota 100, na reconstrução |
| `assess --geometry passou ... --score 92` | PASS | Status `candidato_a_revisao_humana`; `client_approved=false`, na reconstrução |
| Arquivos versionados de QA | PASS | Contrato original e revisões permanecem como arquivos distintos, na reconstrução |

**Limite obrigatório:** o SHA da cópia de código testada **não coincide exatamente** com o blob completo no GitHub; foram usados fixtures simplificados em vez das receitas reais. Portanto, **NÃO DECLARAR** que a suíte `tests/test_metodo_integrado.py` do repositório passou, nem que o novo módulo foi homologado no Windows/Dell G15. Os testes devem ser executados no checkout real para homologação. Este registro não deve ser usado como prova de qualidade visual de imagens.

## Testes ainda necessários antes de classificar o módulo como testado no produto

1. No checkout exato da PR, rodar `python -m unittest discover -s tests -v` e `python -m py_compile tools/metodo_integrado.py` em ambiente temporário, sem acessar o SQLite real.
2. Verificar o extrator com os nove arquivos reais, incluindo textos longos e placeholders.
3. Testar em Windows 10/11 com Python 3.9+ e `ARCHRENDER_DATA_DIR` em uma pasta segura, sem sobrescrever dados.
4. Rodar o benchmark com **referências reais autorizadas** (primeiro cozinha/sala), comparar pixels e anotar ancoras geométricas; meta piloto 0/6 ainda pendente.
5. Revisar a GUI somente depois de o módulo e o benchmark terem evidências suficientes.

**Status global:** integração metodológica e código auxiliar estão **incluídos na PR Draft**, com verificação estática e smoke test parcial. **Não** instalar terceiros e **não** promover para aprovado até a homologação real.

## Adendo — fontes da Internet, fóruns e regressão da versão-base (23/10/2026)

**Fonte verificada:** `catalog/fontes_publicas_r1.json`, com 7 IDs únicos, **2 cenas 3D e 5 fotos**, sete autores/links de licenças e todas as fontes no estado `acquired=false`, `benchmark_status=nao_executado`. Referências e método descritos em `research/CURADORIA_WEB_IMAGENS_FORUNS_R1.md`.

**Conector GitHub:** PR #1 aberta, Draft, `feat/prompt-system-v1` → `main`, **51 commits à frente e zero atrás** na verificação; nenhum `.png`, `.jpg`, `.jpeg`, `.webp`, `.blend`, `.fbx`, `.glb`, `.exr`, `.hdr` ou `.zip` entrou no diff da PR.

**Testes reais executados neste ambiente:**

```
Origem: /mnt/data/ArchRender_Hub_v0.1.0.zip
Ambiente: Python 3.13.5, Linux, arquivo ZIP da versão-base
Comando: python -m unittest discover -s tests -v
Resultado: Ran 6 tests in 1.002s — OK (6 aprovados)
```

Isso **comprova somente a regressão da versão-base V0.1 extraída do ZIP**. Não foi a suíte da branch atual nem prova de que os novos `tests/test_fontes_publicas.py` (5 casos) e `tests/test_metodo_integrado.py` passaram. Como o ambiente de execução do container não resolveu o host `github.com`, a branch não pôde ser clonada aqui. Verificações sobre novos arquivos foram estruturais (JSON, caminhos, presença do subcomando e gates do código).

**Próximo gate:** executar a suíte completa no checkout atual da PR, depois inspecionar/baixar uma cena de geometria conhecida pelo canal licenciado correto e produzir um benchmark com referência original de fato entregue ao gerador. **Nenhum benchmark público foi executado nesta atualização.**
