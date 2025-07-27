import pytest
from unittest.mock import MagicMock
from openai import OpenAI


from src.ai_essay_gen.ai_interact import make_ai_prompt, AIRequestError


def test_make_ai_prompt_returns_correct_content():
    response_content = "Dummy Content"
    model_name = "Model Name"
    system_message = "System Message"
    prompt = "some prompt"

    mock_ai_client = MagicMock()
    mock_response = MagicMock()
    mock_response.choices = [MagicMock()]
    mock_response.choices[0].message.content = response_content
    mock_ai_client.chat.completions.create.return_value = mock_response

    # Act: Call the function with the generated inputs
    result = make_ai_prompt(prompt, mock_ai_client, model_name, system_message)

    # Assert 1: The function returns the expected content
    assert result == response_content

    # Assert 2: The API was called with the correct parameters
    mock_ai_client.chat.completions.create.assert_called_once_with(
        model=model_name,
        n=1,
        messages=[
            {"role": "system", "content": system_message},
            {"role": "user", "content": prompt},
        ],
    )


def test_make_ai_prompt_connection_error():
    ai = OpenAI(api_key="cddf", base_url="https://dfdsfs.com/v1")
    model_name = "gemini"
    system_message = "testing"
    prompt = "dfsd"

    with pytest.raises(AIRequestError) as ai_request_error:
        make_ai_prompt(prompt, ai, model_name, system_message)

    assert (
        str(ai_request_error.value)
        == f"Request to {model_name} returned with error: Connection error."
    )

def test_make_ai_prompt_fails_empty():
    ai = OpenAI(api_key="cddf", base_url="https://dfdsfs.com/v1")
    model_name = "gemini"
    prompt = ""

    with pytest.raises(AIRequestError) as ai_request_error:
        make_ai_prompt(prompt=prompt, ai_client=ai, model_name=model_name, system_message="testing")

    assert (
        str(ai_request_error.value)
        == "Prompt to an AI Model needs contain words"
    )