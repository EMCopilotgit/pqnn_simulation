# Install Plotly
!pip install plotly

import numpy as np
import plotly.graph_objects as go

# Simulation parameters
np.random.seed(42)
grid_size = 30       # 30x30 reshuffling manifold
time_steps = 50      # Number of animation frames

# Initialize quantum state amplitudes randomly
amplitudes = np.random.rand(grid_size, grid_size)

# Define reshuffling potential function R(ψ)
def reshuffling_potential(psi):
    laplacian = (
        -4 * psi +
        np.roll(psi, 1, axis=0) + np.roll(psi, -1, axis=0) +
        np.roll(psi, 1, axis=1) + np.roll(psi, -1, axis=1)
    )
    rarity_boost = np.exp(-psi * 5)
    return psi + 0.1 * laplacian * rarity_boost

# Store frames for animation
frames = []
for t in range(time_steps):
    amplitudes = reshuffling_potential(amplitudes)
    amplitudes = np.clip(amplitudes, 0, 1)

    frame = go.Frame(
        data=[go.Surface(z=amplitudes, colorscale='Viridis')],
        name=str(t)
    )
    frames.append(frame)

# Create initial surface plot
fig = go.Figure(
    data=[go.Surface(z=amplitudes, colorscale='Viridis')],
    layout=go.Layout(
        title="Quantum Amplitude Reshuffling Simulation",
        scene=dict(
            xaxis_title='X',
            yaxis_title='Y',
            zaxis_title='Amplitude',
            xaxis=dict(showgrid=True, gridcolor='lightgray'),
            yaxis=dict(showgrid=True, gridcolor='lightgray'),
            zaxis=dict(showgrid=True, gridcolor='lightgray')
        ),
        updatemenus=[dict(
            type="buttons",
            showactive=False,
            buttons=[dict(label="Play", method="animate", args=[None])]
        )],
        sliders=[dict(
            steps=[dict(method='animate',
                        args=[[f.name], dict(frame=dict(duration=50, redraw=True), transition=dict(duration=0))],
                        label=f.name) for f in frames],
            transition=dict(duration=0),
            x=0.1,
            len=0.9
        )]
    ),
    frames=frames
)

# Save animation to HTML
fig.write_html("quantum_amplitude_reshuffling_simulation.html")