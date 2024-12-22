from langchain_community.document_loaders import AsyncHtmlLoader
from langchain_community.document_transformers.html2text import Html2TextTransformer


class LinksExtractorHtml2Text:
    def extrair_links_html2text(self, links: str) -> str:

        loader = AsyncHtmlLoader([links])
        docs = loader.load()
        html2text = Html2TextTransformer(ignore_images=True, ignore_links=True)
        docs_transformed = html2text.transform_documents(docs)
        doc_transformed = docs_transformed[0]

        return doc_transformed.page_content

    def clean_text_html2text(self, url: str) -> str:
        scrape_result = self.extrair_links_html2text(url)
        linhas = scrape_result.split("\n")

        # Remover links, linhas vazias, linhas com colchetes e linhas curtas
        linhas_limpas = [
            linha.strip()
            for linha in linhas
            if "https" not in linha and "[" not in linha and len(linha.strip()) > 10
        ]

        return "\n".join(linhas_limpas)
