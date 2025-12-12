import subprocess
import textwrap

# 🔧 CONTROLLA questi path
PIPER_BINARY = "/home/cagliostro88/piper/piper/piper"
PIPER_MODEL = "/home/cagliostro88/piper/piper/it_IT-riccardo-x_low.onnx"

def speak(text: str):
    """
    Fa leggere a Riccardo il testo passato.
    Usa Piper e manda l'audio direttamente alla scheda audio (aplay).
    """
    if not text:
        return

    # Togliamo newline e accorciamo se è esageratamente lungo
    text = text.replace("\n", " ")
    text = textwrap.shorten(text, width=600, placeholder="...")

    # Comando shell:
    # echo "testo" | piper --model ... --output_raw | aplay ...
    cmd = (
        f'echo "{text}" '
        f'| "{PIPER_BINARY}" --model "{PIPER_MODEL}" --output_raw '
        f'| aplay -r 22050 -f S16_LE -t raw -'
    )

    subprocess.run(cmd, shell=True, check=False)