import asyncio
from crawl4ai import AsyncWebCrawler


class LinksExtractor:
    async def extract_links(self, url: str) -> str:
        """
        Extracts the markdown content from the given URL.

        Args:
            url (str): The URL to extract the content from.

        Returns:
            str: The extracted markdown content.
        """
        async with AsyncWebCrawler(verbose=True) as crawler:
            result = await crawler.arun(url=url)
            return result.markdown  # type: ignore

    def clean_text(self, url: str) -> str:
        """
        Extracts and cleans the text from the given URL.

        Args:
            url (str): The URL to extract the text from.

        Returns:
            list[str]: The cleaned text, with each line as an item in the list.
        """
        # Extract the markdown content

        markdown = asyncio.run(self.extract_links(url))
        # markdown = await self.extract_links(url)

        # Remove the links
        text_without_links = [
            line for line in markdown.split("\n") if "https" not in line
        ]

        # Remove leading/trailing whitespace

        cleaned_text = [line.strip() for line in text_without_links if line.strip()]

        if isinstance(cleaned_text, list):
            cleaned_text = "\n".join(cleaned_text)

        texto_sem_colchetes = [
            linha for linha in cleaned_text.split("\n") if "[" not in str(linha)
        ]

        if isinstance(texto_sem_colchetes, list):
            texto_sem_colchetes = "\n".join(texto_sem_colchetes)

        retirando_linhas_com_menos_10_caracteres = [
            linha for linha in texto_sem_colchetes.split("\n") if len(linha) > 10
        ]

        if isinstance(retirando_linhas_com_menos_10_caracteres, list):
            retirando_linhas_com_menos_10_caracteres = "\n".join(
                retirando_linhas_com_menos_10_caracteres
            )

        return retirando_linhas_com_menos_10_caracteres
