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
- **Transcrição pelo Groq** (plano grátis, `whisper-large-v3`, `language=pt`), chamado direto do navegador
  (o Groq aceita CORS). A chave do dono fica só no `localStorage` (`captainslog.groq`), fora das prefs e
  dos backups; nunca escrever chave no código. Limite grátis: 25 MB por arquivo, 2 h de áudio por hora,
  8 h por dia. O Groq reconhece o formato pela extensão do nome do arquivo (`extGroq`: .opus vira .ogg).
- iPhone com Dynamic Island: o `.teto` fixo cobre `env(safe-area-inset-top)`; qualquer elemento fixo
  no topo precisa respeitar essa área.
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
   Para testar a transcrição sem chave real, substitua `window.fetch` para `api.groq.com` por uma
   resposta falsa (200 com `{text}`, 401, 429). Uma chave falsa contra o Groq real deve dar "recusou a chave".
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
   Publicado em https://spockthepug.github.io/captains-log/ (repo público `spockthepug/captains-log`, branch `main`).
   Falta: testar no celular de verdade.
   1b. **Áudios do WhatsApp:** o dono usa **iPhone**, onde PWA não recebe "Compartilhar" (sem `share_target`).
   Caminho: WhatsApp → Salvar em Arquivos → botão Importar. Falta confirmar que .opus toca no iPhone
   (se não tocar, a transcrição ainda funciona; avaliar converter ou só avisar).
2. ✅ **Transcrição** pelo Groq grátis (decidido em 2026-10-31): automática ao gravar/importar, fila que
   espera a internet voltar, botão "Transcrever"/"Tentar de novo", "Copiar texto". v0.2.0.
   O PC (faster-whisper em `pc-transcricao/`) fica como opção futura para áudios mais pessoais.
3. **Diário de bordo e Missões:** compromissos com data/hora, missões com prazo; alertas âmbar (a vencer)
   e vermelho (vencido) no Relatório de status.
4. **Assistente:** texto transcrito vira compromisso ou missão, sempre com confirmação.
   Decidir a IA: opção grátis (ex.: Groq) ou Claude pago por uso (exige cartão, perguntar antes).
5. **Saúde:** coletor de medidas do dono — peso, % de gordura, massa magra e outras (definir a lista na etapa),
   com histórico e gráfico; entrada manual ou por voz ("pesei 82,4"). PWA não lê o app Saúde da Apple.
   Dados sensíveis: ficam no aparelho; só passam por IA na nuvem se o dono aceitar.
6. **Pets:** vacinas, vermífugo, peso, consultas.
7. **Carro:** abastecimentos (km/l, custo por km, etanol ou gasolina), revisões, IPVA, seguro. Dinheiro em centavos.
8. **Sincronização** PC e celular pelo Google Drive (`appDataFolder`).

Depois, um por vez: Missões externas (viagens), lembretes com o app fechado, resumo do dia, contas,
assinaturas, vencimento de documentos, consultas e exames, casa, inventário, receitas, e-mail só leitura.
