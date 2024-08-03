import json
from itertools import combinations
from collections import defaultdict, Counter

def find_top_combinations(wins_file, combination_size=6, top_n=1000):
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

    # Open a file to log the output
    with open('combinations_log.txt', 'w', encoding='utf-8') as log_file:
        # Output results to both the console and the log file
        if all(count == 1 for _, count in top_combinations):
            message = "Each 10-number combination appears only once."
            print(message)
            log_file.write(message + '\n')
        else:
            message = f"Top {top_n} combinations and their occurrences:"
            print(message)
            log_file.write(message + '\n')

            for rank, (combination, count) in enumerate(top_combinations, start=1):
                if count > 1:
                    message = f"Rank {rank}: Combination {combination} appears {count} times."
                    print(message)
                    log_file.write(message + '\n')

                    message = "Draws with this combination:"
                    print(message)
                    log_file.write(message + '\n')

                    for draw in draw_map[combination]:
                        message = (
                            f"Draw Date: {draw['draw_date']}, "
                            f"Draw Number: {draw['draw_number']}, "
                            f"Numbers: {draw['numbers']}, "
                            f"Sum: {draw['additional_info']}"
                        )
                        print(message)
                        log_file.write(message + '\n')

                    print()
                    log_file.write('\n')
                else:
                    message = f"Rank {rank}: Combination {combination} appears {count} time."
                    print(message)
                    log_file.write(message + '\n')

# Example usage
wins_file = 'wins.json'
find_top_combinations(wins_file)
