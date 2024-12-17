from firecrawl import FirecrawlApp


from dotenv import load_dotenv
import os

load_dotenv()

app = FirecrawlApp(api_key=os.getenv("FIRECRAWL_API_KEY"))


class LinksExtractorFireCrawl:
    def extrair_links_firecrawl(self, url: str) -> str:
        # Scrape a website:
        scrape_result = app.scrape_url(url, params={"formats": ["markdown"]})
        return scrape_result

    def clean_text_firecrawl(self, url: str) -> list[str]:
        # Extract the markdown content
        scrape_result = self.extrair_links_firecrawl(url)

        # Remove the links
        text_without_links = [
            line
            for line in scrape_result["markdown"].split("\n")
            if "https" not in line
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
