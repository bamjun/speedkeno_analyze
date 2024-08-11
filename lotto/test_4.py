import json

import numpy as np
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split


def prepare_data(wins_file):
    # Load the winning numbers from the JSON file
    with open(wins_file, "r") as file:
        draws = json.load(file)

    # Prepare the dataset
    X = []  # Features: Previous draw numbers and additional patterns
    y = []  # Labels: Numbers in the next draw

    for i in range(len(draws) - 1):
        current_draw = draws[i]["numbers"]
        next_draw = draws[i + 1]["numbers"]

        # Create features from the current draw
        current_features = [1 if j in current_draw else 0 for j in range(1, 71)]

        # Feature engineering: add patterns and sequential dependencies
        # 1. Count of consecutive numbers
        consecutive_count = sum(
            [
                1
                for k in range(len(current_draw) - 1)
                if current_draw[k] + 1 == current_draw[k + 1]
            ]
        )
        current_features.append(consecutive_count)

        # 2. Count of numbers in specific ranges
        range1 = sum([1 for num in current_draw if 1 <= num <= 20])
        range2 = sum([1 for num in current_draw if 21 <= num <= 40])
        range3 = sum([1 for num in current_draw if 41 <= num <= 60])
        range4 = sum([1 for num in current_draw if 61 <= num <= 70])
        current_features.extend([range1, range2, range3, range4])

        X.append(current_features)

        # Convert next draw numbers to binary representation
        next_features = [1 if j in next_draw else 0 for j in range(1, 71)]
        y.append(next_features)

    return np.array(X), np.array(y)


def train_and_predict(wins_file, top_n=10):
    X, y = prepare_data(wins_file)

    # Initialize an empty list to store predictions for each number
    predicted_numbers = []

    # Train a separate model for each number (1-70)
    for number_index in range(70):
        # Extract the target column for the current number
        y_current = y[:, number_index]

        # Split the data into training and testing sets
        X_train, X_test, y_train, y_test = train_test_split(
            X, y_current, test_size=0.2, random_state=42
        )

        # Initialize the Gradient Boosting Classifier
        clf = GradientBoostingClassifier(n_estimators=100, random_state=42)

        # Train the classifier
        clf.fit(X_train, y_train)

        # Predict the numbers for the test set
        predictions = clf.predict(X_test)

        # Calculate accuracy (note: this is just for model evaluation)
        accuracy = accuracy_score(y_test, predictions)
        print(f"Model accuracy for number {number_index + 1}: {accuracy * 100:.2f}%")

        # Predict the probability for the next draw based on the latest draw
        last_draw = X[-1].reshape(1, -1)  # Use the latest draw as input
        probability = clf.predict_proba(last_draw)[
            0, 1
        ]  # Probability of number being drawn

        predicted_numbers.append((number_index + 1, probability))

    # Sort numbers by predicted probability
    predicted_numbers.sort(key=lambda x: x[1], reverse=True)

    # Extract the top N numbers with the highest probabilities
    top_predicted_numbers = [num for num, prob in predicted_numbers[:top_n]]

    return sorted(top_predicted_numbers)


# Example usage
wins_file = "wins.json"
predicted_numbers = train_and_predict(wins_file)

# Print the predicted top 10 numbers for the next draw
print("Predicted Top 10 Numbers for the Next Draw:", predicted_numbers)
