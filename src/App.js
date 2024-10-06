import React, { useRef, useState } from 'react';
import ReactPlayer from 'react-player';
import axios from 'axios';

function VideoRecorder() {
  const [recordedBlob, setRecordedBlob] = useState(null);
  const [isRecording, setIsRecording] = useState(false);
  const videoRef = useRef(null);
  const mediaRecorderRef = useRef(null);

  // ЗАПИСЬ ВИДЕО
  const startRecording = async () => {
    const stream = await navigator.mediaDevices.getUserMedia({ video: true, audio: true });
    videoRef.current.srcObject = stream;
    
    const mediaRecorder = new MediaRecorder(stream);
    mediaRecorderRef.current = mediaRecorder;
    
    mediaRecorder.ondataavailable = (event) => {
      setRecordedBlob(event.data);
      mediaRecorder.stop();
    };
    
    mediaRecorder.start();
    setIsRecording(true);
  };

  // ОТПРАВКА НА СЕРВЕР 
  const handleUpload = () => {
    if (recordedBlob) {
      uploadFile(recordedBlob);
    } else {
      console.error('Нет записанного видео для отправки');
    }
  };

  const uploadFile = async (file) => {

    const chunkSize = 1024 * 10; // 10 Кб
    const formData = new FormData();

    formData.append('file_name', 'file.name');
    formData.append('file_size', file.size);
    formData.append('mime_type', 'string');
    formData.append('user', 1);
    formData.append('group_id', 421);
    formData.append('total_chunks', Math.ceil(file.size/(chunkSize)));

    try {
      // Инициируем загрузку файла (отправляем рамер, имя и получаем id для загрузки чанков)
      const response = await axios.post('http://127.0.0.1:8000/api/video/upload/init/', formData);
      const uploadId = response.data.upload_id;

      // Загрузка чанка (кол-во циклов зависит от кол-ва чанков в файле)
      for (let offset = 0; offset < file.size; offset += chunkSize) {

        const reader = new FileReader();

        await new Promise((resolve) => {
          reader.onload = async (event) => {

            // Вычисляем индексы и кол-во чанков
            const chunkBlob = new Blob([event.target.result], { type: 'video/mp4' });
            const chunkIndex = Math.floor(offset / chunkSize);

            const formData = new FormData();
    
            formData.append('chunk_index', chunkIndex);
            formData.append('chunk', chunkBlob, `chunk_${chunkIndex}`);
    
            try {
              await axios.patch(`http://127.0.0.1:8000/api/video/upload/${uploadId}/chunk/`, formData);
              console.log(`Чанк ${chunkIndex} отправлен`);
            } catch (error) {
              console.error('Ошибка при отправке чанка:', error);
            }
            resolve();
          };
          // Читаем текущий чанк файла (предыдущий размер + 10 Кб)
          reader.readAsArrayBuffer(file.slice(offset, offset + chunkSize));
        });
      }
      const completeResponse = await axios.post(`http://127.0.0.1:8000/api/video/upload/${uploadId}/complete/`);
      console.log(`Загрузка файла завершена, статус: ${completeResponse.data.status}, URL: ${completeResponse.data.file_url}`);
    } catch (error) {
      console.error('Ошибка при отправке информации о файле:', error);
    }
  };

  const stopRecording = () => {
    mediaRecorderRef.current.stop();
    setIsRecording(false);
  };

  return (
    <div>
      <video ref={videoRef} autoPlay muted />
      <button onClick={startRecording} disabled={isRecording}>
        Начать запись
      </button>
      <button onClick={stopRecording} disabled={!isRecording}>
        Остановить запись
      </button>
      {recordedBlob && (
        <ReactPlayer
          url={URL.createObjectURL(recordedBlob)}
          controls
          width="100%"
          height="300px"
        />
      )}
      <button onClick={handleUpload} disabled={!recordedBlob}>Отправить видео</button>
    </div>
  );
}

export default VideoRecorder;