import os
import time
from tts import speak
from speech import take_command
from pathlib import Path
import math  # Потрібен для гучності

# --- Блок для гучності (pycaw) ---
try:
    from ctypes import cast, POINTER
    from comtypes import CLSCTX_ALL
    from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

    # Отримуємо основний пристрій відтворення
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(
        IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume_control = cast(interface, POINTER(IAudioEndpointVolume))
    print("✅ Модуль 'pycaw' (гучність) завантажено.")
    PYCAW_LOADED = True
except Exception as e:
    print(f"❌ Помилка завантаження 'pycaw': {e}. Керування гучністю недоступне.")
    PYCAW_LOADED = False

# --- Блок для яскравості (screen-brightness-control) ---
try:
    import screen_brightness_control as sbc

    print("✅ Модуль 'screen_brightness_control' (яскравість) завантажено.")
    SBC_LOADED = True
except Exception as e:
    print(f"❌ Помилка завантаження 'screen_brightness_control': {e}. Керування яскравістю недоступне.")
    SBC_LOADED = False


# --- ОСНОВНІ КОМАНДИ СИСТЕМИ ---

def tell_time():
    """Повідомляє поточний час."""
    now = time.strftime("%H годин %M хвилин")
    speak(f"Зараз {now}")


def tell_date():
    """Повідомляє поточну дату."""
    now = time.strftime("%d %B %Y року")
    speak(f"Сьогодні {now}")


def open_browser(url=""):
    """Відкриває браузер (або конкретну URL)."""
    if url:
        speak(f"Відкриваю {url.split('.')[0]}.")
        os.system(f"start chrome {url}")
    else:
        speak("Відкриваю браузер.")
        os.system("start chrome")


def open_calculator():
    """Запускає калькулятор."""
    speak("Запускаю калькулятор.")
    os.system("calc")


def open_notepad():
    """Запускає блокнот."""
    speak("Відкриваю блокнот.")
    os.system("notepad")


def open_explorer():
    """Відкриває провідник файлів."""
    speak("Відкриваю провідник.")
    os.system("explorer")


def shutdown_pc():
    """Вимикає комп'ютер (із затримкою)."""
    speak("Вимикаю комп’ютер через хвилину. Скажіть 'скасувати', щоб зупинити.")
    print("⚠️ Вимкнення закоментовано для безпеки.")
    # os.system("shutdown /s /t 60") # 60 секунд на вимкнення


def cancel_shutdown():
    """Скасовує вимкнення."""
    speak("Вимкнення скасовано.")
    print("⚠️ Скасування вимкнення.")
    # os.system("shutdown /a")


# --- КОМАНДИ ДЛЯ ІНТЕРНЕТУ ---

def open_google():
    open_browser("google.com")


def open_youtube():
    open_browser("youtube.com")


def open_wikipedia():
    open_browser("uk.wikipedia.org")


# --- ПРОДУКТИВНІСТЬ ---

def create_note():
    """Створює текстову нотатку на робочому столі."""
    speak("Що ви хочете записати в нотатку?")

    # Використовуємо довший таймаут для диктування
    note_text = take_command(timeout=15, phrase_time_limit=30)

    if note_text == "none":
        speak("Не вдалося розпізнати текст. Спробуйте ще раз.")
        return

    # Знаходимо шлях до Робочого столу
    desktop_path = Path.home() / "Desktop"
    note_filename = f"Нотатка_{time.strftime('%Y-%m-%d_%H%M%S')}.txt"
    full_path = desktop_path / note_filename

    try:
        with open(full_path, 'w', encoding='utf-8') as f:
            f.write(note_text.capitalize())

        speak(f"Нотатку збережено на робочому столі як {note_filename}")
        print(f"✅ Нотатку збережено: {full_path}")
        # Відкриваємо створену нотатку
        os.system(f"notepad {full_path}")

    except Exception as e:
        speak("Не вдалося зберегти нотатку.")
        print(f"❌ Помилка збереження нотатки: {e}")


# --- КЕРУВАННЯ ГУЧНІСТЮ ---

def set_master_volume(level_percent: int):
    """Встановлює гучність системи (0-100)."""
    if not PYCAW_LOADED:
        speak("Модуль керування гучністю 'pycaw' недоступний.")
        return

    if 0 <= level_percent <= 100:
        # pycaw використовує шкалу від 0.0 до 1.0
        scalar_level = level_percent / 100.0
        volume_control.SetMasterVolumeLevelScalar(scalar_level, None)
        speak(f"Гучність встановлено на {level_percent} відсотків.")
    else:
        speak("Рівень гучності має бути від 0 до 100.")


def change_volume(step_percent: int):
    """Змінює гучність на крок (наприклад, +10 або -10)."""
    if not PYCAW_LOADED:
        speak("Модуль керування гучністю 'pycaw' недоступний.")
        return

    current_scalar = volume_control.GetMasterVolumeLevelScalar()
    current_percent = round(current_scalar * 100)

    new_percent = current_percent + step_percent

    if new_percent > 100:
        new_percent = 100
    if new_percent < 0:
        new_percent = 0

    set_master_volume(new_percent)


def toggle_mute():
    """Вмикає або вимикає звук."""
    if not PYCAW_LOADED:
        speak("Модуль керування гучністю 'pycaw' недоступний.")
        return

    is_muted = volume_control.GetMute()
    if is_muted:
        volume_control.SetMute(0, None)
        speak("Звук увімкнено.")
    else:
        volume_control.SetMute(1, None)
        speak("Звук вимкнено.")


# --- КЕРУВАННЯ ЯСКРАВІСТЮ ---

def set_brightness(level_percent: int):
    """Встановлює яскравість (0-100)."""
    if not SBC_LOADED:
        speak("Модуль керування яскравістю недоступний.")
        return

    if 0 <= level_percent <= 100:
        try:
            sbc.set_brightness(level_percent)
            speak(f"Яскравість встановлено на {level_percent} відсотків.")
        except Exception as e:
            speak("Не вдалося змінити яскравість.")
            print(f"Помилка sbc: {e}")
    else:
        speak("Рівень яскравості має бути від 0 до 100.")


def change_brightness(step_percent: int):
    """Змінює яскравість на крок (наприклад, +10 або -10)."""
    if not SBC_LOADED:
        speak("Модуль керування яскравістю недоступний.")
        return

    try:
        # Отримуємо поточну яскравість (беремо середнє, якщо кілька моніторів)
        current_brightness_list = sbc.get_brightness(display=0)
        current_percent = int(current_brightness_list[0])

        new_percent = current_percent + step_percent

        if new_percent > 100:
            new_percent = 100
        if new_percent < 0:
            new_percent = 0

        set_brightness(new_percent)
    except Exception as e:
        speak("Не вдалося отримати поточну яскравість.")
        print(f"Помилка sbc: {e}")