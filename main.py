from tts import speak
from speech import take_command
from modes.tom_mode import run_tom_mode
from modes.jerry_mode import run_jerry_mode


def main_assistant():
    speak("Асистент Том і Джері активовано. Скажіть 'Том' або 'Джері'.")

    while True:
        # Cлухаємо тільки ключові слова
        query = take_command(timeout=5, phrase_time_limit=5)
        if query == "none":
            continue

        # Використовуємо розширений список для кращого розпізнавання "Том"
        if any(x in query for x in ["том", "тома", "тон", "дом", "там", "дім", "томас"]):
            run_tom_mode()
            # Коли ми вийшли з режиму Тома, знову пропонуємо вибір
            speak("Виберіть режим: Том або Джері.")

        elif any(x in query for x in ["джері", "джорі", "жері", "джеррі"]):
            run_jerry_mode()
            # Коли ми вийшли з режиму Джері, знову пропонуємо вибір
            speak("Виберіть режим: Том або Джері.")

        elif any(x in query for x in ["вихід", "зупинити", "стоп", "до побачення"]):
            speak("До побачення! Асистент завершує роботу.")
            break


if __name__ == "__main__":
    main_assistant()