import matplotlib.pyplot as plt


def plot_age_comparison(df):
    # Separate wins and losses
    wins = df[df["result"] == "W"]
    losses = df[df["result"] == "L"]

    # Create the figure
    fig, ax = plt.subplots(figsize=(12, 7))

    # Plot wins in blue
    ax.scatter(wins["player_age"], wins["age_diff"],
               s=18, color="#31B7E9", alpha=0.85,
               label="Match won")

    # Plot losses in red
    ax.scatter(losses["player_age"], losses["age_diff"],
               s=18, color="#E82C8A", alpha=0.85,
               label="Match lost")

    return fig


def _style_plot(ax):
    # Horizontal line where players are the same age
    ax.axhline(0, color="gray", linewidth=1)

    # Axis labels
    ax.set_xlabel("Player's age")
    ax.set_ylabel("Player age - Opponent age")

    # Add grid and remove borders
    ax.grid(True, color="#d9d9d9", linewidth=0.8)
    ax.set_axisbelow(True)

    for spine in ax.spines.values():
        spine.set_visible(False)

    # Add legend
    ax.legend()

    return ax