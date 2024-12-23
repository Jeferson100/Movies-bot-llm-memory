from dotenv import load_dotenv
from extracao import LinksExtractorHtml2Text
from langchain_community.tools import TavilySearchResults
import random
from aiohttp import ClientConnectorDNSError
from linkup import LinkupClient
from chat_bots import chat_limpa_resposta, chat_avaliacao, get_secret_key


load_dotenv()

try:
    api_secret_groq = get_secret_key("GROQ_API_KEY")
except KeyError:
    raise ValueError("API key GROQ inválida ou não definida")

try:
    api_secret_tavily = get_secret_key("TAVILY_API_KEY")
except KeyError:
    raise ValueError("API key TAVILY inválida ou não definida")

try:
    api_secret_firecrawl = get_secret_key("FIRECRAWL_API_KEY")
except KeyError:
    raise ValueError("API key FIRECRAWL inválida ou não definida")

try:
    api_secret_searchapi = get_secret_key("SEARCHAPI_API_KEY")
except KeyError:
    raise ValueError("API key SEARCHAPI inválida ou não definida")


def sorteando_range_texto(texto):

    lenght_text = len(texto)

    indice_inicial = random.randint(0, lenght_text - 6000)

    indice_final = indice_inicial + 6000

    input_incor = texto[indice_inicial:indice_final]

    return input_incor


def search_and_incorporateta_tavily(user_input: str, api_groq: str = api_secret_groq):
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
        include_domains=[
            "https://www.adorocinema.com/",
            "https://www.rottentomatoes.com/",
            "https://cinepop.com.br/",
        ],
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
            texto.append(extractor.clean_text_html2text(link))
        except ClientConnectorDNSError:
            pass

    if isinstance(texto, list):
        texto = "\n".join(texto)

    if len(texto) > 6000:
        texto = sorteando_range_texto(texto)

    texto_clean_final = chat_limpa_resposta(texto, api_groq)

    combined_input = user_input + "\n%%%\n" + texto_clean_final

    return {"messages": [("user", combined_input)]}


def search_and_incorporateta_LinkupClient(
    user_input,
    api_searchapi: str = api_secret_searchapi,
    api_groq: str = api_secret_groq,
):
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
    client = LinkupClient(api_key=api_searchapi)

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
            texto.append(extractor.clean_text_html2text(link))
        except ClientConnectorDNSError:
            pass

    if isinstance(texto, list):
        texto = "\n".join(texto)

    if len(texto) > 6000:
        texto = sorteando_range_texto(texto)

    texto_clean_final = chat_limpa_resposta(texto, api_groq)

    combined_input = user_input + "\n%%%\n" + texto_clean_final

    return {"messages": [{"content": combined_input}]}


def condicional_edges(
    state, api_groq: str = api_secret_groq, api_searchapi: str = api_secret_searchapi
):
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

    if isinstance(state, dict):
        state = state["messages"][0]["content"]

    resposta_avaliada = chat_avaliacao(state, api_groq)

    print(resposta_avaliada)

    palavras_chave = ["yes", "sim"]

    # Condicional melhorado
    if any(
        palavra in resposta_avaliada["messages"][0]["content"].lower()
        for palavra in palavras_chave
    ):

        input_incorporado = search_and_incorporateta_LinkupClient(state, api_searchapi)

        print(input_incorporado)

        if isinstance(input_incorporado, dict):
            input_incorporado = input_incorporado["messages"][0]["content"]  # type: ignore

        if len(input_incorporado) > 6000:

            input_incorporado = sorteando_range_texto(input_incorporado)

        return {"messages": [{"content": input_incorporado}]}

    else:

        return state
