import streamlit as st
import pandas as pd
from data_fetcher import fetch_option_chain
from strategy_engine import generate_strategies
from payoff_plotter import plot_payoff

st.set_page_config(page_title="Nifty 50 Options Analyzer", layout="wide")

st.title("📈 Nifty 50 Options Strategy Analyzer")

with st.spinner("Fetching option chain data..."):
    df, spot_price, expiries = fetch_option_chain()

if df.empty:
    st.error("Failed to fetch options data.")
    st.stop()

st.success(f"Live Spot Price: ₹{spot_price}")

# Market View
outlook = st.selectbox("📊 Market Outlook", ["Neutral", "Bullish", "Bearish"])

# Filters
capital = st.slider("💰 Max Capital (₹)", 10000, 100000, 50000, step=5000)
max_loss = st.slider("❌ Max Loss Allowed (₹)", 1000, 20000, 10000, step=1000)
min_rr_ratio = st.slider("✅ Min Reward:Risk Ratio", 1.0, 3.0, 1.5, step=0.1)

# Strategy generation
strategies = generate_strategies(df, spot_price, capital, max_loss, min_rr_ratio, outlook)

if not strategies:
    st.warning("No strategies found with current filters.")
else:
    top_strats = sorted(strategies, key=lambda x: x['reward_risk'], reverse=True)[:5]

    for strat in top_strats:
        st.subheader(f"🧠 {strat['type']} - {strat['expiry']}")
        st.write(f"🔹 Legs: {strat['legs']}")
        st.write(f"💰 Max Profit: ₹{strat['max_profit']} | ❌ Max Loss: ₹{strat['max_loss']}")
        st.write(f"📍 Breakeven(s): {strat['breakevens']}")
        st.write(f"🧮 Margin Required: ₹{strat['margin']}")
        st.write(f"📈 ROI: {strat['roi']}% | 🧮 Reward:Risk = {strat['reward_risk']:.2f}")
        
        plot_payoff(strat['pnl'], strat['type'])