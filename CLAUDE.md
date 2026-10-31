# Captain's Log

App pessoal de organização com assistente de áudio, no estilo "computador de bordo" de uma nave.
O dono não é programador: explique tudo em português, em linguagem simples. A ideia completa e as
decisões originais estão em [docs/PROJETO.md](docs/PROJETO.md).

## Arquivos

| Arquivo | O que é |
|---|---|
| `index.html` | O app inteiro: HTML, CSS e JavaScript puros, sem bibliotecas nem build. |
| `manifest.webmanifest` | Nome, cores e ícones para instalar como app (PWA). |
| `sw.js` | Service worker: guarda os arquivos para o app abrir sem internet. |
| `icons/` | Ícones PNG (gerados com System.Drawing do PowerShell). |
| `pc-transcricao/` | Teste de transcrição local com faster-whisper (caminho C). Usa o `.venv` da raiz. |
| `docs/PROJETO.md` | Documento original do projeto. |
| `CLAUDE.local.md` | Preferências pessoais e pendências (só neste PC, fora do Git). |

## Regras

- Só publicar no GitHub depois que o dono aprovar. Nada pago ou que exija cartão sem perguntar.
- Uma funcionalidade por vez.
- **Áudios ficam no IndexedDB** (banco `captains-log`, loja `registros`); o `localStorage` guarda só
  preferências (`captainslog.prefs`). Ele é pequeno demais para áudio.
- **Todo campo novo de dados entra em `normalizarRegistro()`** (e `normalizarPrefs()`), para registros
  e backups antigos continuarem funcionando.
- Valores de dinheiro, quando existirem, em **centavos** (inteiros).
- A cada publicação, aumentar `VERSION` no `sw.js` **e** `VERSAO` no `index.html`.
- Backups (`captains-log-backup-*.json`), chaves de API e áudios de teste **nunca** vão para o GitHub (ver `.gitignore`).
- A legibilidade no celular vence qualquer efeito visual.

## Como testar

1. Servidor local: `preview_start` com o nome `captains-log` (em `.claude/launch.json`), que roda
   `python -m http.server 8123`. Abre em http://localhost:8123.
2. Testar em tamanho de celular (375x812) e de computador, e ler o console por erros.
3. No localhost o service worker fica **desligado** para as mudanças aparecerem na hora.
   Para testar o modo offline, abra `http://localhost:8123/?sw=1` — e depois desregistre o
   service worker e apague os caches, senão o localhost passa a servir arquivos antigos.
4. O navegador embutido nega o microfone. Para testar a gravação, substitua
   `navigator.mediaDevices.getUserMedia` por um oscilador (`createMediaStreamDestination`).
   Para testar importação, use `pc-transcricao/testes/teste-voz-sintetica.wav`.
5. Ao terminar, apague os dados de teste do navegador (IndexedDB `captains-log` e `localStorage`).

## Estética

Painel de nave retrofuturista, tranquilo e um pouco divertido.

- Fundo azul-marinho (`#070F26`), tema claro opcional. Âmbar (`#F5B342`) é a cor principal, ciano
  (`#4FD1E8`) os destaques, vermelho só para alertas. Cores chapadas, sem gradientes.
- Cantos bem arredondados. Seções com **trilho colorido numerado** (01, 02…) à esquerda.
- Texto em fonte do sistema; números, datas e rótulos curtos em monoespaçada, em maiúsculas.
- Luzes indicadoras (ciano = ok, âmbar = atenção, vermelho piscando devagar = erro).
- Animações discretas (seções acendem ao abrir); respeitar `prefers-reduced-motion`.
- Bipes gerados com Web Audio (`bipe()`), com opção de desligar em Ajustes.

**Vocabulário:** tela inicial = "Relatório de status"; agenda = "Diário de bordo"; tarefas = "Missões";
viagens = "Missões externas"; a vencer = alerta âmbar; vencido = alerta vermelho. O computador fala
de forma educada e precisa, como o Data de Star Trek ("Bom dia, capitão. …").

## Roteiro

1. ✅ **Base:** gravar, abrir áudios existentes, lista, ouvir, baixar, apagar, backup, tema, bipes, PWA.
   Falta: publicar no GitHub Pages, testar no celular de verdade, receber áudio pelo "Compartilhar" do Android.
2. **Transcrição:** decidir entre Groq grátis (online) e PC (faster-whisper local).
3. **Diário de bordo e Missões** (agenda e tarefas).
4. **Assistente:** texto transcrito vira compromisso ou missão, sempre com confirmação.
5. **Pets**, depois **Carro**.
6. Sincronização PC e celular pelo Google Drive.
