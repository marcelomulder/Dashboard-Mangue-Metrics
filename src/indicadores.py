import pandas as pd
import numpy as np

# analise-ativo.py -------------------------------------
def calcular_medias_moveis(df, ma_periodos):
    for periodo in ma_periodos:
        df[f"MA{periodo}"] = df['Close'].rolling(window=periodo).mean()
    return df

def calcular_rsi(df, janela=14):
    delta = df['Close'].diff()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)
    roll_up = gain.rolling(window=janela).mean()
    roll_down = loss.rolling(window=janela).mean()
    rs = roll_up / roll_down
    df['RSI'] = 100 - (100 / (1 + rs))
    return df

def detectar_cruzamentos(df, ma_periodos):
    cruzamentos = []
    col_curta = f"MA{ma_periodos[0]}"
    col_longa = f"MA{ma_periodos[1]}"
    if col_curta in df.columns and col_longa in df.columns:
        for i in range(1, len(df)):
            if pd.notnull(df.iloc[i][col_curta]) and pd.notnull(df.iloc[i][col_longa]):
                if df.iloc[i-1][col_curta] < df.iloc[i-1][col_longa] and df.iloc[i][col_curta] >= df.iloc[i][col_longa]:
                    cruzamentos.append({
                        'data': df.iloc[i]['Date'],
                        'preco': df.iloc[i][col_curta],
                        'tipo': 'alta',
                        'label': 'Cruzamento Alta'
                    })
                elif df.iloc[i-1][col_curta] > df.iloc[i-1][col_longa] and df.iloc[i][col_curta] <= df.iloc[i][col_longa]:
                    cruzamentos.append({
                        'data': df.iloc[i]['Date'],
                        'preco': df.iloc[i][col_curta],
                        'tipo': 'baixa',
                        'label': 'Cruzamento Baixa'
                    })
    return cruzamentos

def gerar_alertas(df_periodo, ma_periodos, cruzamentos):
    alertas_rsi = []
    alertas_cruz = []
    if 'RSI' in df_periodo.columns and not df_periodo['RSI'].isnull().all():
        df_rsi_alerta = df_periodo.dropna(subset=['RSI'])
        for i in range(1, len(df_rsi_alerta)):
            if df_rsi_alerta['RSI'].iloc[i-1] <= 70 and df_rsi_alerta['RSI'].iloc[i] > 70:
                data_alerta = df_rsi_alerta['Date'].iloc[i]
                alertas_rsi.append(f"⚠️ Sobrecompra detectada em {data_alerta.strftime('%Y-%m-%d')}")
            if df_rsi_alerta['RSI'].iloc[i-1] >= 30 and df_rsi_alerta['RSI'].iloc[i] < 30:
                data_alerta = df_rsi_alerta['Date'].iloc[i]
                alertas_rsi.append(f"⚠️ Sobrevenda detectada em {data_alerta.strftime('%Y-%m-%d')}")
        alertas_rsi = alertas_rsi[-3:]

    for cruz in cruzamentos[-3:]:
        data_formatada = cruz['data'].strftime('%Y-%m-%d')
        if cruz['tipo'] == 'alta':
            alertas_cruz.append(f"📈 Cruzamento de alta em {data_formatada}: MA curta cruzou acima da MA longa.")
        else:
            alertas_cruz.append(f"📉 Cruzamento de baixa em {data_formatada}: MA curta cruzou abaixo da MA longa.")

    return alertas_rsi, alertas_cruz

# comparativo.py -------------------------------------

def calcular_valorizacao_percentual(df, ativos, pesos, total):
    df_pct = pd.DataFrame(index=df.index)
    for ativo in ativos:
        df_pct[ativo] = (df[ativo] / df[ativo].iloc[0] - 1) * 100
    if total == 100:
        carteira_pct = np.zeros(len(df_pct))
        for ativo in ativos:
            carteira_pct += df_pct[ativo] * (pesos[ativo] / 100)
        df_pct['Carteira'] = carteira_pct
        ativos_grafico = ativos + ['Carteira']
    else:
        ativos_grafico = ativos
    return df_pct, ativos_grafico

def calcular_valor_monetario(df, ativos, pesos, valor_inicial, total):
    df_valor = pd.DataFrame(index=df.index)
    valores_iniciais_ativos = {}
    for ativo in ativos:
        fatia = pesos[ativo] / 100
        valor_inicial_ativo = valor_inicial * fatia
        valores_iniciais_ativos[ativo] = valor_inicial_ativo
        df_valor[ativo] = (df[ativo] / df[ativo].iloc[0]) * valor_inicial_ativo
    if total == 100:
        df_valor['Carteira'] = df_valor[ativos].sum(axis=1)
    return df_valor, valores_iniciais_ativos
