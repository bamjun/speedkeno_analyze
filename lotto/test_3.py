import json
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

def prepare_data(wins_file):
    # Load the winning numbers from the JSON file
    with open(wins_file, 'r') as file:
        draws = json.load(file)

    # Prepare the dataset
    X = []  # Features: Previous draw numbers
    y = []  # Labels: Numbers in the next draw

    for i in range(len(draws) - 1):
        current_draw = draws[i]['numbers']
        next_draw = draws[i + 1]['numbers']

        # Convert numbers to a binary representation (1 if drawn, 0 otherwise)
        current_features = [1 if j in current_draw else 0 for j in range(1, 71)]
        next_features = [1 if j in next_draw else 0 for j in range(1, 71)]

        X.append(current_features)
        y.append(next_features)

    return np.array(X), np.array(y)

def train_and_predict(wins_file, top_n=10):
    X, y = prepare_data(wins_file)

    # Split the data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Initialize the random forest classifier
    clf = RandomForestClassifier(n_estimators=100, random_state=42)

    # Train the classifier
    clf.fit(X_train, y_train)

    # Predict the numbers for the next draw
    predictions = clf.predict(X_test)

    # Calculate accuracy (note: this is just for model evaluation)
    accuracy = accuracy_score(y_test, predictions)
    print(f"Model accuracy: {accuracy * 100:.2f}%")

    # Predict numbers for the next draw based on the latest draw
    last_draw = X[-1].reshape(1, -1)  # Use the latest draw as input
    next_draw_prediction = clf.predict(last_draw)

    # Find the top N predicted numbers
    predicted_indices = np.argsort(next_draw_prediction[0])[-top_n:]
    predicted_numbers = [i + 1 for i in predicted_indices]

    return sorted(predicted_numbers)

# Example usage
wins_file = 'wins.json'
predicted_numbers = train_and_predict(wins_file)

# Print the predicted top 10 numbers for the next draw
print("Predicted Top 10 Numbers for the Next Draw:", predicted_numbers)
