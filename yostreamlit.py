import pandas as pd
from cadCAD.configuration.utils import config_sim
from model.genesis_states import generate_initial_state
from model.partial_state_update_block import generate_partial_state_update_blocks
from model.sim_runner import *
from model.parts.utils import post_processing
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import streamlit as st

# Configuring user input
spot_price_reference_input = st.sidebar.selectbox(
    'Select spot price reference',
    ['DAI', 'WETH']
)

decoding_type_input = st.sidebar.selectbox(
    'Select decoding type',
    ['CONTRACT_CALL']
)

parameters = {
    'spot_price_reference': [spot_price_reference_input],
    'decoding_type': [decoding_type_input]
}

# Initial values
initial_values = generate_initial_state(initial_values_json='data/0x8b6e6e7b5b3801fed2cafd4b22b8a16c2f2db21a-initial_pool_states-prices.json', spot_price_base_currency=parameters['spot_price_reference'][0])

# Generate partial state update blocks
result = generate_partial_state_update_blocks('data/0x8b6e6e7b5b3801fed2cafd4b22b8a16c2f2db21a-actions-prices.json')
partial_state_update_blocks = result['partial_state_update_blocks']

# Configuration
steps_number = result['steps_number']
sim_config = config_sim(
    {
        'N': 1,  # number of monte carlo runs
        'T': range(steps_number - 1),  # number of timesteps
        'M': parameters,  # simulation parameters
    }
)

# Execution
df = run(initial_values, partial_state_update_blocks, sim_config)

# Post processing
p_df = post_processing(df, include_spot_prices=False)

# Print DataFrame columns
st.write(p_df)

# Create a plot
fig = go.Figure()
fig.add_trace(go.Scatter(x=p_df["change_datetime"], y=p_df["tvl"], mode='lines', name='TVL'))
fig.update_layout(title='TVL over Time',
                   xaxis_title='Time',
                   yaxis_title='TVL')

st.plotly_chart(fig)