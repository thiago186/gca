import pandas as pd
from datetime import datetime
import os
currpath = os.getcwd()
#biblioteca para ler extratos da b3

def ler_extrato_mov(file_path): #insere caminho de arquivo de extrato, retorna dataframe com as transações
    df = pd.read_excel(file_path, engine = 'openpyxl')
    df['Data_Importacao'] = datetime.today()
    df["Tipo_Lancamento"] = 'Não Identificado'
    df = df.replace("-",0.00)
    for i, lancamento in enumerate(df['Entrada/Saída']):
        if df.loc[i, "Movimentação"] in ["Empréstimo", "Transferência", "Transferência - Liquidação"] and lancamento == "Debito" and df.loc[i, "Valor da Operação"] == 0.00:
            df.loc[i, "Tipo_Lancamento"] = "Entrega Emprestimo"
        elif df.loc[i, "Movimentação"] in ["Empréstimo", "Transferência", "Transferência - Liquidação"] and lancamento == "Credito" and df.loc[i, "Valor da Operação"] == 0.00:
            df.loc[i, "Tipo_Lancamento"] = "Devolucao Emprestimo"   
        elif df.loc[i, "Movimentação"] == "Empréstimo" and df.loc[i, "Entrada/Saída"] == "Credito":
            df.loc[i, "Tipo_Lancamento"] = "Receita Emprestimo"   
        elif df.loc[i, "Movimentação"] == "Empréstimo" and df.loc[i, "Valor da Operação"] >0:
            df.loc[i, "Tipo_Lancamento"] = "Receita Emprestimo"                
        elif df.loc[i, "Movimentação"] == "Transferência - Liquidação" and lancamento == "Credito":
            df.loc[i, "Tipo_Lancamento"] = "Compra"
        elif df.loc[i, "Movimentação"] == "Transferência - Liquidação" and lancamento == "Debito":
            df.loc[i, "Tipo_Lancamento"] = "Venda"          
        elif df.loc[i,"Movimentação"] == "Dividendo":
            df.loc[i, "Tipo_Lancamento"] = "Dividendo"          
        elif df.loc[i,"Movimentação"] == "Juros Sobre Capital Próprio":
            df.loc[i, "Tipo_Lancamento"] = "JCP"
        elif df.loc[i,"Movimentação"] == "Rendimento":
            df.loc[i, "Tipo_Lancamento"] = "Rendimento"
        elif df.loc[i,"Movimentação"] == "Bonificação em Ativos":
            df.loc[i, "Tipo_Lancamento"] = "Bonific. Ativos"

def ler_negociacoes(file_path):
    cabecalho = ['Data do Negócio', 'Tipo de Movimentação', 'Mercado', 'Prazo/Vencimento', 'Instituição', 'Código de Negociação', 'Quantidade', 'Preço', 'Valor']
    extensoes = ['.xlsx', '.xls']
    if os.path.splitext(file_path)[-1] not in extensoes:
        print(f' O arquivo inserido deve possuir uma das seguintes extensões: {extensoes}')
        return
    else:
        try:
            df = pd.read_excel(file_path)
        except:
            print(f'Não foi possível ler arquivo{os.path.basename(file_path)}')
            return
        if list(df.columns) != cabecalho:
            print(f'O arquivo não está no padrão da B3 para negociacoes')
            return
        else:
            df['Data do Negócio'] = pd.to_datetime(df['Data do Negócio'])
            # Apply the operation to every element in the 'column_name' column
            df['Código de Negociação'] = df['Código de Negociação'].apply(lambda x: x[:-1] if x[-1] == "F" else x)
            df['Arquivo Fonte'] = os.path.basename(file_path)
            df['cod_negociacao'] = df.apply(lambda x: ''.join(x.astype(str)), axis=1)
    return df
