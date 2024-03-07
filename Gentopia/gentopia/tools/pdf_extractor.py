from typing import AnyStr
import requests
from bs4 import BeautifulSoup
from gentopia.tools.basetool import *
from PyPDF2 import PdfReader

class PDFExtractorArgs(BaseModel):
    url: str = Field(..., description="a web url to visit. You must make sure that the url is real and correct.")


class PDFExtractor(BaseTool):
    """Tool that adds the capability to query the Google search API."""

    name = "pdf_extractor"
    description = "A tool to retrieve web pages through url. Useful when you have a url and need to find detailed information inside."

    args_schema: Optional[Type[BaseModel]] = PDFExtractorArgs

    def _run(self, url: AnyStr) -> str:
        try:
            response = requests.get(url)
            response.raise_for_status()

            with open('downloaded.pdf','wb') as f:
                for chunk in response.iter_content(1024):
                    f.write(chunk)
            reader = PdfReader('downloaded.pdf')

            text = ""
            for page in reader.pages:
                text += page.extract_text()

            print("Hello from PDFExtractor")

            return text
        except Exception as e:
            return f"Error: {e}\n Probably it is an invalid URL."

    async def _arun(self, *args: Any, **kwargs: Any) -> Any:
        raise NotImplementedError


if __name__ == "__main__":
    ans = PDFExtractor("https://arxiv.org/pdf/1810.04805.pdf")
    print(ans)
