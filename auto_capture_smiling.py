import cv2
import mediapipe as mp
import winsound
import urllib.request
import os
import math
import time

MODEL_URL = (
    "https://storage.googleapis.com/mediapipe-models/"
    "face_landmarker/face_landmarker/float16/1/"
    "face_landmarker.task"
)

MODEL_PATH = "face_landmarker.task"

if not os.path.exists(MODEL_PATH):
    print("Downloading face recognition model...")
    urllib.request.urlretrieve(MODEL_URL, MODEL_PATH)
    print("Model downloaded.")

BaseOptions = mp.tasks.BaseOptions
FaceLandmarker = mp.tasks.vision.FaceLandmarker
FaceLandmarkerOptions = mp.tasks.vision.FaceLandmarkerOptions
VisionRunningMode = mp.tasks.vision.RunningMode

options = FaceLandmarkerOptions(
    base_options=BaseOptions(model_asset_path=MODEL_PATH),
    running_mode=VisionRunningMode.VIDEO,
    num_faces=1
)

THRESHOLD = 99
last_capture_time = 0
capture_cooldown = 2
smile_detected = False

camera = cv2.VideoCapture(0)

if not camera.isOpened():
    print("The camera didn't open.")
    raise SystemExit

with FaceLandmarker.create_from_options(options) as face_landmarker:

    try:
        while True:
            success, image = camera.read()

            if not success:
                print("The camera failed to capture the image.")
                break

            image = cv2.flip(image, 1)

            fh, fw = image.shape[:2]

            rgb_image = cv2.cvtColor(
                image, cv2.COLOR_BGR2RGB
            )

            mp_image = mp.Image(
                image_format=mp.ImageFormat.SRGB,
                data=rgb_image
            )

            timestamp_ms = int(time.monotonic() * 1000)

            output = face_landmarker.detect_for_video(
                mp_image, timestamp_ms
            )

            if output.face_landmarks:
                landmarks = output.face_landmarks[0]

                point1 = landmarks[43]
                point2 = landmarks[287]

                x1 = int(point1.x * fw)
                y1 = int(point1.y * fh)

                x2 = int(point2.x * fw)
                y2 = int(point2.y * fh)

                cv2.circle(image, (x1, y1), 5, (0, 255, 0), -1)
                cv2.circle(image, (x2, y2), 5, (0, 255, 0), -1)

                dist = int(math.hypot(x2 - x1, y2 - y1))

                cv2.putText(
                    image,
                    f"Distance: {dist}",
                    (20, 40),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1,
                    (0, 255, 0),
                    2
                )

                current_time = time.monotonic()

                if (
                    dist > THRESHOLD
                    and not smile_detected
                    and current_time - last_capture_time
                    >= capture_cooldown
                ):
                    cv2.imwrite("selfie.png", image)
                    print("Selfie saved!")

                    winsound.PlaySound(
                        "sound.wav",
                        winsound.SND_FILENAME | winsound.SND_ASYNC
                    )

                    last_capture_time = current_time
                    smile_detected = True

                elif dist <= THRESHOLD:
                    smile_detected = False

            cv2.imshow(
                "Auto Selfie - Face Landmarker",
                image
            )

            key = cv2.waitKey(1) & 0xFF

            if key == 27:
                break

    finally:
        camera.release()
        cv2.destroyAllWindows()
