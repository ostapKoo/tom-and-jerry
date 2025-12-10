import speech_recognition as sr
import os
import time
from google import genai
from google.genai.errors import APIError
from gtts import gTTS
from pydub import AudioSegment
import simpleaudio as sa
import io

# --- КОНФІГУРАЦІЯ ТА ІНІЦІАЛІЗАЦІЯ ---

GEMINI_API_KEY = "AIzaSyBkhXrvb4PGvqjXRE-Dtc75I4bW7SPzIGA"  # 🔒 встав свій ключ сюди
os.environ['GEMINI_API_KEY'] = GEMINI_API_KEY

try:
    client = genai.Client()
    GEMINI_MODEL = 'gemini-2.0-flash'
    print(f"✅ Gemini ініціалізовано. Модель: {GEMINI_MODEL}")
except Exception as e:
    print(f"❌ Помилка підключення до Gemini: {e}")
    client = None

r = sr.Recognizer()



def speak(text):
    """Озвучує текст українською через gTTS."""
    temp_file = "temp.mp3"
    try:
        print(f"🔊 Асистент: {text}")
        tts = gTTS(text=text, lang='uk')
        tts.save(temp_file)

        audio_segment = AudioSegment.from_mp3(temp_file)
        wav_io = io.BytesIO()
        audio_segment.export(wav_io, format="wav", parameters=["-ac", "1", "-ar", "44100"])
        wav_io.seek(0)

        play_obj = sa.play_buffer(
            wav_io.read(),
            num_channels=1,
            bytes_per_sample=2,
            sample_rate=44100
        )

        play_obj.wait_done()
        os.remove(temp_file)
    except Exception as e:
        print(f"❌ Помилка озвучення: {e}")


# --- РОЗПІЗНАВАННЯ ГОЛОСУ ---
def take_command(timeout=10, phrase_time_limit=10):
    """Слухає мікрофон і повертає розпізнаний текст українською."""
    try:
        with sr.Microphone() as source:
            print("\n🎤 Говоріть зараз...")
            r.adjust_for_ambient_noise(source, duration=1)
            print(f"🔧 Energy threshold: {r.energy_threshold}")

            try:
                audio = r.listen(source, timeout=timeout, phrase_time_limit=phrase_time_limit)
                print("🧠 Розпізнавання...")
                query = r.recognize_google(audio, language='uk-UA')
                print(f"👤 Розпізнано: '{query}'")
                return query.lower()
            except sr.WaitTimeoutError:
                print("⌛ Не почуто голосу.")
                return "none"
            except sr.UnknownValueError:
                print("❌ Не вдалося розпізнати голос.")
                return "none"
            except sr.RequestError:
                print("❌ Проблема з Google Speech Recognition.")
                return "none"
    except Exception as e:
        print(f"❌ Помилка мікрофона: {e}")
        return "none"


# --- РЕЖИМ TOM ---
def run_tom_mode():
    speak("Режим Тома активовано. Готовий до команд.")
    while True:
        query = take_command(timeout=10, phrase_time_limit=15)

        if query == "none":
            continue

        if any(x in query for x in ["назад", "головне меню", "вихід"]):
            speak("Повертаюся до вибору асистента.")
            break

        if "браузер" in query:
            speak("Відкриваю браузер.")
            os.system("start chrome")
        elif "калькулятор" in query:
            speak("Запускаю калькулятор.")
            os.system("calc")
        elif "час" in query or "котра година" in query:
            now = time.strftime("%H годин %M хвилин")
            speak(f"Зараз {now}")
        elif "вимкни комп’ютер" in query:
            speak("Вимикаю комп’ютер.")
            # os.system("shutdown /s /t 1")
            print("⚠️ Вимкнення закоментоване для безпеки.")
        else:
            speak("Команда не розпізнана.")
            print(f"Невідома команда: {query}")


# --- РЕЖИМ JERRY ---
def run_jerry_mode():
    speak("Режим Джері активовано. Слухаю вас.")
    while True:
        query = take_command(timeout=10, phrase_time_limit=15)
        if query == "none":
            continue
        if "назад" in query or "головне меню" in query:
            speak("Повертаюся до головного меню.")
            break

        if client is None:
            speak("Немає підключення до Gemini.")
            continue

        try:
            response = client.models.generate_content(
                model=GEMINI_MODEL,
                contents=query,
                config={
                    "system_instruction": "Відповідай українською, коротко і по суті."
                }
            )
            answer = response.text
            print(f"\n🤖 Джері: {answer}")
            speak(answer[:400])
        except Exception as e:
            print(f"❌ Помилка Gemini: {e}")
            speak("Не вдалося отримати відповідь.")


# --- ГОЛОВНИЙ ЦИКЛ ---
def main_assistant():
    print("\n📁 Асистент Том і Джері активований.")
    speak("Асистент Том і Джері активовано. Скажіть 'Том' або 'Джері'.")

    while True:
        query = take_command(timeout=10, phrase_time_limit=10)
        if query == "none":
            continue

        print(f"🗣️ Ви сказали: {query}")

        # Усі можливі варіації для активації
        if any(x in query for x in ["том", "тома", "тон", "дом"]):
            speak("Ви обрали режим Тома.")
            run_tom_mode()
        elif any(x in query for x in ["джері", "джорі", "жері", "джеррі"]):
            speak("Ви обрали режим Джері.")
            run_jerry_mode()
        elif any(x in query for x in ["вихід", "зупинити", "стоп"]):
            speak("До побачення! Асистент завершує роботу.")
            break


if __name__ == "__main__":
    main_assistant()
