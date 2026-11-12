# Fractions and Decimals: Multiplication and Division

A narrated ManimGL lesson for Class 7 maths, drawn on a white board. The voice-over is in Hinglish, read slowly (0.70× speed). The lesson covers:

| Chapter | What is shown |
|---|---|
| Intro | Recap of addition and subtraction, plus a roadmap of the four operations |
| Multiplying fractions | 2/3 × 5/7 = (2×5)/(3×7) = 10/21, built up step by step |
| Fraction as "of" | 1/2 of 2 = 1, using two rotis |
| Size of the product | Number-line comparisons: proper×proper, proper×improper, improper×improper |
| Reciprocal | 3/5 flips upside down into 5/3 |
| Dividing fractions | 2 ÷ 3/5 = 10/3 · 2/3 ÷ 7 = 2/21 · 2/3 ÷ 5/7 = 14/15 |
| Multiplying decimals | 0.5 × 0.7: multiply as whole numbers, count decimal places, place the point |
| × 10, 100, 1000 | 0.53 → 5.3 → 53 → 530, with the decimal point hopping right |
| Decimal ÷ whole number | 8.4 ÷ 4 = 2.1 |
| ÷ 10, 100, 1000 | 23.9 → 2.39 → 0.239 → 0.0239, with the point hopping left |
| Decimal ÷ decimal | 2.4 ÷ 0.2 = 24 ÷ 2 = 12 |
| Summary | Revision cards and a goodbye |


## Render

```sh
# full lesson, 1080p, with voice-over
manimgl fractions_decimals/fractions_decimals.py FractionsAndDecimals -w --hd

# a quick low-quality preview of a single chapter
manimgl fractions_decimals/fractions_decimals.py DividingDecimals -w -l
```

The individual chapter scenes are `Intro`, `MultiplyingFractions`, `DividingFractions`, `MultiplyingDecimals`, `DividingDecimals` and `Summary`.

The video ends up in `videos/`. LaTeX and FFmpeg are required, as for any ManimGL scene.

## Voice-over (Hinglish)

The `voiceover/` folder already contains the clips, so rendering works without any extra setup.

The script is in `narration.py`. Each line is stored twice:

- Roman-script Hinglish ("Toh answer aaya ten by twenty one"), used for the optional subtitles.
- The same words in Devanagari ("तो आंसर आया टेन बाई ट्वेंटी वन"), read by the voice. Writing the English words in Devanagari gives them a natural Indian classroom pronunciation.

If you edit a line, change both versions, then regenerate the clips:

```sh
pip install kokoro-onnx soundfile
python fractions_decimals/generate_voiceover.py --force                 # all clips
python fractions_decimals/generate_voiceover.py --only mul_2 mul_3      # just some
python fractions_decimals/generate_voiceover.py --force --speed 0.8     # a bit faster
python fractions_decimals/generate_voiceover.py --force --voice hf_alpha  # female voice
```

The clips come from [Kokoro](https://github.com/thewh1teagle/kokoro-onnx), an offline text-to-speech model with Hindi voices:

- `hm_omega` (male, the default)
- `hm_psi` (male)
- `hf_alpha` (female)
- `hf_beta` (female)

The default speed is 0.70. The model files (~350 MB) download into `tts_model/` on the first run.

Each `with self.voice("key"):` block in the scene plays one clip. The animations inside the block run while the clip plays, and the scene then waits until the clip has finished, so the video stays in sync if you change the wording. If a clip is missing, the scene still renders silently and estimates the timing from the word count.

Subtitles are off by default. Set `subtitles = True` on `VoiceScene` to show the Roman Hinglish text at the bottom of the screen.
