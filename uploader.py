import json
from sqlalchemy import create_engine, text
from datetime import datetime, timedelta

class DatabaseUploader:
    def __init__(self, df, config_path="config.json", tabla="tb_crmz_backup"):
        self.df = df
        self.config_path = config_path
        self.tabla = tabla

    def run(self):
        with open(self.config_path, "r") as config_file:
            config = json.load(config_file)

        try:
            engine = create_engine(
                f"mysql+mysqlconnector://{config['user']}:{config['password']}@{config['host']}:{config.get('port', 3306)}/{config['database']}",
                connect_args={"connect_timeout": 600},
                pool_recycle=3600,
                pool_pre_ping=True
            )
            print("✅ Conexión a MySQL establecida")
        except Exception as e:
            print(f"❌ Error al conectar con MySQL: {e}")
            return

        fecha_hace_30_dias = (datetime.today() - timedelta(days=30)).strftime('%Y-%m-%d')

        try:
            with engine.begin() as connection:
                delete_query = text(f"""
                    DELETE FROM {self.tabla}
                    WHERE fecha_de_captura >= :fecha_hace_30_dias
                """)
                connection.execute(delete_query, {"fecha_hace_30_dias": fecha_hace_30_dias})
                print(f"🧹 Datos desde {fecha_hace_30_dias} eliminados")

            self.df.to_sql(self.tabla, con=engine, if_exists='append', index=False)
            print("📥 Nuevos datos insertados exitosamente")

        except Exception as e:
            print(f"❌ Error al procesar la base de datos: {e}")
