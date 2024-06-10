from flask import Flask, render_template, Response, request, jsonify
import cv2
import pandas as pd
import numpy as np
import base64
import os
import easyocr
from image_processing import capture_image as process_capture_image, apply_threshold, convert_to_bw

app = Flask(__name__)

# Начальные координаты для зеленого квадрата
x1, y1, x2, y2 = 100, 100, 200, 200

camera = cv2.VideoCapture(1)  # Захват видео с камеры
reader = easyocr.Reader(['ru'])


def gen_frames():
    global x1, y1, x2, y2
    while True:
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


@app.route('/capture_image', methods=['POST'])
def capture_image():
    global x1, y1, x2, y2
    success, frame = camera.read()
    if success:
        try:
            # Логирование для отладки
            print(f"Read a frame from the camera: {frame.shape}")
            print(f"Cropping coordinates: x1={x1}, y1={y1}, x2={x2}, y2={y2}")

            # Обрезка изображения по координатам квадрата
            cropped_frame = frame[y1:y2, x1:x2]
            print("Cropped the frame successfully")

            if cropped_frame.size == 0:
                print("Cropped frame is empty")
                return jsonify({'message': 'Cropped frame is empty'}), 500

            # Конвертация изображения в черно-белый формат
            gray_image = cv2.cvtColor(cropped_frame, cv2.COLOR_BGR2GRAY)
            print("Converted the frame to grayscale")

            # Кодирование изображения в base64
            _, buffer = cv2.imencode('.jpg', gray_image)
            encoded_image = base64.b64encode(buffer).decode('utf-8')
            image_data = f'data:image/jpeg;base64,{encoded_image}'
            print("Encoded the image to base64")

            return jsonify({'imageData': image_data})

        except Exception as e:
            print(f"Exception: {e}")
            return jsonify({'message': 'An error occurred during image processing', 'error': str(e)}), 500
    else:
        print("Failed to read a frame from the camera")
    return jsonify({'message': 'Failed to capture image'}), 500

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'excelFile' not in request.files:
        return "No file part", 400
    file = request.files['excelFile']
    if file.filename == '':
        return "No selected file", 400
    if file:
        # Чтение Excel файла
        df = pd.read_excel(file)
        # Преобразование всех значений в одномерный массив
        data = df.values.flatten().tolist()
        # Возвращаем данные в виде одномерного массива
        return jsonify(data)

@app.route('/process_frame', methods=['POST'])
def process_frame():
    try:
        data = request.get_json()
        image_data = data['image']
        image_data = base64.b64decode(image_data.split(',')[1])

        # Преобразование изображения в формат, с которым может работать OpenCV
        nparr = np.frombuffer(image_data, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        # Применение вашей логики обработки изображений
        img_bw_cv = convert_to_bw(img)
        img_bw_threshold = apply_threshold(img_bw_cv, 128)

        # Конвертация обработанного изображения обратно в base64 для отправки на клиент
        _, buffer = cv2.imencode('.jpg', img_bw_threshold)
        encoded_image = base64.b64encode(buffer)
        encoded_image_str = 'data:image/jpeg;base64,' + encoded_image.decode('utf-8')

        return jsonify({'image': encoded_image_str})
    except Exception as e:
        print(f"Exception in process_frame: {e}")
        return jsonify({'message': 'Error processing frame', 'error': str(e)}), 500

@app.route('/save_image', methods=['POST'])
def save_image():
    try:
        data = request.get_json()
        image_data = data['image']
        image_data = image_data.split(",")[1]
        image_bytes = base64.b64decode(image_data)

        # Указываем путь к папке /tmp и имя файла
        image_path = '/tmp/captured_image.jpg'

        # Сохраняем изображение
        with open(image_path, 'wb') as image_file:
            image_file.write(image_bytes)

        return 'Изображение сохранено', 200
    except Exception as e:
        print(f"Exception while saving image: {e}")
        return 'Failed to save image', 500

def ocr_recognition(image):
    try:
        temp_image_path = 'temp_image.jpg'
        cv2.imwrite(temp_image_path, image)
        result = reader.readtext(temp_image_path, detail=0)
        os.remove(temp_image_path)
        return " ".join(result)
    except Exception as e:
        print(f"Exception in OCR recognition: {e}")
        return 'Failed to recognize text'

if __name__ == '__main__':
    app.run(debug=True)