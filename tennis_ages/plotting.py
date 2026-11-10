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