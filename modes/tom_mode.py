from tts import speak
from speech import take_command
import utils


def _parse_number_from_query(query: str) -> int | None:
    """Допоміжна функція для пошуку числа у запиті."""
    for word in query.split():
        if word.isdigit():
            try:
                num = int(word)
                if 0 <= num <= 100:
                    return num
            except ValueError:
                continue
    return None


def run_tom_mode():
    speak("Режим Тома активовано. Готовий до команд.")

    while True:
        query = take_command()
        if query == "none":
            continue

        # --- Навігація ---
        if any(x in query for x in ["назад", "головне меню", "вихід", "джері"]):
            speak("Повертаюся до вибору асистента.")
            break

        # --- Керування гучністю (перевірка pycaw) ---
        elif "голосніше" in query or "збільшити звук" in query:
            utils.change_volume(10)
        elif "тихіше" in query or "зменшити звук" in query:
            utils.change_volume(-10)
        elif "вимкни звук" in query or "ввімкни звук" in query or "тиша" in query:
            utils.toggle_mute()
        elif "гучність" in query or "звук на" in query:
            level = _parse_number_from_query(query)
            if level is not None:
                utils.set_master_volume(level)
            else:
                # Якщо pycaw вимкнено, він все одно скаже, що модуль недоступний
                utils.set_master_volume(0)

                # --- Керування яскравістю (ВИПРАВЛЕНА ЛОГІКА) ---

        # 1. Спочатку перевіряємо відносні зміни
        elif "яскравіше" in query or "збільшити яскравість" in query:
            utils.change_brightness(15)  # +15%

        elif "темніше" in query or "зменшити яскравість" in query:
            utils.change_brightness(-15)  # -15%

        # 2. Потім перевіряємо абсолютні (з числом)
        #    Тепер реагує на "яскравість 70" та "яркість 50"
        elif "яскравість" in query or "яркість" in query:
            level = _parse_number_from_query(query)
            if level is not None:
                # Знайшли число!
                utils.set_brightness(level)
            else:
                # Сказали "яскравість", але без числа
                speak("Не розпізнала рівень. Повторіть, наприклад: 'яскравість 70'.")

        # --- Час / Дата ---
        elif "час" in query or "котра година" in query:
            utils.tell_time()

        elif "дата" in query or "який сьогодні день" in query:
            utils.tell_date()

        # --- Запуск програм ---
        elif "калькулятор" in query:
            utils.open_calculator()

        elif "блокнот" in query:
            utils.open_notepad()

        elif "провідник" in query or "файли" in query:
            utils.open_explorer()

        # --- Інтернет ---
        elif "браузер" in query:
            utils.open_browser()
        elif "google" in query:
            utils.open_google()
        elif "youtube" in query:
            utils.open_youtube()
        elif "вікіпеді" in query:
            utils.open_wikipedia()

        # --- Продуктивність ---
        elif "нотатк" in query or "запис" in query or "запиши" in query:
            utils.create_note()

        # --- Керування живленням ---
        elif "вимкни комп’ютер" in query:
            utils.shutdown_pc()
        elif "скасувати вимкнення" in query or "скасуй" in query:
            utils.cancel_shutdown()

        # --- Якщо команда не розпізнана ---
        else:
            speak("Команда не розпізнана.")
            print(f"Невідома команда для Тома: {query}")