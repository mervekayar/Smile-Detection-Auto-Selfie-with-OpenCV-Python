# Smile Detection Auto Selfie

A Python application that uses OpenCV and MediaPipe to detect facial landmarks and automatically capture a selfie when a smile-like mouth movement is detected.

## Features

- Real-time webcam video processing
- Facial landmark detection with MediaPipe
- Distance-based smile estimation
- Automatic photo capture
- Sound notification after capturing a photo
- Cooldown mechanism to prevent repeated captures
- Press ESC to exit the application

## Technologies Used

- Python
- OpenCV
- MediaPipe
- Math
- Time
- Winsound

## Requirements

- Python 3.10 or a compatible Python version
- A working webcam
- Windows operating system for the `winsound` module
- Internet connection for the initial model download

## Installation

1. Clone this repository:

   ```bash
   git clone https://github.com/YOUR-USERNAME/smile-detection-auto-selfie.git
   ```

2. Navigate to the project directory:

   ```bash
   cd smile-detection-auto-selfie
   ```

3. Install the required packages:

   ```bash
   pip install opencv-python mediapipe
   ```

4. Place a `sound.wav` audio file in the project working directory.

5. Run the application:

   ```bash
   python auto_capture_smiling.py
   ```

The MediaPipe face landmark model is downloaded automatically on the first run if it is not already available in the working directory.

## How It Works

1. The application captures frames from the webcam.
2. MediaPipe detects facial landmarks in each frame.
3. The application calculates the pixel distance between two selected facial landmarks.
4. When the distance exceeds a configurable threshold and the cooldown conditions are satisfied, a selfie is saved as `selfie.png`.
5. A sound notification is played after the photo is captured.

## Configuration

- `THRESHOLD`: Distance threshold used to estimate a smile-like mouth movement.
- `capture_cooldown`: Minimum waiting time between photo captures, in seconds.
- `MODEL_PATH`: Local path to the MediaPipe face landmark model.

The distance-based method is a simple heuristic, not a dedicated smile classification model. Results may vary depending on camera resolution, face position, and individual facial features.

## Notes

- The application requires webcam access.
- The `winsound` module is specific to Windows.
- The `sound.wav` file must be available in the working directory.
- Captured photos may be overwritten when a new selfie is saved with the same filename.

## Future Improvements

- Use a dedicated smile classification model.
- Add configurable thresholds and capture settings.
- Support saving multiple photos with timestamps.
- Add cross-platform audio support.

## License

No license has been specified yet.
