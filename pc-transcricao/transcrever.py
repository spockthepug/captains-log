"""Teste de transcrição local (caminho C): transcreve áudios em português no próprio PC.

Uso:
    .venv\\Scripts\\python.exe pc-transcricao\\transcrever.py ARQUIVO [ARQUIVO ...] [--modelo small]

Mostra o texto e quanto tempo levou. Nada sai do computador: o modelo é baixado
uma vez (na primeira execução) e depois roda offline.
"""

import argparse
import time

from faster_whisper import WhisperModel


def main():
    parser = argparse.ArgumentParser(description="Transcreve áudios em português no PC.")
    parser.add_argument("arquivos", nargs="+", help="áudios (.wav, .mp3, .m4a, .ogg, .opus...)")
    parser.add_argument("--modelo", default="small", help="tiny, base, small, medium, large-v3-turbo, large-v3")
    args = parser.parse_args()

    inicio = time.perf_counter()
    # int8 deixa o modelo mais leve e rápido no processador, com perda mínima de qualidade.
    modelo = WhisperModel(args.modelo, device="cpu", compute_type="int8")
    print(f"[modelo {args.modelo} carregado em {time.perf_counter() - inicio:.1f}s]")

    for arquivo in args.arquivos:
        inicio = time.perf_counter()
        trechos, info = modelo.transcribe(arquivo, language="pt", vad_filter=True)
        texto = " ".join(t.text.strip() for t in trechos)
        gasto = time.perf_counter() - inicio
        print(f"\n== {arquivo}")
        print(f"[áudio de {info.duration:.0f}s transcrito em {gasto:.1f}s]")
        print(texto)


if __name__ == "__main__":
    main()
