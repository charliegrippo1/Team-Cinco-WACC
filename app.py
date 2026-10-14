"""The WACC card.

Run from the repo root:   streamlit run app.py

Owner: the product manager. This works today on the FAKE numbers, so you can build
the page before the real numbers exist. When the developer's pull request is merged,
outputs/wacc.csv appears and the app switches to it automatically.
"""
from pathlib import Path

import pandas as pd
import streamlit as st

st.set_page_config(page_title='WACC card', layout='centered')

real = Path('outputs/wacc.csv')
is_fake = not real.exists()
card = pd.read_csv(real if real.exists() else 'outputs/wacc_FAKE.csv').iloc[0]
inputs = pd.read_csv('inputs/assumptions.csv', index_col='item')

if is_fake:
    st.warning('Illustrative only: no calculated WACC is available yet. This card is showing the FAKE example.')

st.title(f"{card['ticker']} | Cost of capital")
st.caption(f"Data through {card['asof']}")
st.markdown(
    f"Use **{card['wacc']:.2%}** as the baseline annual return hurdle for projects "
    f"with risk similar to {card['ticker']}'s existing business. Projects expected to "
    'earn more may create value; this is a benchmark, not a guarantee.'
)

c1, c2, c3, c4 = st.columns(4)
c1.metric('WACC / hurdle rate', f"{card['wacc']:.2%}")
c2.metric('Cost of equity', f"{card['cost_of_equity']:.2%}")
c3.metric('After-tax debt cost', f"{card['rd'] * (1 - card['tax']):.2%}")
c4.metric('Debt in capital mix', f"{card['w_d']:.0%}")
st.caption(
    f"Equity beta: {card['beta']:.2f} | Capital mix: "
    f"{card['w_e']:.0%} equity / {card['w_d']:.0%} debt"
)

st.subheader('Leverage scenario')
scenario_debt_weight = st.slider(
    'Debt as a share of total capital',
    min_value=0.0,
    max_value=1.0,
    value=float(card['w_d']),
    step=0.01,
    format='%.0f%%',
)
scenario_equity_weight = 1 - scenario_debt_weight
scenario_wacc = (
    scenario_equity_weight * card['cost_of_equity']
    + scenario_debt_weight * card['rd'] * (1 - card['tax'])
)
scenario_change = scenario_wacc - card['wacc']
st.metric('Scenario WACC', f'{scenario_wacc:.2%}', f'{scenario_change:+.2%} vs. current')
st.caption(
    'Illustrative: changes only the debt/equity mix. Beta, borrowing cost, tax rate, '
    'and market assumptions stay fixed; financing costs may change with leverage.'
)

st.subheader('What drives the WACC')
st.write(
    f"{card['w_e']:.0%} equity × {card['cost_of_equity']:.2%} cost of equity "
    f"+ {card['w_d']:.0%} debt × {card['rd']:.2%} debt cost × "
    f"(1 − {card['tax']:.0%} tax) = **{card['wacc']:.2%}**."
)

st.subheader('Assumptions and sources')
st.dataframe(inputs, width='stretch')

# Peer comparison is omitted until comparable company data is added to the output contract.
