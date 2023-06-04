import pandas as pd
from cadCAD.configuration.utils import config_sim
from model.genesis_states import generate_initial_state
from model.partial_state_update_block import generate_partial_state_update_blocks
from model.sim_runner import *
from model.parts.utils import post_processing
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

parameters = {
    'spot_price_reference': ['DAI'],
    'decoding_type': ['CONTRACT_CALL']
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

print(p_df)

# # Plotting
# fig = make_subplots(rows=2, cols=1, shared_xaxes=True, vertical_spacing=0.02)

# # Assuming "time" and "spot_price" columns in your dataframe
# fig.add_trace(
#     go.Scatter(x=p_df["time"], y=p_df["spot_price"], mode='lines', name='Spot Price'),
#     row=1, col=1
# )

# # Assuming "time" and "volume" columns in your dataframe
# fig.add_trace(
#     go.Scatter(x=p_df["time"], y=p_df["volume"], mode='lines', name='Volume'),
#     row=2, col=1
# )

# fig.update_layout(height=600, width=800, title_text="Simulation Results")
# fig.show()
