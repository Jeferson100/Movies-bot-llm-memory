from langchain_community.document_loaders import AsyncHtmlLoader
from langchain_community.document_transformers.html2text import Html2TextTransformer
import concurrent.futures


class LinksExtractorHtml2Text:
    def extrair_links_html2text(self, links: str) -> str:

        loader = AsyncHtmlLoader([links])
        docs = loader.load()
        html2text = Html2TextTransformer(ignore_images=True, ignore_links=True)
        docs_transformed = html2text.transform_documents(docs)
        doc_transformed = docs_transformed[0]

        return doc_transformed.page_content

    def extrair_links_timeout(self, url: str, timeout: int = 20) -> str:
        with concurrent.futures.ThreadPoolExecutor() as executor:
            # Submete a tarefa
            future = executor.submit(self.extrair_links_html2text, url)

            try:
                # Aguarda com timeout
                resultado = future.result(timeout=timeout)
                return resultado

            except concurrent.futures.TimeoutError:
                # Cancela a tarefa se exceder o tempo limite
                future.cancel()
                return f"Extração interrompida. Tempo limite de {timeout} segundos excedido."

    def clean_text_html2text(self, url: str, timeout: int = 20) -> str:
        scrape_result = self.extrair_links_timeout(url, timeout=timeout)
        linhas = scrape_result.split("\n")

        # Remover links, linhas vazias, linhas com colchetes e linhas curtas
        linhas_limpas = [
            linha.strip()
            for linha in linhas
            if "https" not in linha and "[" not in linha and len(linha.strip()) > 10
        ]

        return "\n".join(linhas_limpas)
