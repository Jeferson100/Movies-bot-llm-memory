from dotenv import load_dotenv
import os
from extracao import LinksExtractorHtml2Text
from langchain_community.tools import TavilySearchResults
import random
from aiohttp import ClientConnectorDNSError
from linkup import LinkupClient
from chat_bots import chat_limpa_resposta, chat_avaliacao


load_dotenv()


def sorteando_range_texto(texto):

    lenght_text = len(texto)

    indice_inicial = random.randint(0, lenght_text - 6000)

    indice_final = indice_inicial + 6000

    input_incor = texto[indice_inicial:indice_final]

    return input_incor


def verificar_texto(state):
    try:
        if isinstance(state, str):
            last_message = state[-1].lower()

        if isinstance(state["messages"], list):
            last_message = state["messages"][0].content.lower()

        if isinstance(state["messages"], dict):
            last_message = state["messages"][0].content.lower()
        # pylint: disable=E0606, W0707
        if last_message is None:
            raise ValueError("Mensagem não encontrada")

        return last_message
        # pylint: disable=E0606, W0707

    except AttributeError:
        if isinstance(state["messages"], list):
            last_message = state["messages"][-1]["content"].lower()

        if isinstance(state["messages"], dict):
            last_message = state["messages"][-1]["content"].lower()

        if isinstance(state, str):
            last_message = state[-1].lower()

        # pylint: disable=E0606, W0707
        if last_message is None:
            raise ValueError("Mensagem não encontrada")

        return last_message
        # pylint: disable=E0606, W0707


def search_and_incorporateta_tavily(user_input):
    # Realizando a pesquisa

    """
    Performs a search based on the user input, filters the search results,
    extracts and cleans the text from the filtered URLs, and combines the
    cleaned text with the original user input to produce a final output.

    Args:
        user_input (str): The input query from the user.

    Returns:
        str: The combined string of the original user input and the cleaned
        text extracted from the filtered search results.
    """

    search_tool = TavilySearchResults(
        max_results=5,
        search_depth="advanced",
        include_answer=True,
        include_raw_content=True,
        include_images=False,
    )

    pesquisa = search_tool.invoke({"query": user_input})

    links = []

    for numero in range(len(pesquisa)):
        try:
            links.append(pesquisa[numero]["url"])
        except TypeError:
            pass

    # Filtrando resultados para remover links do YouTube
    links_results = [
        result
        for result in links
        if "youtube.com" not in result and "https://www.disney.com.br" not in result
    ]

    # extractor = LinksExtractorFireCrawl()
    # extractor = LinksExtractor()
    extractor = LinksExtractorHtml2Text()

    texto = []

    for link in links_results:
        try:
            print(link)
            texto.append(extractor.clean_text_html2text(link, timeout=20))
        except ClientConnectorDNSError:
            pass

    if isinstance(texto, list):
        texto = "\n".join(texto)

    if len(texto) > 6000:
        texto = sorteando_range_texto(texto)

    texto_clean_final = chat_limpa_resposta(texto)

    combined_input = user_input + "\n%%%\n" + texto_clean_final

    return {"messages": [("user", combined_input)]}


def search_and_incorporateta_LinkupClient(user_input):
    # Realizando a pesquisa

    """
    Performs a search based on the user input, filters the search results,
    extracts and cleans the text from the filtered URLs, and combines the
    cleaned text with the original user input to produce a final output.

    Args:
        user_input (str): The input query from the user.

    Returns:
        str: The combined string of the original user input and the cleaned
        text extracted from the filtered search results.
    """
    client = LinkupClient(api_key=os.getenv("SEARCHAPI_API_KEY"))

    response = client.search(
        query=user_input,
        depth="standard",
        output_type="searchResults",
    )

    links = [
        response.dict()["results"][link]["url"]
        for link in range(len(response.dict()["results"]))
    ][:5]

    # Filtrando resultados para remover links do YouTube
    links_results = [
        result
        for result in links
        if "youtube.com" not in result and "https://www.disney.com.br" not in result
    ]

    # extractor = LinksExtractorFireCrawl()
    # extractor = LinksExtractor()
    extractor = LinksExtractorHtml2Text()

    texto = []

    for link in links_results:
        try:
            print(link)
            texto.append(extractor.clean_text_html2text(link, timeout=20))
        except ClientConnectorDNSError:
            pass

    if isinstance(texto, list):
        texto = "\n".join(texto)

    if len(texto) > 6000:
        texto = sorteando_range_texto(texto)

    texto_clean_final = chat_limpa_resposta(texto)

    combined_input = user_input + "\n%%%\n" + texto_clean_final

    return {"messages": [("user", combined_input)]}


def condicional_edges(state):
    """
    Processes the given state to evaluate a chat message and conditionally incorporate additional information.

    Args:
        state (dict or str): The input state containing chat messages. It can be a dictionary with a "messages" key or a string.

    Returns:
        dict: If the evaluation indicates the message is related to movies or series, returns a dictionary with the key "messages" containing
              a tuple ("user", input_incorporado) where input_incorporado is the processed and possibly truncated message.
        state: If the evaluation indicates the message is not related, returns the original state.

    The function works by extracting the last message, evaluating its relevance, and, if relevant, incorporating additional information
    through a search process that may truncate the message if it exceeds a certain length.
    """

    last_message = verificar_texto(state)

    resposta_avaliada = chat_avaliacao(last_message)

    print(resposta_avaliada)

    palavras_chave = ["yes", "sim"]

    # Condicional melhorado
    if any(
        palavra in resposta_avaliada["messages"][0][1].lower()
        for palavra in palavras_chave
    ):

        input_incorporado = search_and_incorporateta_LinkupClient(last_message)

        print(input_incorporado)

        if isinstance(input_incorporado, dict):
            input_incorporado = input_incorporado["messages"][0][1]

        if isinstance(input_incorporado, list):
            input_incorporado = input_incorporado["messages"][0][1]

        if len(input_incorporado) > 6000:

            input_incorporado = sorteando_range_texto(input_incorporado)

        return {"messages": [("user", input_incorporado)]}

    else:

        return state
