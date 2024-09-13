import os
import pandas as pd
import mysql.connector
from sqlalchemy import create_engine
import chardet  # Fayl kodlashini aniqlash uchun

# Fayl kodlashini aniqlash
def fayl_kodlashini_aniqlash(file_path):
    with open(file_path, 'rb') as f:
        rawdata = f.read(10000)
    result = chardet.detect(rawdata)
    return result['encoding']

# MySQLga ulanish uchun sozlamalar
def mysql_ulanis(db_host, db_user, db_password, db_name):
    try:
        # SQLAlchemy motorini yaratish
        engine = create_engine(f"mysql+mysqlconnector://{db_user}:{db_password}@{db_host}/{db_name}")
        return engine
    except Exception as e:
        print(f"MySQL ulanishida xatolik: {e}")
        return None

# Faqat .csv fayllarni o'qish va MySQL ga kiritish
def csvdan_mysqlga(folder_path, engine):
    try:
        fayllar = os.listdir(folder_path)
        # Faqat .csv fayllarni tanlab olish
        csv_fayllar = [fayl for fayl in fayllar if fayl.endswith('.csv')]
        
        for fayl in csv_fayllar:
            try:
                file_path = os.path.join(folder_path, fayl)
                table_name = os.path.splitext(fayl)[0]
                
                # Fayl kodlashini aniqlash
                encoding = fayl_kodlashini_aniqlash(file_path)
                print(f"'{fayl}' faylining kodlash formati: {encoding}")
                
                # CSV faylni Pandas yordamida o'qish
                df = pd.read_csv(file_path, encoding=encoding)
                
                # Jadvalni MySQL ga yozish
                df.to_sql(name=table_name, con=engine, if_exists='replace', index=False)
                print(f"Fayl '{fayl}' jadvalga '{table_name}' nomi bilan saqlandi.")
            
            except Exception as e:
                print(f"'{fayl}' faylida xatolik yuz berdi: {e}")
                continue  # Xatolik yuz berganda bu faylni o'tkazib yuboradi
    except Exception as e:
        print(f"Xatolik: {e}")

# Foydalanish
if __name__ == "__main__":
    folder_path = '/home/uznetdev/Desktop/project/AdventureWorks Dashboard/sql-server-samples-master/samples/databases/adventure-works/data-warehouse-install-script'
    
    # MySQL ulanish sozlamalari
    db_host = 'localhost'
    db_user = 'project'
    db_password = 'myproject'
    db_name = 'adventure-works'
    
    # MySQL bilan ulanish
    engine = mysql_ulanis(db_host, db_user, db_password, db_name)
    
    if engine:
        csvdan_mysqlga(folder_path, engine)
