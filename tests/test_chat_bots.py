import pytest
from chat_bots import (chat_bot, 
                       chat_summarize_messages,
                       chat_avaliacao,
                       chat_limpa_resposta)
from langchain_core.messages import AIMessage, HumanMessage
from langchain_core.chat_history import BaseChatMessageHistory
from funcoes_auxiliares import InMemoryHistory, chat_summarize_messages
from unittest.mock import patch

config = {
    "configurable": {
        "session_id": "foo"
    }
}

store = {}

def get_by_session_id(session_id: str) -> BaseChatMessageHistory:
    if session_id not in store:
        store[session_id] = InMemoryHistory()

    if store[session_id].messages:
        for mes in store[session_id].messages[-2:]:
            if isinstance(mes, HumanMessage):
                if "\n%%%\n" in mes.content:
                    store[session_id].messages[
                        store[session_id].messages.index(mes)
                    ] = HumanMessage(content=mes.content.split("\n%%%\n")[0])
            if isinstance(mes, AIMessage):
                store[session_id].messages[store[session_id].messages.index(mes)] = (
                    AIMessage(content=chat_summarize_messages(mes.content))
                )

    # Removendo as duas primeiras mensagens
    tamanho_memoria = sum([len(mes.content) for mes in store[session_id].messages])
    if tamanho_memoria > 6500:
        del store[session_id].messages[:2]
    return store[session_id]

@pytest.fixture
def setup_store():
    global store
    store = {}
    yield
    store = {}

def test_chat_bot_resposta() -> None:
    result = chat_bot("Hello",get_by_session_id, config)
    assert result is not None
    assert isinstance(result["messages"][0][1], str)
    assert len(result["messages"][0][1]) > 0
    


def test_chat_summarize_messages():
    input_message = """Você está procurando por filmes de ficção científica, certo? 
                Aqui estão algumas sugestões baseadas na lista que você me forneceu:
                I, Robot (2004) - Um policial tecnofóbico investiga um crime que pode 
                levar a um futuro distópico se n ter sido cometido por um robô, o que 
                leva a uma ameaça maior à humanidade.
                Timecrimes (2007) - Um homem viaja no tempo e precisa encontrar uma maneira 
                de voltar ao presente antes que as coisas fiquem ainda mais complicadas.
                Coherence (2013) - Um grupo de amigos experimenta estranhos eventos durante um jantar, 
                quando um cometa está passando sobre a Terra.
                Idiocracy (2006) - Um homem comum é congelado e acorda em um futuro onde a humanidade se 
                tornou extremamente estúpida.
                Infinity Pool (2023) - Um casal em uma praia de luxo descobre um subcultura perversa e 
                surreal que os leva a uma jornada de auto-descoberta.
                Esses filmes exploram temas de ficção científica, como viagens no tempo, robôs, 
                cometas e futuros distópicos. Se você quiser mais sugestões ou informações sobre esses 
                filmes, basta perguntar!"""
    
    # Use o patch para substituir chat_summarize_messages pela função mock
    with patch('chat_bots.chat_summarize_messages', return_value="Resumo de filmes de ficção científica"):
        result = chat_summarize_messages(input_message)
        assert result is not None
        assert len(result) < len(input_message)
        assert isinstance(result, str)
        
def test_chat_avaliacao_true() -> None:
    with patch('chat_bots.chat_avaliacao', return_value="Resposta positiva"):
        result = chat_avaliacao("Me fale sobre o filme I, Robot (2004)")
        assert result is not None
        assert isinstance(result['messages'][0]['content'], str)
        assert len(result['messages'][0]['content']) > 0
        assert "yes" in result['messages'][0]['content'].lower() or "sim" in result['messages'][0]['content'].lower()
    
def test_chat_avaliacao_false() -> None:
    with patch('chat_bots.chat_avaliacao', return_value="Resposta negativa"):
        result = chat_avaliacao("qual e a cor do ceu")
        assert result is not None
        assert isinstance(result['messages'][0]['content'], str)
        assert len(result['messages'][0]['content']) > 0
        assert "no" in result['messages'][0]['content'].lower() or "não" in result['messages'][0]['content'].lower()

def test_chat_limpa_resposta() -> None:
    input_message = """'AdoroCinema\nEx.: Sem Coração, Os Observadores, Dogman\n* Melhores filmes\n* Em cartaz\n* 
    Críticas AdoroCinema\n* Bilheterias\n* Todos os filmes infantis\n* Todos os filmes\n* Programação\n* Televisão\n* 
    Filmes Online\nMinha conta\nConectarCriar uma conta\nInicialComédias mais popularesMelhores filmes\n#  
    Top comédias\nMelhores filmes de todos os tempos pelos espectadores\nOs filmes mais votados por membros AdoroCinema\nMelhores 
    filmes de acordo com a imprensa Melhores filmes de acordo com\nAdoroCinema\nMelhores documentários Melhores documentários de 
    acordo com a imprensa\nMelhores filmes para crianças\n**Tipo** :  Comédia\nPor ano de produção\n* 2020 - 2029\n* 2010 - 
    2019\n* 2000 - 2009\n* 1990 - 1999\n* 1980 - 1989\n##  Forrest Gump - O Contador de Histórias\n2h 20min | Comédia, Drama, 
    Romance\nDireção: Robert Zemeckis\nElenco: Tom Hanks, Gary Sinise, Robin Wright\nTítulo original  Forrest Gump\nMeus 
    amigos\nQuarenta anos da história dos Estados Unidos, vistos pelos olhos de Forrest\nGump (Tom Hanks), 
    um rapaz com QI abaixo da média e boas intenções. Por obra\ndo acaso, ele consegue participar de momentos cruciais, 
    como a Guerra do\nVietnã e Watergate, mas continua pensando no seu amor de infância, Jenny\nAssistir em streaming\n## 
    A Vida é Bela\n1h 57min | Comédia, Comédia dramática, Drama\nDireção: Roberto Benigni\nElenco: Roberto Benigni, Horst Buchholz, 
    Marisa Paredes\nTítulo original  La vita e bella\nMeus amigos\nDurante a Segunda Guerra Mundial na Itália, o judeu Guido 
    (Roberto Benigni) e\nseu filho Giosué são levados para um campo de concentração nazista. 
    """
    with patch('chat_bots.chat_limpa_resposta', return_value="Limpar a resposta"):
        result = chat_limpa_resposta(input_message)
        assert result is not None
        assert len(result) < len(input_message)
        assert isinstance(result, str)