"""
Module for generating statistics and plots based on motion data.
"""
import json
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

def generate_statistics(json_file="motion_data.json", output_file="motion_statistics.png"):
    """
    Reads motion log data, calculates statistics, and generates a bar chart.

    Args:
        json_file (str): Path to the JSON log file.
        output_file (str): Path to save the generated graph.
        
    Returns:
        dict: A dictionary containing calculated statistics.
    """
    file_path = Path(json_file)

    # 1. Handle missing file
    if not file_path.exists():
        print(f"Error: Log file '{json_file}' does not exist.")
        return None

    # 2. Read and parse the JSON file safely
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except json.JSONDecodeError:
        print(f"Error: Log file '{json_file}' contains invalid JSON.")
        return None
    except OSError as e:
        print(f"Error reading file '{json_file}': {e}")
        return None

    # 3. Handle empty data or data that is not a list
    if not isinstance(data, list) or len(data) == 0:
        print("Notice: No motion events found in the log file.")
        return None
        
    # 4. Load JSON data into a Pandas DataFrame
    # A DataFrame is a 2D table, similar to an Excel spreadsheet, which makes analysis easy
    df = pd.DataFrame(data)

    # 5. Handle cases where the DataFrame is missing expected columns
    if 'date' not in df.columns or 'number_of_objects' not in df.columns:
        print("Error: JSON data does not contain expected event records.")
        return None

    # 6. Perform basic data analysis (Aggregation)
    total_events = len(df)
    total_objects = df['number_of_objects'].sum()

    # Group the events by the 'date' column and count how many events happened on each date
    # 'size()' counts the number of rows in each group
    events_per_date = df.groupby('date').size()

    # 7. Generate a simple bar chart using Matplotlib
    # Create a new figure with a specific size (width, height)
    plt.figure(figsize=(10, 6))

    # Plot a bar chart: X-axis = dates, Y-axis = number of events
    events_per_date.plot(kind='bar', color='skyblue', edgecolor='black')

    # Add labels and a title to make the graph clear
    plt.title('Number of Motion Events per Date', fontsize=14)
    plt.xlabel('Date', fontsize=12)
    plt.ylabel('Number of Motion Events', fontsize=12)

    # Rotate the x-axis labels (dates) slightly so they don't overlap
    plt.xticks(rotation=45, ha='right')

    # Add a grid to make it easier to read values
    plt.grid(axis='y', linestyle='--', alpha=0.7)

    # Automatically adjust layout so labels aren't cut off
    plt.tight_layout()

    # 8. Save the graph to a file and close it (no pop-ups)
    plt.savefig(output_file)
    plt.close()

    # 9. Return the calculated statistics
    stats = {
        "total_events": total_events,
        "total_objects": int(total_objects),
        "events_per_date": events_per_date.to_dict()
    }
    return stats

if __name__ == "__main__":
    # Test the function directly when this file is run
    stats = generate_statistics()
    
    if stats:
        print("\nMotion Statistics")
        print("-----------------")
        print(f"Total Motion Events : {stats['total_events']}")
        print(f"Total Objects       : {stats['total_objects']}")
        print(f"Graph saved to      : motion_statistics.png\n")

