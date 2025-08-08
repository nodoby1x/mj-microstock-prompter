import unittest
from unittest.mock import patch, MagicMock
from controller import PrompterGenerator, AIProvider
import openai

class TestPrompterGenerator(unittest.TestCase):

    def setUp(self):
        self.api_key = "test_api_key"

    @patch('controller.genai')
    def test_gemini_initialization(self, mock_genai):
        """Test that the Gemini client is initialized correctly."""
        generator = PrompterGenerator(api_key=self.api_key, provider='gemini')
        mock_genai.configure.assert_called_with(api_key=self.api_key)
        mock_genai.GenerativeModel.assert_called_with(model_name='gemini-1.5-pro')
        self.assertEqual(generator.provider, AIProvider.GEMINI)

    @patch('controller.openai')
    def test_openai_initialization(self, mock_openai):
        """Test that the OpenAI client is initialized correctly."""
        generator = PrompterGenerator(api_key=self.api_key, provider='openai')
        self.assertEqual(mock_openai.api_key, self.api_key)
        mock_openai.OpenAI.assert_called_with(api_key=self.api_key)
        self.assertEqual(generator.provider, AIProvider.OPENAI)

    def test_initialization_with_no_api_key(self):
        """Test that the generator raises an error if no API key is provided."""
        with self.assertRaises(ValueError):
            PrompterGenerator(api_key=None)

    @patch('controller.genai.GenerativeModel')
    def test_prompt_generator_gemini(self, mock_gemini_model):
        """Test that the prompt generator returns a Gemini prompt."""
        mock_response = MagicMock()
        mock_response.text = "a test prompt"
        mock_gemini_model.return_value.generate_content.return_value = mock_response

        generator = PrompterGenerator(api_key=self.api_key, provider='gemini')
        result = generator.prompt_generator(main_base="test")

        self.assertEqual(result['text'], "a test prompt")
        self.assertEqual(result['provider'], 'gemini')

    @patch('controller.openai.OpenAI')
    def test_prompt_generator_openai(self, mock_openai_client):
        """Test that the prompt generator returns an OpenAI prompt."""
        mock_response = MagicMock()
        mock_response.choices[0].message.content = "a test prompt"
        mock_openai_client.return_value.chat.completions.create.return_value = mock_response

        generator = PrompterGenerator(api_key=self.api_key, provider='openai')
        result = generator.prompt_generator(main_base="test")

        self.assertEqual(result['text'], "a test prompt")
        self.assertEqual(result['provider'], 'openai')

if __name__ == '__main__':
    unittest.main()