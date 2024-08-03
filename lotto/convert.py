import json

def convert_text_to_json(text_file, json_file):
    # Initialize a list to store each draw as a dictionary
    draws = []

    # Open and read the text file
    with open(text_file, 'r') as file:
        for line in file:
            # Strip newline characters and split the line into parts
            line = line.strip()
            parts = line.split('\t')

            # Extract each part of the line
            draw_date = parts[0]
            draw_number = int(parts[1])
            numbers = list(map(int, parts[2].split(',')))
            additional_info = parts[3]

            # Create a dictionary for the current draw
            draw_dict = {
                "draw_date": draw_date,
                "draw_number": draw_number,
                "numbers": numbers,
                "additional_info": additional_info
            }

            # Append the dictionary to the list
            draws.append(draw_dict)

    # Write the list of draws to a JSON file
    with open(json_file, 'w') as json_file:
        json.dump(draws, json_file, indent=4)

# Example usage
text_file = 'wins.txt'
json_file = 'wins.json'
convert_text_to_json(text_file, json_file)

print(f"Conversion complete! Data saved to {json_file}.")
