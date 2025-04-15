def generate_strategies(df, spot_price, capital_limit, max_loss_limit, min_rr, outlook):
    strategies = []

    # Example strategy: Bull Put Spread
    for expiry in df['expiry'].unique():
        puts = df[(df['expiry'] == expiry) & (df['type'] == 'PE')]
        puts = puts.sort_values('strike')

        for i in range(len(puts)-1):
            sell = puts.iloc[i]
            buy = puts.iloc[i+1]

            if sell['strike'] < spot_price and buy['strike'] < spot_price:
                credit = sell['ltp'] - buy['ltp']
                max_loss = (buy['strike'] - sell['strike']) * 50 - credit * 50
                margin = max_loss  # simplified

                if margin < capital_limit and max_loss < max_loss_limit and credit > 0:
                    roi = (credit * 50) / margin * 100
                    rr = (credit * 50) / max_loss if max_loss != 0 else 0

                    if rr >= min_rr:
                        strategies.append({
                            'type': 'Bull Put Spread',
                            'expiry': expiry,
                            'legs': f"Sell PE {sell['strike']}, Buy PE {buy['strike']}",
                            'max_profit': round(credit * 50),
                            'max_loss': round(max_loss),
                            'margin': round(margin),
                            'breakevens': f"{sell['strike'] - credit:.2f}",
                            'roi': round(roi, 2),
                            'reward_risk': rr,
                            'pnl': {
                                'lower': buy['strike'] - 200,
                                'upper': sell['strike'] + 200,
                                'entry_credit': credit,
                                'loss': max_loss
                            }
                        })

    return strategies