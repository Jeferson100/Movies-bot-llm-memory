def test_importacoes_extracao():
    from extracao import (
        LinksExtractor,
        LinksExtractorFireCrawl,
        LinksExtractorHtml2Text,
    )

    assert LinksExtractorHtml2Text
    assert LinksExtractorFireCrawl
    assert LinksExtractor


def test_importacoes_chat_bots():
    from chat_bots import (
        chat_bot,
        chat_avaliacao,
        chat_limpa_resposta,
        chat_summarize_messages,
    )

    assert chat_bot
    assert chat_avaliacao
    assert chat_limpa_resposta
    assert chat_summarize_messages


def test_importacoes_funcoes_auxiliares():
    from funcoes_auxiliares import (
        condicional_edges,
        sorteando_range_texto,
        search_and_incorporateta_LinkupClient,
        InMemoryHistory,
    )

    assert condicional_edges
    assert sorteando_range_texto
    assert search_and_incorporateta_LinkupClient
    assert InMemoryHistory
