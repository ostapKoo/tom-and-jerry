from unittest.mock import patch, MagicMock
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

def before_all(context):
    """Запускається перед усіма тестами. Тут ми ставимо глобальні Моки."""
    # 1. Мокаємо гучність (pycaw), щоб не змінювати реальну гучність ПК
    context.volume_patcher = patch('utils.volume_control')
    context.mock_volume = context.volume_patcher.start()

    # Налаштовуємо поведінку моку гучності
    context.mock_volume.GetMasterVolumeLevelScalar.return_value = 0.5

    # 2. Мокаємо озвучення (tts), щоб ПК мовчав під час тестів
    context.tts_patcher = patch('tts.speak')
    context.mock_speak = context.tts_patcher.start()

    import utils
    utils.PYCAW_LOADED = True


def after_all(context):
    """Прибираємо сміття після тестів."""
    context.volume_patcher.stop()
    context.tts_patcher.stop()