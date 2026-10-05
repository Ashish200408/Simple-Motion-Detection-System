"""
Module for detecting motion using OpenCV.
"""
import cv2
import numpy as np

class MotionDetector:
    def __init__(self, min_contour_area=500):
        """
        Initialize the motion detector.
        
        Args:
            min_contour_area (int): The minimum area of a contour to be considered as a valid object.
        """
        self.min_contour_area = min_contour_area
        self.previous_frame = None

    def detect(self, frame):
        """
        Detect motion in the given frame.

        Args:
            frame (numpy.ndarray): The current BGR frame from a video or webcam.

        Returns:
            tuple: (processed_frame, motion_detected, num_objects, bounding_boxes)
        """
        # Create a copy of the frame to draw on
        processed_frame = frame.copy()
        
        # 1. Convert to grayscale: Simplifies the image, reducing data to process and removing color dependence
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # 2. Apply Gaussian Blur: Smoothes the image, which helps to remove high-frequency noise 
        # and reduces false positives in motion detection
        blurred_frame = cv2.GaussianBlur(gray_frame, (21, 21), 0)

        # Handle the first frame: Initialize previous_frame and return no motion
        if self.previous_frame is None:
            self.previous_frame = blurred_frame
            return processed_frame, False, 0, []

        # 3. Frame difference: Compute the absolute difference between the current frame and the previous frame
        # This highlights areas that have changed (motion)
        frame_diff = cv2.absdiff(self.previous_frame, blurred_frame)

        # 4. Threshold: Apply a binary threshold to the difference image. 
        # Pixels with a difference greater than 25 become white (255), others become black (0)
        _, thresh = cv2.threshold(frame_diff, 25, 255, cv2.THRESH_BINARY)

        # 5. Dilation: Dilate the thresholded image to fill in holes and make object boundaries more complete
        thresh = cv2.dilate(thresh, None, iterations=2)

        # 6. Contour detection: Find the boundaries of the white regions (moving objects)
        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        motion_detected = False
        bounding_boxes = []

        # Iterate over all found contours
        for contour in contours:
            # Ignore very small contours to filter out minor noise
            if cv2.contourArea(contour) < self.min_contour_area:
                continue

            motion_detected = True
            
            # 7. Bounding boxes: Compute the bounding rectangle for valid moving objects
            (x, y, w, h) = cv2.boundingRect(contour)
            bounding_boxes.append((x, y, w, h))
            
            # Draw a green rectangle around the detected object on the processed frame
            cv2.rectangle(processed_frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        # Update the previous frame for the next iteration
        self.previous_frame = blurred_frame

        return processed_frame, motion_detected, len(bounding_boxes), bounding_boxes

