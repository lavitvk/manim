"""
Generate the Indian-accented English voice-over for the lesson.

Uses the offline Kokoro TTS model (via ``kokoro-onnx``) with one of its
Hindi-native voices.  Feeding English text through a Hindi voice gives
natural sounding Indian-English speech, and everything runs locally.

Setup (one time):

    pip install kokoro-onnx soundfile
    # model files (~350 MB) are downloaded automatically on first run

Usage:

    python fractions_decimals/generate_voiceover.py              # all clips
    python fractions_decimals/generate_voiceover.py --voice hf_alpha
    python fractions_decimals/generate_voiceover.py --only mul_1 mul_2

Available Indian voices: hm_omega (male, default), hm_psi (male),
hf_alpha (female), hf_beta (female).
"""
import argparse
import os
import sys
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

from narration import NARRATION  # noqa: E402

MODEL_DIR = os.path.join(HERE, "tts_model")
VOICE_DIR = os.path.join(HERE, "voiceover")
BASE_URL = "https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/"
MODEL_FILES = ["kokoro-v1.0.onnx", "voices-v1.0.bin"]


def ensure_model(model_dir):
    os.makedirs(model_dir, exist_ok=True)
    for name in MODEL_FILES:
        path = os.path.join(model_dir, name)
        if not os.path.exists(path):
            print(f"Downloading {name} ...")
            urllib.request.urlretrieve(BASE_URL + name, path)
    return [os.path.join(model_dir, n) for n in MODEL_FILES]


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--voice", default="hm_omega", help="Kokoro voice (hm_omega, hm_psi, hf_alpha, hf_beta)")
    parser.add_argument("--speed", type=float, default=0.92, help="Speaking speed (1.0 = normal)")
    parser.add_argument("--model-dir", default=MODEL_DIR)
    parser.add_argument("--only", nargs="*", help="Only regenerate these clip keys")
    parser.add_argument("--force", action="store_true", help="Overwrite existing clips")
    args = parser.parse_args()

    import soundfile as sf
    from kokoro_onnx import Kokoro
    from pydub import AudioSegment

    model_path, voices_path = ensure_model(args.model_dir)
    kokoro = Kokoro(model_path, voices_path)
    os.makedirs(VOICE_DIR, exist_ok=True)

    keys = args.only or list(NARRATION)
    for key in keys:
        out = os.path.join(VOICE_DIR, f"{key}.mp3")
        if os.path.exists(out) and not args.force and not args.only:
            continue
        # English phonemes + Hindi voice = Indian English accent
        samples, rate = kokoro.create(NARRATION[key], voice=args.voice, speed=args.speed, lang="en-us")
        wav = out[:-4] + ".wav"
        sf.write(wav, samples, rate)
        AudioSegment.from_wav(wav).export(out, format="mp3", bitrate="96k")
        os.remove(wav)
        print(f"{key:8s} {len(samples) / rate:5.1f}s  {out}")


if __name__ == "__main__":
    main()
