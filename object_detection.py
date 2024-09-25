import time
import sys
import cv2
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision

# Global variables to calculate FPS
COUNTER, FPS = 0, 0
START_TIME = time.time()
detection_result_list = []

def run(model: str, max_results: int, score_threshold: float, 
        camera_id: int, width: int, height: int, detection_callback=None) -> None:

    # Start capturing video input from the camera
    cap = cv2.VideoCapture(camera_id)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)


    start_time = time.time()  # Record the start time

    def save_result(result: vision.ObjectDetectorResult, unused_output_image: mp.Image, timestamp_ms: int):
        detection_result_list.clear() 

        for detection in result.detections:
            if detection.categories:
                detected_object = detection.categories[0].category_name
                score = detection.categories[0].score
                detection_result_list.append((detected_object, score))

        if detection_callback:
            detection_callback(detection_result_list)
        else:
            for obj, score in detection_result_list:
                print(f"Detected object: {obj}, Confidence: {score}")

    # Initialize the object detection model
    base_options = python.BaseOptions(model_asset_path=model)
    options = vision.ObjectDetectorOptions(base_options=base_options,
                                           running_mode=vision.RunningMode.LIVE_STREAM,
                                           max_results=max_results, score_threshold=score_threshold,
                                           result_callback=save_result)
    detector = vision.ObjectDetector.create_from_options(options)


    while cap.isOpened():
        success, image = cap.read()
        if not success:
            sys.exit('ERROR: Unable to read from camera.')

        rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_image)

        detector.detect_async(mp_image, time.time_ns() // 1_000_000)
        
        # ESC key to stop program.
        if cv2.waitKey(1) == 27:
            break

    detector.close()
    cap.release()
    cv2.destroyAllWindows()
