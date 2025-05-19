from downloader import ReportDownloader
from processor import CSVProcessor
from uploader import DatabaseUploader
# from file_mover import FileMover
from downloadbluemirror import ReportDownloaderALG
import time
from datetime import datetime, timedelta
import calendar
import sys

#nomas la cuenta regresiva
def cuenta_regresiva(segundos):
    for i in range(segundos, 0, -1):
        mins, secs = divmod(i, 60)
        tiempo = f"{mins:02d}:{secs:02d}"
        sys.stdout.write(f"\rCerrando en {tiempo}...")
        sys.stdout.flush()
        time.sleep(1)
    print("\n Script finalizado. Cerrando...")

if __name__ == "__main__":
    hoy = datetime.today()
    desde = (hoy - timedelta(days=30)).strftime('%Y-%m-%d')

    ultimo_dia_mes = calendar.monthrange(hoy.year, hoy.month)[1]
    hasta = datetime(hoy.year, hoy.month, ultimo_dia_mes).strftime('%Y-%m-%d')

    print(f"Desde: {desde}")
    print(f"Hasta: {hasta}")

    #Paso 1
    downloader1 = ReportDownloader(desde, hasta)
    ruta_csv1 = downloader1.run()
    time.sleep(3)
    downloader2 = ReportDownloaderALG(desde, hasta)
    ruta_csv2 = downloader2.run()
    time.sleep(3)

    if not ruta_csv1 or not ruta_csv2:
        print("No se pudieron descargar ambos reportes. Abortando...")
        sys.exit(1)
    
    #Paso 2
    processor = CSVProcessor([ruta_csv1, ruta_csv2])
    df = processor.run()

    #paso 3
    uploader = DatabaseUploader(df)
    uploader.run()

    print("\nPuedes revisar los resultados. Cerrando en 2 minutos...\n")
    cuenta_regresiva(120)

