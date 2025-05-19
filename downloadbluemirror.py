import os
from playwright.sync_api import Playwright, sync_playwright

class ReportDownloaderALG:
    def __init__(self, desde, hasta):
        self.desde = desde
        self.hasta = hasta
        self.ruta_csv = None

    def run(self):
        def download(playwright: Playwright):
            # Especificar la ruta donde quieres guardar el archivo descargado
            download_path = r"Z:\CRMhorahora\Blue"
            os.makedirs(download_path, exist_ok=True)  # Crear la carpeta si no existe

            # Lanzar Chromium y controlar la descarga
            browser = playwright.chromium.launch(headless=False)
            context = browser.new_context(accept_downloads=True)
            page = context.new_page()

            # Navegar a la página y realizar el login
            page.goto("https://aglv3.net//login")
            page.get_by_role("textbox", name="Enter Email Address...").fill("SP023")
            page.wait_for_timeout(3000)
            page.get_by_role("textbox", name="Password").fill("oscarSP023")
            page.wait_for_timeout(3000)
            page.get_by_role("button", name="Iniciar").click()
            page.wait_for_timeout(3000)

            # Ingresar a la página de descargas y llenar los parámetros
            page.get_by_role("link", name="Descargar Reportes").click()
            page.wait_for_timeout(3000)
            page.get_by_role("textbox", name="Desde").fill(self.desde)
            page.wait_for_timeout(3000)
            page.get_by_role("textbox", name="Hasta").fill(self.hasta)
            page.wait_for_timeout(3000)
            page.get_by_role("textbox", name="Hasta").press("Tab")
            page.wait_for_timeout(3000)
            page.locator("#selectFirma").press("Enter")
            page.wait_for_timeout(3000)
            page.locator("#selectFirma").press("B")
            page.wait_for_timeout(3000)
            page.locator("#selectFirma").press("B")
            page.wait_for_timeout(1000)
            page.locator("#selectFirma").press("B")
            page.wait_for_timeout(1000)
            page.locator("#selectFirma").press("Tab")
            page.wait_for_timeout(3000)
            page.locator("#selectFirma").press("Tab")
            page.wait_for_timeout(3000)
            page.locator("#selectProducto").press("Enter")
            page.wait_for_timeout(3000)
            page.locator("#selectProducto").press("Tab")
            page.wait_for_timeout(3000)
            page.locator("select[name=\"tipo_reporte\"]").press("Enter")
            page.wait_for_timeout(3000)
            page.locator("select[name=\"tipo_reporte\"]").press("Tab")
            page.wait_for_timeout(3000)

            # Esperar la descarga y guardarla en la ruta específica
            with page.expect_download() as download_info:
                page.get_by_role("button", name="Generar").click()

            download = download_info.value
            download_path_final = os.path.join(download_path, download.suggested_filename)
            download.save_as(download_path_final)

            context.close()
            browser.close()

            # Regresar la ruta completa donde se guardó el archivo
            return download_path_final

        # Ejecutar la descarga usando Playwright
        with sync_playwright() as playwright:
            self.ruta_csv = download(playwright)

        print(f"✅ Archivo descargado: {self.ruta_csv}")
        return self.ruta_csv
