import json


def find_draw_with_numbers(wins_file, target_numbers):
    # Load the winning numbers from the JSON file
    with open(wins_file, "r") as file:
        draws = json.load(file)

    # Sort the target numbers for easy comparison
    target_numbers = sorted(target_numbers)

    # Iterate through each draw to find a match
    matching_draws = []
    for draw in draws:
        # Sort the numbers in the current draw
        draw_numbers = sorted(draw["numbers"])

        # Check if the target numbers are a subset of the draw numbers
        if all(number in draw_numbers for number in target_numbers):
            matching_draws.append(draw)

    return matching_draws


# Example usage
wins_file = "wins.json"
# target_numbers = [1, 12, 23, 34, 56, 57, 67, 59, 69, 70]
target_numbers = [56, 57, 67, 59, 69, 70]

# Find draws containing the target numbers
matching_draws = find_draw_with_numbers(wins_file, target_numbers)

# Print the results
if matching_draws:
    print("Draws containing the target numbers:")
    for draw in matching_draws:
        print(
            f"Draw Date: {draw['draw_date']}, Draw Number: {draw['draw_number']}, Numbers: {draw['numbers']}, Sum: {draw['additional_info']}"
        )
else:
    print("No draws contain the target numbers.")
