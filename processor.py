import pandas as pd


class CSVProcessor:
    def __init__(self, carpeta_csv):
        self.carpeta_csv = carpeta_csv
        self.df = None

    def run(self):
        columnas_deseadas = [
            "CREDITO", "GESTION", "TELEFONO", "CODIGO RESULTADO", "CC", "CALIFICACION",
            "TIPO PROMESA", "MONTO", "FECHA PROMESA", "CUMPLIDO", "CODIGO ACCION",
            "NOMBRE FIRMA", "NOMBRE PRODUCTO", "NOMBRE GESTOR", "SUPERVISOR NOMBRE",
            "GERENTE NOMBRE", "FECHA DE CAPTURA", "GER AZTECA", "ESTA ACTIVO EN SISTEMA",
            "DIQUE", "SUCURSAL NOMBRE", "SEMANA AZTECA", "CONFIRMADO EN SCL", "ASIGNADA A"
        ]

        dfs = []
        for ruta in self.carpeta_csv:
            df = pd.read_csv(ruta, delimiter='|', low_memory=False)
            df = df[columnas_deseadas]
            df.columns = (
                df.columns
                .str.strip()
                .str.lower()
                .str.replace(' ', '_')
                .str.replace('á', 'a')
                .str.replace('é', 'e')
            )
            for col in ['fecha_promesa', 'fecha_de_captura']:
                df[col] = pd.to_datetime(df[col], errors='coerce').dt.strftime('%Y-%m-%d')
            df['telefono'] = df['telefono'].astype(str).str.replace('.0', '', regex=False)
            dfs.append(df)

        self.df = pd.concat(dfs, ignore_index=True)

        # Eliminar duplicados según los campos clave
        campos_clave = [
            'fecha_de_captura', 'fecha_promesa', 'monto',
            'credito', 'nombre_gestor', 'semana_azteca', 'confirmado_en_scl'
        ]
        antes = len(self.df)
        self.df = self.df.drop_duplicates(subset=campos_clave)
        despues = len(self.df)

        print(f"🧼 CSVs combinados. {antes - despues} duplicados eliminados")
        return self.df
