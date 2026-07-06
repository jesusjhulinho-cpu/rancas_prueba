import pandas as pd
import sqlite3
import os

def excel_to_sqlite():
    # Buscar archivos Excel en la carpeta
    excel_files = [f for f in os.listdir('.') if f.endswith(('.xlsx', '.xls'))]
    
    if not excel_files:
        print("❌ No hay archivos Excel en la carpeta")
        print("📁 Coloca tu archivo Excel en la carpeta del proyecto")
        return
    
    print("📁 Archivos Excel encontrados:")
    for i, f in enumerate(excel_files):
        print(f"   {i}: {f}")
    
    idx = int(input("🔢 Selecciona el número del archivo: "))
    excel_file = excel_files[idx]
    
    try:
        # Leer Excel
        df = pd.read_excel(excel_file)
        
        print(f"\n📋 Columnas encontradas en el archivo:")
        for col in df.columns:
            print(f"   - {col}")
        
        print("\n📋 Vista previa de los datos:")
        print(df.head(3))
        
        # Verificar que las columnas existen
        columnas_requeridas = ['CIE10', 'DESCRIPCION']
        for col in columnas_requeridas:
            if col not in df.columns:
                print(f"❌ Error: No se encontró la columna '{col}'")
                print(f"📋 Columnas disponibles: {df.columns.tolist()}")
                return
        
        # Limpiar datos: eliminar filas sin código o descripción
        df = df.dropna(subset=['CIE10', 'DESCRIPCION'])
        
        # Si existe la columna ESTADO, la usamos como categoría
        if 'ESTADO' in df.columns:
            print("\n✅ Columna 'ESTADO' encontrada, se usará como categoría")
        else:
            print("\n⚠️ Columna 'ESTADO' no encontrada, se usará 'General' como categoría")
        
        # Preparar datos
        datos = []
        for _, row in df.iterrows():
            codigo = str(row['CIE10']).strip()
            descripcion = str(row['DESCRIPCION']).strip()
            
            # Categoría: usar ESTADO si existe, si no, "General"
            if 'ESTADO' in df.columns and pd.notna(row['ESTADO']):
                categoria = str(row['ESTADO']).strip()
            else:
                categoria = "General"
            
            # Limpiar códigos: eliminar caracteres extraños
            codigo = codigo.replace('"', '').replace("'", "").strip()
            descripcion = descripcion.replace('"', '').replace("'", "").strip()
            
            if codigo and descripcion:
                datos.append((codigo, descripcion, categoria))
        
        print(f"\n✅ Se procesaron {len(datos)} registros válidos")
        
        if len(datos) == 0:
            print("❌ No se encontraron registros válidos para insertar")
            return
        
        # Mostrar ejemplos
        print("\n📋 Ejemplos de datos a insertar:")
        for i in range(min(5, len(datos))):
            print(f"   {datos[i][0]} - {datos[i][1][:50]}... ({datos[i][2]})")
        
        confirmar = input("\n¿Deseas continuar con la inserción? (s/n): ")
        if confirmar.lower() != 's':
            print("❌ Operación cancelada")
            return
        
        # Guardar en SQLite
        db_path = 'database/cie10.db'
        os.makedirs('database', exist_ok=True)
        
        conn = sqlite3.connect(db_path)
        c = conn.cursor()
        
        # Crear tabla
        c.execute('''
            CREATE TABLE IF NOT EXISTS cie10 (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                codigo TEXT UNIQUE NOT NULL,
                descripcion TEXT NOT NULL,
                categoria TEXT
            )
        ''')
        
        # Crear índices para búsqueda rápida
        c.execute('CREATE INDEX IF NOT EXISTS idx_codigo ON cie10(codigo)')
        c.execute('CREATE INDEX IF NOT EXISTS idx_descripcion ON cie10(descripcion)')
        
        # Eliminar datos existentes
        c.execute('DELETE FROM cie10')
        
        # Insertar datos en lotes
        batch_size = 1000
        total_insertados = 0
        
        for i in range(0, len(datos), batch_size):
            batch = datos[i:i+batch_size]
            c.executemany('INSERT OR REPLACE INTO cie10 (codigo, descripcion, categoria) VALUES (?, ?, ?)', batch)
            total_insertados += len(batch)
            print(f"   Insertados {min(i+batch_size, len(datos))} de {len(datos)}")
        
        conn.commit()
        conn.close()
        
        print(f"\n✅ ¡Éxito! {total_insertados} registros importados")
        print(f"📁 Base de datos: {db_path}")
        
        # Verificar
        conn = sqlite3.connect(db_path)
        c = conn.cursor()
        c.execute('SELECT COUNT(*) FROM cie10')
        count = c.fetchone()[0]
        conn.close()
        
        print(f"🔍 Total en base de datos: {count} registros")
        
        # Mostrar algunos ejemplos
        print("\n📋 Ejemplos de búsqueda que puedes hacer:")
        print("   - Buscar 'A00' para cólera")
        print("   - Buscar 'fiebre' para fiebres")
        print("   - Buscar 'neumonía' para neumonías")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    excel_to_sqlite()