from gtts import gTTS
from pydub import AudioSegment
import simpleaudio as sa
import io


def speak(text: str):
    """Озвучує текст українською (виправлена версія gTTS)."""

    mp3_fp = io.BytesIO()
    wav_io = io.BytesIO()

    try:
        print(f"🔊 Асистент: {text}")
        tts = gTTS(text=text, lang='uk')

        # Виправлений метод: записуємо у потік пам'яті
        tts.write_to_fp(mp3_fp)
        mp3_fp.seek(0)

        # Конвертуємо MP3 (з mp3_fp) у WAV (в wav_io)
        audio_segment = AudioSegment.from_file(mp3_fp, format="mp3")

        audio_segment.export(wav_io, format="wav")
        wav_io.seek(0)

        # Відтворюємо WAV
        wave_obj = sa.WaveObject.from_wave_file(wav_io)
        play_obj = wave_obj.play()
        play_obj.wait_done()

    except Exception as e:
        print(f"❌ Помилка озвучення (gTTS): {e}")
    finally:
        mp3_fp.close()
        wav_io.close()