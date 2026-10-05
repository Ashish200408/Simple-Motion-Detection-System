"""
Module for logging motion detection events.
"""
import json
import datetime
from pathlib import Path

class MotionLogger:
    def __init__(self, file_path="motion_data.json"):
        """
        Initialize the MotionLogger.
        
        Args:
            file_path (str): The path to the JSON file where events will be stored.
        """
        self.file_path = Path(file_path)
        # Ensure the file exists and has valid initial data
        self._ensure_file_exists()

    def _ensure_file_exists(self):
        """
        Check if the JSON file exists. If it does not, create it with an empty list.
        """
        if not self.file_path.exists():
            self._write_empty_list()

    def _write_empty_list(self):
        """
        Write an empty JSON array to the file.
        """
        try:
            with open(self.file_path, 'w', encoding='utf-8') as f:
                json.dump([], f)
        except OSError as e:
            print(f"Error creating JSON file: {e}")

    def log_motion(self, timestamp, motion_status, num_objects):
        """
        Log a motion event to the JSON file.

        Args:
            timestamp (datetime.datetime): The datetime object of when the event occurred.
            motion_status (str): The status (e.g., "MOTION DETECTED" or "NO MOTION").
            num_objects (int): The number of objects detected.
        """
        # Ensure timestamp is a datetime object to format it correctly
        if not isinstance(timestamp, datetime.datetime):
            try:
                # Attempt to parse if it's an ISO string
                timestamp = datetime.datetime.fromisoformat(str(timestamp))
            except ValueError:
                # Fallback to current time if parsing fails
                timestamp = datetime.datetime.now()
                
        date_str = timestamp.strftime("%d-%m-%Y")
        time_str = timestamp.strftime("%H:%M:%S")
        timestamp_iso = timestamp.isoformat()

        # Construct the event dictionary
        event = {
            "date": date_str,
            "time": time_str,
            "timestamp": timestamp_iso,
            "motion_status": motion_status,
            "number_of_objects": num_objects
        }

        # Read existing events, append the new one, and save back to the file
        events = self.get_events()
        events.append(event)
        
        try:
            with open(self.file_path, 'w', encoding='utf-8') as f:
                # Add indentation for readability
                json.dump(events, f, indent=4)
        except OSError as e:
            print(f"Error writing to JSON file: {e}")

    def get_events(self):
        """
        Read and return all stored motion events.

        Returns:
            list: A list of motion event dictionaries.
        """
        try:
            with open(self.file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                # Verify that the data is indeed a list. 
                # If it's a dict or something else due to corruption, treat it as empty.
                if isinstance(data, list):
                    return data
                else:
                    print("Warning: JSON data is not a list. Resetting file.")
                    self._write_empty_list()
                    return []
        
        # Handle cases where the file doesn't exist unexpectedly
        except FileNotFoundError:
            print("Warning: JSON file not found. Creating a new one.")
            self._write_empty_list()
            return []
            
        # Handle cases where the file is corrupted or empty
        except json.JSONDecodeError:
            print("Warning: JSON file is corrupted or empty. Recovering by resetting.")
            self._write_empty_list()
            return []
            
        # Handle permissions or other OS-level errors
        except OSError as e:
            print(f"Error reading JSON file: {e}")
            return []

    def clear_events(self):
        """
        Clear all logged motion events and reset the JSON file to [].
        """
        self._write_empty_list()

