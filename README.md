
## Silhouette-Automated incident detection system

This project is a Flask web application that uses YOLO (You Only Look Once) for object detection in video streams. The application supports uploading videos, live webcam feed detection, and email alerts when specific incidents are detected.

## Features

- Upload video files for object detection
- Live webcam feed detection
- Email alerts for detected incidents (e.g., fall detection)

## Requirements

- Python 3.x
- Flask
- Flask-Mail
- Flask-WTF
- OpenCV
- YOLOv8 (Ultralytics)

## Installation

1. **Clone the repository:**

    ```sh
    git clone https://github.com/your-username/flask-yolo-detection.git
    cd flask-yolo-detection
    

2. **Create a virtual environment and activate it:**

    ```sh
    python3 -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. **Install the required packages:**

    ```sh
    pip install -r requirements.txt
    ```

4. **Download YOLO weights and place them in the specified directory:**

    Download the required YOLO weights and place them in the `YOLO-Weights` directory.

5. **Set up environment variables:**

    Create a `.env` file and add your email credentials:

    ```env
    SECRET_KEY=your_secret_key
    MAIL_SERVER=smtp.gmail.com
    MAIL_PORT=465
    MAIL_USERNAME=your_email@gmail.com
    MAIL_PASSWORD=your_email_password
    ```

## Usage

1. **Run the Flask application:**

    ```sh
    python app.py
    ```

2. **Access the application:**

    Open your web browser and go to `http://127.0.0.1:5000`.
   

## Email Notification

The application sends an email notification when a fall is detected. Ensure you have configured the email credentials correctly in the `.env` file.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## STEP BY STEP INSTRUCTIONS:

Clone the repository:

1) Open your terminal and run:
   
   ```sh   
   git clone https://github.com/your-username/flask-yolo-detection.git
   cd flask-yolo-detection
   ```

3) Create a virtual environment and activate it:
   
   ```sh
   python3 -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

5) Install the required packages:
   ```sh
    pip install -r requirements.txt
   ```

6) Download YOLO weights:
Download the required YOLO weights and place them in the YOLO-Weights directory.

8) Run the Flask application:
python app.py

7)Access the application:
Open your web browser and go to `http://127.0.0.1:5000`.

8)Upload a video file:
Go to the "Upload Video" page, select a video file, and click "Run". The video will be processed, and detected objects will be displayed.

9)View live webcam feed:
Go to the "Webcam" page to view live object detection from your webcam.

10)Receive email alerts:
Ensure that your email credentials are correctly configured to receive alerts for detected incidents (e.g., falls).

