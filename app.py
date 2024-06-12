from flask import Flask, render_template, Response, request, jsonify
import cv2
import pandas as pd
import numpy as np
import base64
import os
import easyocr
from image_processing import capture_image as process_capture_image, apply_threshold, convert_to_bw

app = Flask(__name__)

# Начальные координаты для зеленого квадрата и пороговое значение
x1, y1, x2, y2 = 100, 100, 400, 350
threshold_value = 128
last_gray_image = None

camera = cv2.VideoCapture(1)  # Захват видео с камеры
reader = easyocr.Reader(['ru'])

def gen_frames():
    global x1, y1, x2, y2
    while True:
        try:
            success, frame = camera.read()  # Чтение кадра
            if not success:
                break
            else:
                # Рисование зеленого квадрата
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                ret, buffer = cv2.imencode('.jpg', frame)
                frame = buffer.tobytes()
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
        except Exception as e:
            print(f"Error in gen_frames: {e}")
            continue

@app.route('/')
def index():
    return render_template('index.html', x1=x1, y1=y1, x2=x2, y2=y2)

@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/video_page')
def video_page():
    return render_template('video.html')

@app.route('/update_coords', methods=['POST'])
def update_coords():
    global x1, y1, x2, y2
    data = request.json
    x1 = int(data['x1'])
    y1 = int(data['y1'])
    x2 = int(data['x2'])
    y2 = int(data['y2'])
    return jsonify({'message': 'Coordinates updated successfully'})

@app.route('/update_threshold', methods=['POST'])
def update_threshold():
    global threshold_value, last_gray_image
    try:
        data = request.json
        threshold_value = int(data['threshold'])

        if last_gray_image is not None:
            _, threshold_image = cv2.threshold(last_gray_image, threshold_value, 255, cv2.THRESH_BINARY)

            # Кодирование порогового изображения в base64
            _, buffer_thresh = cv2.imencode('.jpg', threshold_image)
            encoded_thresh_image = base64.b64encode(buffer_thresh).decode('utf-8')
            thresh_image_data = f'data:image/jpeg;base64,{encoded_thresh_image}'

            return jsonify({'imageData': thresh_image_data})
        else:
            print("No grayscale image available")
            return jsonify({'message': 'No grayscale image available'}), 500
    except Exception as e:
        print(f"Exception in /update_threshold: {e}")
        return jsonify({'message': 'An error occurred during image processing', 'error': str(e)}), 500

@app.route('/capture_image', methods=['POST'])
def capture_image():
    global x1, y1, x2, y2, threshold_value, last_gray_image
    try:
        success, frame = camera.read()
        if success:
            print(f"Read a frame from the camera: {frame.shape}")
            print(f"Cropping coordinates: x1={x1}, y1={y1}, x2={x2}, y2={y2}")

            # Проверка координат обрезки
            if x1 < 0 or y1 < 0 or x2 > frame.shape[1] or y2 > frame.shape[0]:
                print("Cropping coordinates are out of bounds")
                return jsonify({'message': 'Cropping coordinates are out of bounds'}), 500

            cropped_frame = frame[y1:y2, x1:x2]
            print("Cropped the frame successfully")

            if cropped_frame.size == 0:
                print("Cropped frame is empty")
                return jsonify({'message': 'Cropped frame is empty'}), 500

            gray_image = cv2.cvtColor(cropped_frame, cv2.COLOR_BGR2GRAY)
            last_gray_image = gray_image  # Сохранение последнего черно-белого изображения
            print("Converted the frame to grayscale")

            # Применение порогового преобразования
            _, threshold_image = cv2.threshold(gray_image, threshold_value, 255, cv2.THRESH_BINARY)
            print(f"Applied threshold to grayscale image with value {threshold_value}")

            # Кодирование порогового изображения в base64
            _, buffer_thresh = cv2.imencode('.jpg', threshold_image)
            encoded_thresh_image = base64.b64encode(buffer_thresh).decode('utf-8')
            thresh_image_data = f'data:image/jpeg;base64,{encoded_thresh_image}'
            print("Encoded the threshold image to base64")

            # Кодирование черно-белого изображения в base64
            _, buffer_gray = cv2.imencode('.jpg', gray_image)
            encoded_gray_image = base64.b64encode(buffer_gray).decode('utf-8')
            gray_image_data = f'data:image/jpeg;base64,{encoded_gray_image}'
            print("Encoded the grayscale image to base64")

            return jsonify({'imageData': thresh_image_data, 'grayImageData': gray_image_data})

        else:
            print("Failed to read a frame from the camera")
            return jsonify({'message': 'Failed to capture image'}), 500
    except Exception as e:
        print(f"Exception in /capture_image: {e}")
        return jsonify({'message': 'An error occurred during image processing', 'error': str(e)}), 500

@app.route('/upload', methods=['POST'])
def upload_file():
    try:
        if 'excelFile' not in request.files:
            return "No file part", 400
        file = request.files['excelFile']
        if file.filename == '':
            return "No selected file", 400
        if file:
            df = pd.read_excel(file)
            data = df.values.flatten().tolist()
            return jsonify(data)
    except Exception as e:
        print(f"Exception in /upload: {e}")
        return jsonify({'message': 'An error occurred during file upload', 'error': str(e)}), 500

@app.route('/process_frame', methods=['POST'])
def process_frame():
    try:
        data = request.get_json()
        image_data = data['image']
        image_data = base64.b64decode(image_data.split(',')[1])

        nparr = np.frombuffer(image_data, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        img_bw_cv = convert_to_bw(img)
        img_bw_threshold = apply_threshold(img_bw_cv, threshold_value)

        _, buffer = cv2.imencode('.jpg', img_bw_threshold)
        encoded_image = base64.b64encode(buffer)
        encoded_image_str = 'data:image/jpeg;base64,' + encoded_image.decode('utf-8')

        return jsonify({'image': encoded_image_str})
    except Exception as e:
        print(f"Exception in /process_frame: {e}")
        return jsonify({'message': 'Error processing frame', 'error': str(e)}), 500

@app.route('/save_image', methods=['POST'])
def save_image():
    try:
        data = request.get_json()
        image_data = data['image']
        image_data = image_data.split(",")[1]
        image_bytes = base64.b64decode(image_data)

        image_path = '/tmp/captured_image.jpg'

        with open(image_path, 'wb') as image_file:
            image_file.write(image_bytes)

        return 'Изображение сохранено', 200
    except Exception as e:
        print(f"Exception in /save_image: {e}")
        return 'Failed to save image', 500

@app.route('/recognize_text', methods=['POST'])
def recognize_text():
    global last_gray_image, threshold_value
    try:
        if last_gray_image is not None:
            _, threshold_image = cv2.threshold(last_gray_image, threshold_value, 255, cv2.THRESH_BINARY)

            # Сохранение порогового изображения во временный файл
            temp_image_path = 'temp_threshold_image.jpg'
            cv2.imwrite(temp_image_path, threshold_image)

            # Распознавание текста с помощью EasyOCR
            result = reader.readtext(temp_image_path, detail=0)
            recognized_text = " ".join(result)

            # Вывод распознанного текста в терминал
            print(f"Recognized Text: {recognized_text}")


            # Удаление временного файла
            os.remove(temp_image_path)

            return jsonify({'recognizedText': recognized_text})
        else:
            print("No grayscale image available")
            return jsonify({'message': 'No grayscale image available'}), 500
    except Exception as e:
        print(f"Exception in /recognize_text: {e}")
        return jsonify({'message': 'An error occurred during text recognition', 'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)