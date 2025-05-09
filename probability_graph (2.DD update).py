import numpy as np
import matplotlib.pyplot as plt

# Initial value of the equity
initial_value = 100000

# Generate 50 random numbers, where 0 is selected 60% of the time
random_numbers = np.random.choice([0, 1], size=50, p=[0.60, 0.40])

# Count the occurrences of 0 and 1
count_0 = np.count_nonzero(random_numbers == 0)
count_1 = np.count_nonzero(random_numbers == 1)

# Print how many times each number was selected
print(f"Number of times 0 (-1% or -0.5%) was selected: {count_0}")
print(f"Number of times 1 (+3% or +1.5%) was selected: {count_1}")

# Map the random numbers:
# 0 is initially mapped to -1%, 1 is mapped to +3%
mapped_percentages = np.where(random_numbers == 0, -1, 3)

# Initialize variables for equity curve calculation (50 trades)
equity_curve = np.zeros(50)
equity_curve[0] = initial_value

# Loop through and calculate the equity curve with drawdown logic
for i in range(1, 50):
    # Calculate the peak (most recent high) up to this point
    peak = np.max(equity_curve[:i])

    # Calculate the drawdown
    drawdown = (peak - equity_curve[i - 1]) / peak * 100

    # Adjust the percentage mapping based on drawdown
    if drawdown >= 5:
        # If drawdown is >= 5%, adjust 0 to -0.5% and 1 to +1.5%
        if random_numbers[i] == 0:
            mapped_percentages[i] = -0.5
        elif random_numbers[i] == 1:
            mapped_percentages[i] = 1.5
    elif drawdown <= 2:
        # Reset 0 to -1% and 1 to +3% when drawdown recovers to <= -2%
        if random_numbers[i] == 0:
            mapped_percentages[i] = -1
        elif random_numbers[i] == 1:
            mapped_percentages[i] = 3

    # Calculate the monetary change based on the adjusted percentages
    monetary_change = initial_value * (mapped_percentages[i] / 100)

    # Update the equity curve
    equity_curve[i] = equity_curve[i - 1] + monetary_change

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
plt.xlabel("Index")
plt.ylabel("Monetary Value ($)")
plt.title("Continuous Equity Curve with Drawdown Logic")
plt.grid(True)  # Add grid lines
plt.ylim(
    equity_curve.min() - 100, equity_curve.max() + 100
)  # Adjust y-axis limits for better visibility
plt.show()
