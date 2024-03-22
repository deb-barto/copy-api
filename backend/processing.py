import pandas as pd
from .models import Upload

def read_xlsx(file_path):
    df = pd.read_excel(file_path)
    data_list = df.to_dict(orient='records')
    
    return data_list

def get_processed_data():
    try:
        last_upload = Upload.objects.order_by('-uploaded_at').first()
        if not last_upload:
            return [] 
        file_path = last_upload.file.path
        df = pd.read_excel(file_path)
        
        return df.to_dict(orient='records')
    except Exception as e:
        print(e)
        return []  