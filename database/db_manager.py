import sqlite3
import os
from typing import List, Dict, Optional

class DatabaseManager:
    def __init__(self):
        self.db_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'database')
        self.db_path = os.path.join(self.db_dir, 'cie10.db')
        os.makedirs(self.db_dir, exist_ok=True)
        self._init_database()
    
    def _init_database(self):
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS cie10 (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    codigo TEXT UNIQUE NOT NULL,
                    descripcion TEXT NOT NULL,
                    categoria TEXT
                )
            ''')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_codigo ON cie10(codigo)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_descripcion ON cie10(descripcion)')
            conn.commit()
            conn.close()
            self._insert_sample_data_if_empty()
        except sqlite3.Error as e:
            print(f"Error: {e}")
    
    def _insert_sample_data_if_empty(self):
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM cie10")
            count = cursor.fetchone()[0]
            
            if count == 0:
                sample_data = [
                    ('A00.0', 'Cólera debida a Vibrio cholerae 01', 'Infecciosas'),
                    ('A00.1', 'Cólera debida a Vibrio cholerae 01, biotipo el tor', 'Infecciosas'),
                    ('A00.9', 'Cólera no especificada', 'Infecciosas'),
                    ('A01.0', 'Fiebre tifoidea', 'Infecciosas'),
                    ('A01.1', 'Fiebre paratifoidea A', 'Infecciosas'),
                    ('A01.2', 'Fiebre paratifoidea B', 'Infecciosas'),
                    ('A01.3', 'Fiebre paratifoidea C', 'Infecciosas'),
                    ('A01.4', 'Fiebre paratifoidea no especificada', 'Infecciosas'),
                    ('A02.0', 'Salmonelosis', 'Infecciosas'),
                    ('A02.1', 'Septicemia por Salmonella', 'Infecciosas'),
                    ('A03.0', 'Shigelosis debida a Shigella dysenteriae', 'Infecciosas'),
                    ('A03.1', 'Shigelosis debida a Shigella flexneri', 'Infecciosas'),
                    ('A03.2', 'Shigelosis debida a Shigella boydii', 'Infecciosas'),
                    ('A03.3', 'Shigelosis debida a Shigella sonnei', 'Infecciosas'),
                    ('A03.9', 'Shigelosis no especificada', 'Infecciosas'),
                    ('A04.0', 'Infección por E. coli enteropatógena', 'Infecciosas'),
                    ('A04.1', 'Infección por E. coli enterotoxigénica', 'Infecciosas'),
                    ('A04.2', 'Infección por E. coli enteroinvasiva', 'Infecciosas'),
                    ('A04.3', 'Infección por E. coli enterohemorrágica', 'Infecciosas'),
                    ('A04.4', 'Infección por E. coli no especificada', 'Infecciosas'),
                    ('A04.5', 'Enteritis por Campylobacter', 'Infecciosas'),
                    ('A04.6', 'Enteritis por Yersinia enterocolitica', 'Infecciosas'),
                    ('A04.7', 'Enterocolitis por Clostridium difficile', 'Infecciosas'),
                    ('A04.8', 'Otras infecciones intestinales', 'Infecciosas'),
                    ('A04.9', 'Infección intestinal no especificada', 'Infecciosas'),
                    ('A05.0', 'Intoxicación alimentaria por estafilococos', 'Infecciosas'),
                    ('A05.1', 'Botulismo', 'Infecciosas'),
                    ('A05.2', 'Intoxicación por Clostridium perfringens', 'Infecciosas'),
                    ('A05.3', 'Intoxicación por Vibrio parahaemolyticus', 'Infecciosas'),
                    ('A05.4', 'Intoxicación por Bacillus cereus', 'Infecciosas'),
                ]
                cursor.executemany('INSERT OR REPLACE INTO cie10 (codigo, descripcion, categoria) VALUES (?, ?, ?)', sample_data)
                conn.commit()
                print(f"✅ Insertados {len(sample_data)} registros")
            conn.close()
        except sqlite3.Error as e:
            print(f"Error: {e}")
    
    def search_cie10(self, query: str) -> List[Dict[str, str]]:
        if not query or len(query.strip()) < 2:
            return []
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            search_pattern = f"%{query.strip()}%"
            cursor.execute('''
                SELECT codigo, descripcion FROM cie10 
                WHERE codigo LIKE ? OR descripcion LIKE ? 
                ORDER BY codigo ASC LIMIT 100
            ''', (search_pattern, search_pattern))
            results = [{"codigo": row[0], "descripcion": row[1]} for row in cursor.fetchall()]
            conn.close()
            return results
        except sqlite3.Error as e:
            print(f"Error: {e}")
            return []