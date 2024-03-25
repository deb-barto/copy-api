from collections import defaultdict
import pandas as pd
from .models import Upload
from datetime import datetime


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
        df['data início'] = pd.to_datetime(df['data início'], dayfirst=True)
        df = df.sort_values(by='data início')
        mrr_data = calculate_mrr_from_df(df)   
        return df.to_dict(orient='records')
    except Exception as e:
        print(e)
        return []  

def calculate_mrr_from_df(df):
    mrr_data = defaultdict(lambda: {"MRR": 0, "Novos_MRR": 0, "Churn_MRR": 0})

    # Assegura que todas as datas estão no formato correto para comparação
    df['data início'] = pd.to_datetime(df['data início'])
    df['data status'] = pd.to_datetime(df['data status'])
    df['data cancelamento'] = pd.to_datetime(df['data cancelamento'])
    df['próximo ciclo'] = pd.to_datetime(df['próximo ciclo'])

    data_final = pd.Timestamp(datetime.today())

    for date in pd.date_range(start=df['data início'].min(), end=data_final, freq='MS'):
        mes_ano = date.strftime("%Y-%m")

        for _, row in df.iterrows():
            data_inicio = row['data início'].to_pydatetime().date()
            
            # Considera o valor para o Novos_MRR se a data de início está dentro do mês atual do loop
            if data_inicio.year == date.year and data_inicio.month == date.month:
                mrr_data[mes_ano]['Novos_MRR'] += row['valor']
                mrr_data[mes_ano]['MRR'] += row['valor']

            # Para assinaturas que começam antes do mês e não foram canceladas até o fim do mês
            elif data_inicio <= date.to_pydatetime().date():
                if pd.isnull(row['data cancelamento']) or row['data cancelamento'].to_pydatetime().date() > date.to_pydatetime().date():
                    mrr_data[mes_ano]['MRR'] += row['valor']

            # Calcula o Churn_MRR para assinaturas canceladas dentro do mês
            if pd.notnull(row['data cancelamento']) and row['data cancelamento'].to_pydatetime().date().year == date.year and row['data cancelamento'].to_pydatetime().date().month == date.month:
                mrr_data[mes_ano]['Churn_MRR'] += row['valor']
                mrr_data[mes_ano]['MRR'] -= row['valor']
        
        # Arredonda os valores para duas casas decimais
        mrr_data[mes_ano]['MRR'] = round(mrr_data[mes_ano]['MRR'], 2)
        mrr_data[mes_ano]['Novos_MRR'] = round(mrr_data[mes_ano]['Novos_MRR'], 2)
        mrr_data[mes_ano]['Churn_MRR'] = round(mrr_data[mes_ano]['Churn_MRR'], 2)

    # Filtro para remover meses futuros sem atividade MRR
    mrr_data = {k: v for k, v in mrr_data.items() if pd.to_datetime(k) <= data_final and (v['MRR'] != 0 or v['Novos_MRR'] != 0 or v['Churn_MRR'] != 0)}

    return dict(mrr_data)