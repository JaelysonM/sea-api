import asyncio
from pyppeteer import launch
from jinja2 import Environment, FileSystemLoader
from src.siasdapi.domain.ports.services.pdf import (
    PDFGeneratorService,
)
from src.siasdapi.domain.shared.documents import (
    Document,
)


class JinjaPDFGenerator(PDFGeneratorService):
    def __init__(self):
        self.env = Environment(
            loader=FileSystemLoader("assets/documents")
        )

    async def generate(self, document: Document) -> bytes:
        template = self.env.get_template(document.template)
        rendered_html = template.render(document.data)

        try:
            browser = await launch(
                headless=True,
                handleSIGINT=False,
                handleSIGTERM=False,
                handleSIGHUP=False,
                args=[
                    "--no-sandbox",
                    "--disable-dev-shm-usage",
                    "--disable-gpu",
                    "--disable-software-rasterizer",
                    "--disable-setuid-sandbox",
                ],
            )
            page = await browser.newPage()

            await page.setContent(rendered_html)
            await asyncio.sleep(1)
            pdf_bytes = await page.pdf(
                {"format": "A4", "printBackground": True}
            )
            await browser.close()
            return pdf_bytes
        except Exception as e:  # pragma: no cover
            print(
                "An error occurred while generating PDF file "
                + str(e)
            )
            return None
