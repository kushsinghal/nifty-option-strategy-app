import matplotlib.pyplot as plt
import streamlit as st
import numpy as np

def plot_payoff(pnl_data, strategy_name):
    x = np.linspace(pnl_data['lower'], pnl_data['upper'], 100)
    y = []

    for price in x:
        if price <= pnl_data['lower']:
            y.append(-pnl_data['loss'])
        elif price >= pnl_data['upper']:
            y.append(pnl_data['entry_credit'] * 50)
        else:
            # Linear approximation
            slope = (pnl_data['entry_credit'] * 50 + pnl_data['loss']) / (pnl_data['upper'] - pnl_data['lower'])
            y_val = slope * (price - pnl_data['lower']) - pnl_data['loss']
            y.append(y_val)

    fig, ax = plt.subplots()
    ax.plot(x, y, label='P/L')
    ax.axhline(0, color='gray', linestyle='--')
    ax.set_xlabel("Spot Price at Expiry")
    ax.set_ylabel("Profit / Loss (₹)")
    ax.set_title(f"Payoff: {strategy_name}")
    ax.grid(True)
    st.pyplot(fig)