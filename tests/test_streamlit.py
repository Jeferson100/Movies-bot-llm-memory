from streamlit.testing.v1 import AppTest
from app_streamlit import clear_messages
import pytest
from unittest.mock import patch


def test_no_interaction():
    at = AppTest.from_file("app_streamlit.py")
    at.secrets["password"] = "streamlit"
    at.run()
    assert at.session_state["config"] == {"configurable": {"session_id": "foo"}}
    assert at.session_state["store"] == {}
    assert at.session_state["messages"] == []
    assert len(at.title) == 1
    assert len(at.chat_input) == 1
    assert len(at.button) == 1
    assert len(at.markdown) >= 10
    assert len(at.sidebar) == 12


@pytest.fixture
def setup_session_state():
    clear_messages()
    yield
    clear_messages()


def test_chat_resposta_condicional_true():
    # Crie uma função mock para chat_reposta_condicional
    mock_response = "filme de ação"

    # Use o patch para substituir chat_reposta_condicional pela função mock
    with patch("app_streamlit.chat_reposta_condicional", return_value=mock_response):
        # Crie uma instância de AppTest
        at = AppTest.from_file("app_streamlit.py", default_timeout=300)

        # Execute o app
        at.run()

        # pylint: disable=no-member
        at.chat_input[0].set_value("Qual é o melhor filme de ação?").run()
        # pylint: disable=no-member
        # Verifique se a resposta do assistente é a esperada
        assistant_message = at.chat_message[-1]
        assert assistant_message is not None


def test_chat_resposta_condicional_false():
    # Crie uma função mock para chat_reposta_condicional
    mock_response = "filme de ação"

    # Use o patch para substituir chat_reposta_condicional pela função mock
    with patch("app_streamlit.chat_reposta_condicional", return_value=mock_response):
        # Crie uma instância de AppTest
        at = AppTest.from_file("app_streamlit.py", default_timeout=300)

        # Execute o app
        at.run()

        # pylint: disable=no-member
        at.chat_input[0].set_value("Bom dia").run()
        # pylint: disable=no-member
        # Verifique se a resposta do assistente é a esperada
        assistant_message = at.chat_message[-1]
        assert assistant_message is not None
