import os
import time
from pathlib import Path
import math

# Ініціалізація змінних (Щоб уникнути помилок AttributeError)
volume_control = None
PYCAW_LOADED = False
SBC_LOADED = False

# --- Блок гучності ---
try:
    from ctypes import cast, POINTER
    from comtypes import CLSCTX_ALL
    from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume_control = cast(interface, POINTER(IAudioEndpointVolume))
    PYCAW_LOADED = True
    print("✅ utils: Модуль 'pycaw' завантажено.")
except Exception as e:
    print(f"⚠️ utils: Гучність недоступна ({e})")
    PYCAW_LOADED = False

# --- Блок яскравості ---
try:
    import screen_brightness_control as sbc

    SBC_LOADED = True
    print("✅ utils: Модуль 'sbc' завантажено.")
except Exception as e:
    print(f"⚠️ utils: Яскравість недоступна ({e})")
    SBC_LOADED = False


# --- ФУНКЦІЇ (Імпорти перенесено всередину!) ---

def tell_time():
    from tts import speak  # <--- ВАЖЛИВО: Імпорт тут
    now = time.strftime("%H годин %M хвилин")
    speak(f"Зараз {now}")


def tell_date():
    from tts import speak
    now = time.strftime("%d %B %Y року")
    speak(f"Сьогодні {now}")


def open_browser(url=""):
    from tts import speak
    if url:
        speak(f"Відкриваю {url.split('.')[0]}.")
        os.system(f"start chrome {url}")
    else:
        speak("Відкриваю браузер.")
        os.system("start chrome")


def open_calculator():
    from tts import speak
    speak("Запускаю калькулятор.")
    os.system("calc")


def open_notepad():
    from tts import speak
    speak("Відкриваю блокнот.")
    os.system("notepad")


def open_explorer():
    from tts import speak
    speak("Відкриваю провідник.")
    os.system("explorer")


def shutdown_pc():
    from tts import speak
    speak("Вимикаю комп’ютер через хвилину.")
    # os.system("shutdown /s /t 60")


def cancel_shutdown():
    from tts import speak
    speak("Вимкнення скасовано.")
    # os.system("shutdown /a")


def open_google():
    open_browser("google.com")


def open_youtube():
    open_browser("youtube.com")


def open_wikipedia():
    open_browser("uk.wikipedia.org")


def create_note():
    from tts import speak
    from speech import take_command  # <--- ВАЖЛИВО
    speak("Що ви хочете записати в нотатку?")
    note_text = take_command(timeout=15, phrase_time_limit=30)

    if note_text == "none":
        speak("Не вдалося розпізнати текст.")
        return

    desktop_path = Path.home() / "Desktop"
    note_filename = f"Нотатка_{time.strftime('%Y-%m-%d_%H%M%S')}.txt"
    full_path = desktop_path / note_filename

    try:
        with open(full_path, 'w', encoding='utf-8') as f:
            f.write(note_text.capitalize())
        speak(f"Нотатку збережено.")
        os.system(f"notepad {full_path}")
    except Exception as e:
        speak("Помилка збереження.")
        print(e)


def set_master_volume(level_percent: int):
    from tts import speak

    # Якщо модуль не завантажено (наприклад, на CI), просто виходимо
    if not PYCAW_LOADED or volume_control is None:
        return

    if 0 <= level_percent <= 100:
        scalar_level = level_percent / 100.0
        volume_control.SetMasterVolumeLevelScalar(scalar_level, None)
        speak(f"Гучність {level_percent} відсотків.")
    else:
        # Текст повідомлення має збігатися з features/tom_volume.feature
        speak("Рівень має бути від 0 до 100.")


def change_volume(step_percent: int):
    from tts import speak
    if not PYCAW_LOADED or volume_control is None:
        return

    current_scalar = volume_control.GetMasterVolumeLevelScalar()
    current_percent = round(current_scalar * 100)
    new_percent = max(0, min(100, current_percent + step_percent))
    set_master_volume(new_percent)


def toggle_mute():
    from tts import speak
    if not PYCAW_LOADED or volume_control is None:
        return
    is_muted = volume_control.GetMute()
    volume_control.SetMute(not is_muted, None)
    speak("Звук перемкнено.")


def set_brightness(level_percent: int):
    from tts import speak
    if not SBC_LOADED: return
    if 0 <= level_percent <= 100:
        try:
            sbc.set_brightness(level_percent)
            speak(f"Яскравість {level_percent}.")
        except:
            pass


def change_brightness(step_percent: int):
    from tts import speak
    if not SBC_LOADED: return
    try:
        current = sbc.get_brightness(display=0)[0]
        set_brightness(max(0, min(100, current + step_percent)))
    except:
        pass