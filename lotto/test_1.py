import json
from collections import Counter


def predict_frequent_numbers(wins_file, top_n=10):
    # Load the winning numbers from the JSON file
    with open(wins_file, "r") as file:
        wins = json.load(file)

    # Flatten the list of lists into a single list of all drawn numbers
    all_numbers = [number for draw in wins for number in draw["numbers"]]

    # Count the frequency of each number
    number_counts = Counter(all_numbers)

    # Get the most common numbers
    most_common_numbers = number_counts.most_common(top_n)

    # Extract only the numbers (ignoring their counts)
    predicted_numbers = [number for number, _ in most_common_numbers]

    return predicted_numbers


# Example usage
wins_file = "wins.json"
predicted_numbers = predict_frequent_numbers(wins_file)

# Print the predicted top 10 numbers
print("Predicted Top 10 Most Frequently Drawn Numbers:", predicted_numbers)
