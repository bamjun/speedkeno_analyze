use serde::Deserialize;
use serde_json::Value;
use std::collections::HashMap;
use itertools::Itertools;
use std::fs::File;
use std::io::{self, BufReader, Write};

#[derive(Debug, Deserialize)]
struct Draw {
    draw_date: String,
    draw_number: u32,
    numbers: Vec<u32>,
    additional_info: Option<Value>, // Additional info can be any JSON value
}

fn find_top_combinations(wins_file: &str, combination_size: usize, top_n: usize) -> io::Result<()> {
    // Read and parse the JSON file into a vector of Draw structs
    let file = File::open(wins_file)?;
    let reader = BufReader::new(file);
    let draws: Vec<Draw> = serde_json::from_reader(reader)?;

    // Create hashmaps to store combination counts and draw maps
    let mut combination_counts: HashMap<Vec<u32>, u32> = HashMap::new();
    let mut draw_map: HashMap<Vec<u32>, Vec<&Draw>> = HashMap::new();

    // Iterate over each draw and generate combinations
    for draw in &draws {
        // Sort the numbers to ensure consistent combination ordering
        let sorted_numbers = draw.numbers.iter().sorted();

        // Generate all possible combinations of the specified size
        for combo in sorted_numbers.combinations(combination_size) {
            let combo_vec = combo.into_iter().cloned().collect::<Vec<u32>>();

            // Increment the combination count and map the draw to the combination
            *combination_counts.entry(combo_vec.clone()).or_insert(0) += 1;
            draw_map.entry(combo_vec).or_insert_with(Vec::new).push(draw);
        }
    }

    // Sort combinations by occurrence count in descending order
    let mut top_combinations: Vec<_> = combination_counts.iter().collect();
    top_combinations.sort_by(|a, b| b.1.cmp(a.1));
    top_combinations.truncate(top_n);

    // Open a log file to write the results
    let mut log_file = File::create("combinations_log.txt")?;

    // Check if all combinations appear only once
    if top_combinations.iter().all(|&(_, &count)| count == 1) {
        let message = "각 10개 번호 조합은 한 번씩만 나타납니다.";
        println!("{}", message);
        writeln!(log_file, "{}", message)?;
    } else {
        let message = format!("상위 {}개의 조합과 그 발생 횟수:", top_n);
        println!("{}", message);
        writeln!(log_file, "{}", message)?;

        // Iterate over each top combination and print details
        for (rank, (combination, &count)) in top_combinations.iter().enumerate() {
            if count > 1 {
                let message = format!(
                    "순위 {}: 조합 {:?}이(가) {}번 나타났습니다.",
                    rank + 1,
                    combination,
                    count
                );
                println!("{}", message);
                writeln!(log_file, "{}", message)?;

                let message = "이 조합을 포함하는 추첨들:";
                println!("{}", message);
                writeln!(log_file, "{}", message)?;

                // Access draws associated with the combination using slices
                if let Some(draws) = draw_map.get(combination.as_slice()) {
                    for draw in draws {
                        let message = format!(
                            "추첨 날짜: {}, 추첨 번호: {}, 숫자들: {:?}, 추가 정보: {:?}",
                            draw.draw_date, draw.draw_number, draw.numbers, draw.additional_info
                        );
                        println!("{}", message);
                        writeln!(log_file, "{}", message)?;
                    }
                }

                println!();
                writeln!(log_file)?;
            } else {
                let message = format!(
                    "순위 {}: 조합 {:?}이(가) {}번 나타났습니다.",
                    rank + 1,
                    combination,
                    count
                );
                println!("{}", message);
                writeln!(log_file, "{}", message)?;
            }
        }
    }

    Ok(())
}

fn main() -> io::Result<()> {
    let wins_file = "wins.json";
    find_top_combinations(wins_file, 10, 1000)
}
