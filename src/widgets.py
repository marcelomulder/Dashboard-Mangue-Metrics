import streamlit as st

# analise-ativo.py -------------------------------------
# Adiciona o heatmap de criptomoedas
def tradingview_heatmap(title="🌐 Heatmap de Criptomoedas - TradingView", height=650, color_theme="dark"):
    st.markdown(f"## {title}")
    st.components.v1.html(f"""
    <!-- TradingView Widget BEGIN -->
    <div class="tradingview-widget-container" style="height:{height}px;">
      <div class="tradingview-widget-container__widget"></div>
      <div class="tradingview-widget-copyright">
        <a href="https://www.tradingview.com/" rel="noopener nofollow" target="_blank">          
        </a>
      </div>
      <script type="text/javascript" src="https://s3.tradingview.com/external-embedding/embed-widget-crypto-coins-heatmap.js" async>
      {{
      "dataSource": "Crypto",
      "blockSize": "market_cap_calc",
      "blockColor": "24h_close_change|5",
      "locale": "en",
      "symbolUrl": "",
      "colorTheme": "{color_theme}",
      "hasTopBar": false,
      "isDataSetEnabled": false,
      "isZoomEnabled": true,
      "hasSymbolTooltip": true,
      "isMonoSize": false,
      "width": "100%",
      "height": "{height}"
      }}
      </script>
    </div>
    <!-- TradingView Widget END -->
    """, height=height )

# Insere a fita de ativos no dashboard
def tradingview_ticker_tape(title=None, height=100, color_theme="dark"):
    if title:
        st.markdown(f"## {title}")
    st.components.v1.html(f"""
    <!-- TradingView Widget BEGIN -->
    <div class="tradingview-widget-container" style="height:{height}px;">
      <div class="tradingview-widget-container__widget"></div>
      <div class="tradingview-widget-copyright">
        <a href="https://www.tradingview.com/" rel="noopener nofollow" target="_blank">          
        </a>
      </div>
      <script type="text/javascript" src="https://s3.tradingview.com/external-embedding/embed-widget-ticker-tape.js" async>
      {{
      "symbols": [
        {{"proName": "FOREXCOM:SPXUSD", "title": "S&P 500 Index"}},
        {{"proName": "BITSTAMP:BTCUSD", "title": "Bitcoin"}},
        {{"proName": "BITSTAMP:ETHUSD", "title": "Ethereum"}},
        {{"description": "Ripple", "proName": "BITSTAMP:XRPUSD"}},
        {{"description": "Solana", "proName": "BITSTAMP:SOLUSD"}},
        {{"description": "Gold ETF", "proName": "AMEX:IAU"}},
        {{"description": "Brazil ETF", "proName": "AMEX:EWZ"}},
        {{"description": "S&P ETF", "proName": "AMEX:SPY"}}
      ],
      "showSymbolLogo": true,
      "isTransparent": false,
      "displayMode": "adaptive",
      "colorTheme": "{color_theme}",
      "locale": "en"
      }}
      </script>
    </div>
    <!-- TradingView Widget END -->
    """, height=height-50)

import streamlit as st

def tradingview_technical_analysis(symbol="BITSTAMP:BTCUSD", interval="1D", width=425, height=450, color_theme="dark"):
    st.components.v1.html(f"""
    <!-- TradingView Widget BEGIN -->
    <div style="display: flex; justify-content: center;">
      <div class="tradingview-widget-container" style="width:100%">
        <div class="tradingview-widget-container__widget"></div>
        <div class="tradingview-widget-copyright">
          <a href="https://br.tradingview.com/" rel="noopener nofollow" target="_blank">
            <span class="blue-text">Monitore todos os mercados no TradingView</span>
          </a>
        </div>
        <script type="text/javascript" src="https://s3.tradingview.com/external-embedding/embed-widget-technical-analysis.js" async>
        {{
          "interval": "{interval}",
          "width": "{width}",
          "isTransparent": false,
          "height": "{height}",
          "symbol": "{symbol}",
          "showIntervalTabs": true,
          "displayMode": "single",
          "locale": "br",
          "colorTheme": "{color_theme}"
        }}
        </script>
      </div>
    </div>
    <!-- TradingView Widget END -->
    """, height=height - 15)


