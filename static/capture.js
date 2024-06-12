$(document).ready(function() {
    function updateCoords() {
        const x1 = $('#x1').val();
        const y1 = $('#y1').val();
        const x2 = $('#x2').val();
        const y2 = $('#y2').val();

        // Обновляем значения в интерфейсе
        $('#x1_val').text(x1);
        $('#y1_val').text(y1);
        $('#x2_val').text(x2);
        $('#y2_val').text(y2);

        // Отправляем данные на сервер
        $.ajax({
            type: 'POST',
            url: '/update_coords',
            contentType: 'application/json',
            data: JSON.stringify({ x1: x1, y1: y1, x2: x2, y2: y2 }),
            success: function() {
                console.log('Coordinates updated');
            }
        });
    }

    function updateThreshold() {
        const threshold = $('#threshold').val();
        $('#threshold_val').text(threshold);
    
        // Обновляем пороговое изображение на сервере
        $.ajax({
            type: 'POST',
            url: '/update_threshold',
            contentType: 'application/json',
            data: JSON.stringify({ threshold: threshold }),
            success: function(response) {
                if (response.imageData) {
                    $('#threshImage').attr('src', response.imageData).show();
                    recognizeText();  // Вызов функции распознавания текста
                } else {
                    console.error(response.message);
                    alert('Failed to update threshold image: ' + response.message);
                }
            },
            error: function() {
                alert('Failed to update threshold image');
            }
        });
    }

    // Обновление координат при изменении слайдеров
    $('#x1, #y1, #x2, #y2').on('input', updateCoords);

    // Обновление порогового значения при изменении слайдера
    $('#threshold').on('input', updateThreshold);

    // Обработчик нажатия кнопки захвата изображения
    $('#captureImageButton').on('click', function() {
        $.ajax({
            type: 'POST',
            url: '/capture_image',
            success: function(response) {
                if (response.imageData && response.grayImageData) {
                    // Обновление src атрибутов изображений
                    $('#capturedImage').attr('src', response.grayImageData).show();
                    $('#threshImage').attr('src', response.imageData).show();
                } else {
                    console.error(response.message);
                    alert('Failed to capture image: ' + response.message);
                }
            },
            error: function() {
                alert('Failed to capture image');
            }
        });
    });
});

//function recognizeText() {  Добавляем функцию распознавания текста 
    // Отправляем запрос на сервер для распознавания текста
    //$.ajax({
    //    type: 'POST',
    //    url: '/recognize_text',
    //    success: function(response) {
    //        if (response.recognizedText) {
    //            $('#recognizedText').text(response.recognizedText);
    //        } else {
    //            console.error(response.message);
    //            alert('Failed to recognize text: ' + response.message);
    //        }
    //    },
    //    error: function() {
    //        alert('Failed to recognize text');
    //    }
    //});