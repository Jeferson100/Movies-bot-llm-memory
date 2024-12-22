# Movies Bot LLM Memory

![Movies Bot](https://raw.githubusercontent.com/Jeferson100/Movies-bot-llm-memory/refs/heads/main/image/imagem_modificada.webp)



[![Aplicativo Streamlit](https://img.shields.io/badge/APP_STREAMLIT-whit?style=flat&logo=streamlit)](https://bot-movies.streamlit.app/)
[![Testes](https://github.com/Jeferson100/Movies-bot-llm-memory/actions/workflows/testes.yml/badge.svg)](https://github.com/Jeferson100/Movies-bot-llm-memory/actions/workflows/testes.yml)


Este repositório contém um bot de filmes baseado em modelos de linguagem (LLMs) para oferecer recomendações, informações e interações dinâmicas sobre filmes. O bot também é capaz de resumir mensagens, avaliar respostas e processar informações de forma eficiente.

## 🌟 Funcionalidades

- **Recomendações Personalizadas**: Sugere filmes com base em preferências do usuário.
- **Extração de Dados**: Capacidade de buscar informações relacionadas a filmes diretamente da web.
- **Interface Intuitiva**: Implementado com Streamlit para interações fáceis e rápidas.
- **Memória**: Armazena e recupera conversas para ter uma experiencia mais interessante.

## 🚀 Tecnologias Usadas

<p align="center">
  <img src="https://img.shields.io/badge/python-black?style=flat&logo=python" alt="Python" />
  <img src="https://img.shields.io/badge/langchain-black?style=flat&logo=langchain" alt="Langchain" />
  <img src="https://img.shields.io/badge/streamlit-black?style=flat&logo=streamlit" alt="Streamlit" />
  <img src="https://img.shields.io/badge/groq-black?style=flat&logo=groq" alt="Groq" />
  <img src="https://img.shields.io/badge/tavily-black?style=flat&logo=tavily" alt="Tavily" />
</p>

- **Python**: Uma linguagem de programação poderosa, usada para desenvolver o bot e suas funcionalidades.
- **Langchain**: Uma biblioteca para construir cadeias de processamento de linguagem natural, usada para criar e gerenciar os modelos de linguagem do bot.
- **Streamlit**: Uma biblioteca para criar aplicativos web interativos e intuitivos diretamente a partir de scripts Python.
- **Groq**: Uma plataforma de hardware e software para acelerar o processamento de modelos de inteligência artificial, usada para melhorar o desempenho do bot.
- **Tavily**: Uma biblioteca para extração de dados estruturados de páginas da web, usada para obter informações relevantes de forma eficiente.


## Estrutura do Repositório

O repositorio contém as seguintes pastas:

**chat_bots**

- A pasta [chat_bots](https://github.com/Jeferson100/Movies-bot-llm-memory/tree/main/chat_bots) contém quatro arquivos mais importante. A primeira é [chat_avaliacao](https://github.com/Jeferson100/Movies-bot-llm-memory/blob/main/chat_bots/chat_avaliacao.py) que avalia se a pegunta do usuario é sobre filmes ou não, o segundo [chat_limpa_resposta](https://github.com/Jeferson100/Movies-bot-llm-memory/blob/main/chat_bots/chat_limpa_resposta.py) que limpa as informações obtidas da internet, a terceiras é [chat_summarize](https://github.com/Jeferson100/Movies-bot-llm-memory/blob/main/chat_bots/chat_summarize.py) que faz o resumo das respostas para guardar na memoria menos informacoes e por ultimo o [chat_bot](https://github.com/Jeferson100/Movies-bot-llm-memory/blob/main/chat_bots/chat_bot.py) que é o chat que responde ao usuario.

**Extracao**

A pasta [extracao](https://github.com/Jeferson100/Movies-bot-llm-memory/tree/main/extracao) é dedicada à raspagem de dados da internet, utilizando diferentes tecnologias para extrair textos e informações de páginas web. Ela contém os seguintes arquivos:

- **`extracao_textos_links_crawl4ai`**: Implementa a raspagem de dados utilizando a tecnologia Crawl4AI.
- **`extracao_textos_links_firacrawl`**: Utiliza a ferramenta FireCrawl para extrair informações de páginas web.
- **`extracao_textos_links_html2text`**: Realiza a conversão de páginas HTML em texto puro para facilitar o processamento.

Cada arquivo é responsável por uma abordagem específica, garantindo flexibilidade e eficiência na obtenção de dados. 


**Funcoes_auxiliares** 

A pasta [funcoes_auxiliares](https://github.com/Jeferson100/Movies-bot-llm-memory/tree/main/funcoes_auxiliares) contém funções auxiliares utilizadas pelo bot. Contem dois arquivos, [memory](https://github.com/Jeferson100/Movies-bot-llm-memory/blob/main/funcoes_auxiliares/memory.py) com contem a classe para introducao da memoria e o arquivo [funcoes_auxiliares](https://github.com/Jeferson100/Movies-bot-llm-memory/blob/main/funcoes_auxiliares/funcoes_auxiliares.py) onde se encontra a função **condicional_edges** que verifica se o bot deve usar a web para responder a pergunta do usuario.


**app_streamlit**

O arquivo [app_streamlit](https://github.com/Jeferson100/Movies-bot-llm-memory/blob/main/app_streamlit.py) contém o código principal do aplicativo desenvolvido em Streamlit. Ele é responsável por implementar a interface do usuário e integrar as funcionalidades do bot de filmes, permitindo interações diretas com os usuários de forma intuitiva e dinâmica. 


## Uso

### Variáveis de Ambiente

Certifique-se de definir as seguintes variáveis de ambiente para que o bot funcione corretamente:

- `GROQ_API_KEY`
- `FIRECRAWL_API_KEY`
- `SEARCHAPI_API_KEY`
- `TAVILY_API_KEY`

Crie um arquivo `.env` na raiz do repositório e defina as variáveis de ambiente conforme necessário.

### Instalação

Para instalar as dependências do projeto, execute os seguintes etapas:

- Primeiro utilize a biblioteca **UV** para repositorio de dependencias

```bash
pip install uv
```

- Após crie um abiente virtual

```
uv venv
```

- Instale as dependências do projeto, executando o comando:

```sh
uv pip install -r requirements.txt
```

Para executar o bot, utilize o seguinte comando:

```sh
streamlit run app_streamlit.py
```


## Configuração de CI/CD

O repositório utiliza GitHub Actions para CI/CD. O workflow está definido em `.github/workflows/testes.yml` e inclui etapas para copiar os arquivos do repositório, instalar dependências, verificar formatação, lint, testes e tipagem dos arquivos.


## Contribuição

Contribuições são bem-vindas! Sinta-se à vontade para abrir issues e pull requests.

## Licença

Este projeto está licenciado sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.