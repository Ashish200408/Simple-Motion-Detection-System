"""
Main entry point for the Simple Motion Detection System.
"""
import cv2
import datetime
from motion_detector import MotionDetector
from motion_logger import MotionLogger
from statistics import generate_statistics

def main():
    # 1. Initialize the video capture (webcam)
    # The '0' usually refers to the built-in webcam on most computers.
    cap = cv2.VideoCapture(0)

    # 2. Check if the camera opened successfully
    if not cap.isOpened():
        print("Error: Could not open the webcam. Please check if it's connected and not in use by another application.")
        return

    # 3. Initialize our custom modules
    detector = MotionDetector()
    logger = MotionLogger("motion_data.json")

    # State variables for event logging to prevent spamming the JSON file
    # We only want to log when motion starts, not every single frame it continues
    previous_motion_state = False
    # Initialize last_logged_time far in the past to ensure the first event always logs
    last_logged_time = datetime.datetime.min 

    print("Starting the Simple Motion Detection System...")
    print("Press 'q' or 'Q' in the video window to quit.")

    # 4. Use try/finally to guarantee that resources are released even if an error occurs
    try:
        # Continuously read frames from the webcam
        while True:
            # Read a single frame from the camera
            # 'ret' is a boolean that is True if a frame was grabbed successfully
            ret, frame = cap.read()
            
            if not ret:
                print("Error: Failed to grab frame from camera.")
                break

            # 5. Process the frame using our MotionDetector
            # This returns a frame with drawn bounding boxes, and motion statistics
            processed_frame, motion_detected, num_objects, bounding_boxes = detector.detect(frame)

            # Get current date and time for display and logging
            now = datetime.datetime.now()
            date_str = now.strftime("%d-%m-%Y")
            time_str = now.strftime("%H:%M:%S")

            # --- MOTION LOGGING LOGIC ---
            # Check for a transition from NO MOTION to MOTION DETECTED
            if motion_detected and not previous_motion_state:
                # Add a 2-second debounce/cooldown period
                # This prevents rapid "flickering" motion from generating hundreds of events
                time_since_last_log = (now - last_logged_time).total_seconds()
                
                if time_since_last_log >= 2.0:
                    try:
                        # Log a single event when motion begins
                        logger.log_motion(now, "MOTION DETECTED", num_objects)
                        last_logged_time = now # Update the cooldown timer
                        print(f"[{time_str}] Motion logged: {num_objects} object(s) detected.")
                    except Exception as e:
                        # If JSON logging fails (e.g. disk full), don't crash the webcam app
                        print(f"Error: Failed to log motion event - {e}")
            
            # Update the previous state for the next frame's comparison
            previous_motion_state = motion_detected
            # ----------------------------

            # 6. Gather information to display on the screen
            # Determine colors based on motion status (BGR format)
            if motion_detected:
                status_text = "MOTION DETECTED"
                status_color = (0, 0, 255) # Red for motion
            else:
                status_text = "NO MOTION"
                status_color = (0, 255, 0) # Green for no motion

            # General text color (e.g., white)
            text_color = (255, 255, 255)

            # 7. Draw text overlays onto the processed_frame
            # cv2.putText(image, text, position(x,y), font, scale, color, thickness)
            cv2.putText(processed_frame, "=================================", (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, text_color, 1)
            cv2.putText(processed_frame, "MOTION DETECTION SYSTEM", (10, 45), cv2.FONT_HERSHEY_SIMPLEX, 0.6, text_color, 2)
            cv2.putText(processed_frame, "=================================", (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 0.5, text_color, 1)
            
            cv2.putText(processed_frame, "Camera Status : ON", (10, 105), cv2.FONT_HERSHEY_SIMPLEX, 0.5, text_color, 1)
            cv2.putText(processed_frame, f"Date          : {date_str}", (10, 130), cv2.FONT_HERSHEY_SIMPLEX, 0.5, text_color, 1)
            cv2.putText(processed_frame, f"Time          : {time_str}", (10, 155), cv2.FONT_HERSHEY_SIMPLEX, 0.5, text_color, 1)
            cv2.putText(processed_frame, f"Motion Status : {status_text}", (10, 180), cv2.FONT_HERSHEY_SIMPLEX, 0.5, status_color, 2)
            cv2.putText(processed_frame, f"Objects       : {num_objects}", (10, 205), cv2.FONT_HERSHEY_SIMPLEX, 0.5, text_color, 1)

            # 8. Display the live processed frame
            cv2.imshow("Simple Motion Detection System", processed_frame)

            # 9. Wait for 1 millisecond and check if the user pressed a key
            # cv2.waitKey returns the ASCII value of the key pressed
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q') or key == ord('Q'):
                print("Quitting the application...")
                break

    finally:
        # 10. Always release the camera and destroy all OpenCV windows on exit
        cap.release()
        cv2.destroyAllWindows()
        
        print("\n=================================")
        print("MOTION DETECTION SYSTEM")
        print("=================================")
        print("Camera stopped.")
        print("Generating motion statistics...")
        
        try:
            stats = generate_statistics("motion_data.json", "motion_statistics.png")
            if stats:
                print("Motion statistics saved to: motion_statistics.png")
            else:
                print("Notice: No motion statistics were generated (no data or error occurred).")
        except Exception as e:
            print(f"Error generating statistics: {e}")
            
        print("Motion detection system closed.")

if __name__ == "__main__":
    main()
