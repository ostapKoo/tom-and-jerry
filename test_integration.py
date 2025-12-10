import unittest
from unittest.mock import patch, MagicMock
import sys
import io


import utils
import gemini_client
import tts

class TestIntegrationComponents(unittest.TestCase):
    # --- ТЕСТ 1: ВНУТРІШНЯ ВЗАЄМОДІЯ (UTILS -> TTS) ---
    # Ми перевіряємо, чи дійсно функція tell_time викликає функцію speak.
    @patch('utils.speak')  # Ми робимо Spy/Mock для функції speak
    def test_utils_integrates_with_tts(self, mock_speak):
        """
        Integration Test: Перевірка того, що модуль utils коректно
        передає дані в модуль tts.
        """
        print("\n--- Running Integration Test: Utils -> TTS ---")
        utils.tell_time()
        # 2. Verification (Перевірка взаємодії)
        # Ми не перевіряємо, який саме час (це unit-тест),
        # ми перевіряємо ФАКТ виклику іншого компонента.
        self.assertTrue(mock_speak.called, "Помилка: utils.tell_time() не викликала tts.speak()")

        # Перевіряємо, що передано саме рядок
        args, _ = mock_speak.call_args
        print(f"Utils передав у TTS: '{args[0]}'")
        self.assertIn("Зараз", args[0])

    # --- ТЕСТ 2: ЗОВНІШНЯ ВЗАЄМОДІЯ (GEMINI CLIENT -> GOOGLE API) ---
    # (+30%).
    # Ми імітуємо відповідь Google, щоб не витрачати гроші/ліміти і не залежати від інтернету.

    @patch('gemini_client.model')  # Mock для об'єкта model всередині клієнта
    def test_gemini_client_integrates_with_api(self, mock_model):
        """
        Integration Test: Перевірка взаємодії клієнта з бібліотекою Google API
        з використанням Mock-об'єкта.
        """
        print("\n--- Running Integration Test: Gemini Client -> Google API (Mocked) ---")

        # 1. Setup (Налаштування Mock-об'єкта)
        # Створюємо фейковий об'єкт чату, який поверне фейкову відповідь
        mock_chat = MagicMock()
        mock_response = MagicMock()
        mock_response.text = "Це тестова відповідь від штучного інтелекту."

        # Налаштовуємо ланцюжок викликів: model.start_chat() -> chat.send_message() -> response
        mock_model.start_chat.return_value = mock_chat
        mock_chat.send_message.return_value = mock_response

        # 2. Action (Дія)
        # Ми викликаємо нашу функцію, думаючи, що це реальний Google
        user_prompt = "Хто ти?"
        result = gemini_client.ask_gemini(user_prompt)

        # 3. Verification (Перевірка)

        # Перевіряємо, що результат відповідає тому, що "повернув" Mock
        self.assertEqual(result, "Це тестова відповідь від штучного інтелекту.")

        # Перевіряємо, чи правильно наш клієнт сформував запит до API
        mock_chat.send_message.assert_called_once_with(user_prompt)
        print("Gemini Client успішно викликав метод send_message() у бібліотеки Google.")


if __name__ == '__main__':
    unittest.main()