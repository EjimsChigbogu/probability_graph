import numpy as np
import matplotlib.pyplot as plt

# Initial value of the equity
initial_value = 100000

# Generate 200 random numbers in the range [0, 3]
random_numbers = np.random.randint(0, 4, size=1000)

# Map the random numbers to percentage changes
mapped_percentages = np.where(
    random_numbers == 0, 
    0,  # 0% change
    np.where(random_numbers < 3, -1, np.random.choice([4, 5], size=1000))
)

# Calculate the monetary changes based on the percentages
monetary_changes = initial_value * (mapped_percentages / 100)

# Calculate the cumulative equity curve starting from the initial value
equity_curve = initial_value + np.cumsum(monetary_changes)

# Check the range of the equity curve values
print(f"Equity curve range: {equity_curve.min()} to {equity_curve.max()}")

# Calculate the percentage gain
final_value = equity_curve[-1]
percentage_gain = ((final_value - initial_value) / initial_value) * 100

# Print percentage gain
print(f"Percentage Gain: {percentage_gain:.2f}%")

# Calculate the drawdowns
peaks = np.maximum.accumulate(equity_curve)  # Find the peak value up to each point
drawdowns = (peaks - equity_curve) / peaks * 100  # Drawdowns in percentage

# Find the highest drawdown
max_drawdown = drawdowns.max()

# Print highest drawdown
print(f"Highest Drawdown: {max_drawdown:.2f}%")

# Calculate the win rate
changes = np.diff(equity_curve)
wins = changes > 0
win_rate = np.mean(wins) * 100  # Convert to percentage

# Print win rate
print(f"Win Rate: {win_rate:.2f}%")

# Calculate the loss rate
losses = changes < 0
loss_rate = np.mean(losses) * 100  # Convert to percentage

# Print loss rate
print(f"Loss Rate: {loss_rate:.2f}%")

# Plot the equity curve
plt.plot(equity_curve)  # Removed markers, leaving only the curve line
plt.xlabel('Index')
plt.ylabel('Monetary Value ($)')
plt.title('Continuous Equity Curve')
plt.grid(True)  # Add grid lines
plt.ylim(equity_curve.min() - 1000, equity_curve.max() + 1000)  # Adjust y-axis limits for better visibility
plt.show()
