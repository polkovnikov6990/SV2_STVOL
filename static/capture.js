// Предполагаемая функция захвата кадра из видеопотока и преобразование его в Base64
function captureFrameToBase64(videoElement) {
    const canvas = document.createElement('canvas');
    canvas.width = videoElement.videoWidth;
    canvas.height = videoElement.videoHeight;
    const ctx = canvas.getContext('2d');
    ctx.drawImage(videoElement, 0, 0, canvas.width, canvas.height);
    return canvas.toDataURL('image/jpeg');
}

// Асинхронная функция для отправки захваченного изображения на сервер и получения обработанного изображения
async function sendFrameAndProcess(imageData) {
    try {
        const response = await fetch('/process_frame', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ image: imageData })
        });

        if (!response.ok) {
            throw new Error('Network response was not ok');
        }

        const data = await response.json();
        return data.image; // Возвращаем обработанное изображение
    } catch (error) {
        console.error('Error:', error);
    }
}

// Функция для отображения обработанного изображения на странице
function displayProcessedFrame(imageData) {
    const image = new Image();
    image.src = imageData;
    image.onload = function() {
        const container = document.getElementById('processedFrameContainer'); // Убедитесь, что у вас есть этот контейнер в HTML
        container.innerHTML = ''; // Очистка предыдущего изображения, если оно есть
        container.appendChild(image);
    };
}

// Главная функция, объединяющая все шаги
async function captureAndProcessFrame() {
    const videoElement = document.querySelector('video');
    const imageData = captureFrameToBase64(videoElement);

    try {
        const response = await fetch('/save_image', { // Предполагаемый маршрут на сервере
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ image: imageData })
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        } else {
            console.log('Изображение успешно отправлено на сервер');
        }
    } catch (error) {
        console.error('Ошибка при отправке изображения:', error);
    }
}

// Обработчик нажатия на кнопку "Захватить изображение"
document.getElementById('captureImageButton').addEventListener('click', captureAndProcessFrame);