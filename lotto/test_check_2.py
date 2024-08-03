import json
from itertools import combinations
from collections import defaultdict, Counter

def find_top_combinations(wins_file, combination_size=10, top_n=10):
    # Load the winning numbers from the JSON file
    with open(wins_file, 'r') as file:
        draws = json.load(file)

    # Create a dictionary to count occurrences of each combination
    combination_counts = defaultdict(int)
    draw_map = defaultdict(list)

    # Iterate through each draw and generate combinations
    for draw in draws:
        numbers = draw['numbers']
        
        # Generate all possible combinations of the specified size
        for combo in combinations(sorted(numbers), combination_size):
            combination_counts[combo] += 1
            draw_map[combo].append(draw)

    # Get the most common combinations
    top_combinations = Counter(combination_counts).most_common(top_n)

    # Output results
    if all(count == 1 for _, count in top_combinations):
        print("Each 10-number combination appears only once.")
    else:
        print(f"Top {top_n} combinations and their occurrences:")

        for rank, (combination, count) in enumerate(top_combinations, start=1):
            if count > 1:
                print(f"Rank {rank}: Combination {combination} appears {count} times.")
                print("Draws with this combination:")
                for draw in draw_map[combination]:
                    print(f"Draw Date: {draw['draw_date']}, Draw Number: {draw['draw_number']}, Numbers: {draw['numbers']}, Sum: {draw['additional_info']}")
                print()
            else:
                print(f"Rank {rank}: Combination {combination} appears {count} time.")

# Example usage
wins_file = 'wins.json'
find_top_combinations(wins_file)
