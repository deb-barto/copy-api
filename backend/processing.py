from collections import defaultdict
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
        mrr_data = calculate_mrr_from_df(df)   
        return df.to_dict(orient='records')
    except Exception as e:
        print(e)
        return []  

def calculate_mrr_from_df(df):
    mrr_data = defaultdict(lambda: {"MRR": 0, "Novos_MRR": 0, "Churn_MRR": 0})
    
    df['data início'] = pd.to_datetime(df['data início'], dayfirst=True)
    df['data cancelamento'] = pd.to_datetime(df['data cancelamento'], dayfirst=True, errors='coerce')
    
    grouped = df.groupby('ID assinante')
    
    for name, group in grouped:
        group = group.sort_values(by='data início')
        for i, row in group.iterrows():
            mes_ano = row['data início'].strftime("%Y-%m")
            if pd.isnull(row['data cancelamento']):
                mrr_data[mes_ano]["MRR"] += row['valor']
                if i == group.first_valid_index():  
                    mrr_data[mes_ano]["Novos_MRR"] += row['valor']
            else:
                mes_ano_cancelamento = row['data cancelamento'].strftime("%Y-%m")
                mrr_data[mes_ano_cancelamento]["Churn_MRR"] += row['valor']
                
    return dict(mrr_data)
