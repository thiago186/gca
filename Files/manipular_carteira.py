import interpretador_sql
import pandas as pd
import passwords
from datetime import datetime
from datetime import timedelta
import numpy as np
import database_infos
import os

date_format = '%d-%m-%Y'
caminho_carteira = os.path.dirname(os.getcwd())+'/carteiras_gca'

if not os.path.exists(caminho_carteira):
    os.mkdir(caminho_carteira)


def montar_carteira(data: datetime, cnx, table_name, save_path = caminho_carteira):
    df = interpretador_sql.get_table_as_dataframe(cnx, table_name)
    df = df.drop(['Arquivo Fonte', 'cod negociacao'], axis = 1)
    df['Data do Negócio'] = pd.to_datetime(df['Data do Negócio'], format = '%Y-%m-%d')
    df['Prazo/Vencimento'] = pd.to_datetime(df['Prazo/Vencimento'], format = '%d/%m/%Y', errors = 'coerce')
    df['PrecoXqtde'] = df['Preço']*df['Quantidade']
    #filter dates after informed date
    df = df.loc[(df['Data do Negócio'] < data) & ((df['Prazo/Vencimento'] > data) | (df['Prazo/Vencimento'].isna()))].reset_index(drop = True)
    ativos = set(df['Código de Negociação'].to_list())
    carteira = pd.DataFrame(columns = ['Ticker', 'Qtde', 'Preço Médio',])
    for ativo in ativos:
        try:
            preco_medio = sum(df.loc[(df['Código de Negociação'] == ativo) & (df['Tipo de Movimentação'] == "Compra")]['PrecoXqtde'])/sum(df.loc[(df['Código de Negociação'] == ativo) & (df['Tipo de Movimentação'] == "Compra")]['Quantidade'])
        except: 
            print(f'Não foi possível atribuir preço médio para o ativo {ativo}')
            preco_medio = np.nan
        qtde = sum(df.loc[(df['Código de Negociação'] == ativo) & (df['Tipo de Movimentação'] == "Compra")]['Quantidade']) - sum(df.loc[(df['Código de Negociação'] == ativo) & (df['Tipo de Movimentação'] == "Venda")]['Quantidade'])
        carteira.loc[-1] = [ativo, qtde, preco_medio]
        carteira = carteira.reset_index(drop = True)
        carteira = carteira.loc[ carteira['Qtde'] != 0].sort_values('Ticker').reset_index(drop = True)
    carteira.to_excel(f'{save_path}/carteira-simples-{data.strftime(date_format)}.xlsx', index = False)

def salvar_movimentacoes(data_inicial:datetime, data_final: datetime, cnx, table_name, save_path = caminho_carteira):
    if data_inicial > data_final:
        print('Data inicial informada foi maior que final. O periodo foi trocado.')
        temp = data_inicial
        data_inicial = data_final
        data_final = temp
    df = interpretador_sql.get_table_as_dataframe(cnx, table_name)
    df['Data do Negócio'] = pd.to_datetime(df['Data do Negócio'], format = '%Y-%m-%d')
    df = df.loc[(df['Data do Negócio'] < data_final) & (df['Data do Negócio'] > data_inicial)]
    df.to_excel(f'{save_path}/movimentacoes-{data_inicial.strftime(date_format)}-{data_final.strftime(date_format)}.xlsx', index = False)

def categorizar_movimentacoes(cnx):
    


if __name__ == '__main__':
    cnx = interpretador_sql.get_cnx(database_infos.database, database_infos.host)
    data = datetime(2021,8,19)       
    table_name = 'negociacoes'
    df = montar_carteira(data, cnx, table_name)