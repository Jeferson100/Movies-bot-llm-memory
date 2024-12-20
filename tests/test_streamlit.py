from streamlit.testing.v1 import AppTest
from app_streamlit import  clear_messages, chat_reposta_condicional
import pytest
from unittest.mock import patch

def test_no_interaction():
    at = AppTest.from_file("app_streamlit.py")
    at.secrets["password"] = "streamlit"
    at.run()
    assert at.session_state['config'] == {"configurable": {"session_id": "foo"}}
    assert at.session_state['store'] == {}
    assert at.session_state['messages'] == []
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

def test_chat_input():
    at = AppTest.from_file("app_streamlit.py", default_timeout=100)
    at.secrets
    at.run()
    prompt = at.chat_input[0].placeholder
    # Defina um valor para o chat_input e execute novamente
    at.chat_input[0].set_value("Olá, Streamlit!")
    
    # Verifique se o valor foi definido corretamente
    assert at.chat_input[0].value == "Olá, Streamlit!"
    assert prompt == "Me pergunte sobre filmes?"

from unittest.mock import patch

def test_chat_input_and_response_with_mock():
    # Crie uma função mock para chat_reposta_condicional
    mock_response = "filme de ação"
    
    # Use o patch para substituir chat_reposta_condicional pela função mock
    with patch('test_streamlit.chat_reposta_condicional', return_value=mock_response):
        # Crie uma instância de AppTest
        at = AppTest.from_file("app_streamlit.py", default_timeout=300)

        # Execute o app
        at.run()

        # Simule uma entrada do usuário
        at.chat_input[0].set_value("Qual é o melhor filme de ação?").run()

        # Verifique se a resposta do assistente é a esperada
        assistant_message = at.chat_message[-1]  # A última mensagem deve ser do assistente
        assert mock_response in assistant_message.markdown[0].value 
    


    


