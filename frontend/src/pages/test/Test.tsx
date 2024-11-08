import React, { useEffect, useState } from 'react';
import axios from 'axios';

interface PhotoData {
  albumId: number;
  id: number;
  title: string;
  url: string;
  thumbnailUrl: string;
}

function Test() {
  const [photos, setPhotos] = useState<PhotoData[]>([]);

  useEffect(() => {
    const fetchPhotos = async () => {
      try {
        const response = await axios.get("https://jsonplaceholder.typicode.com/photos");
        setPhotos(response.data.slice(0, 50)); // 상위 5개 데이터만 가져옴
      } catch (error) {
        console.error("데이터 가져오기 실패:", error);
      }
    };

    fetchPhotos();
  }, []);

  return (
    <div>
      <h3>사진 데이터</h3>
      <ul>
        {photos.map((photo) => (
          <li key={photo.id}>
            <img src={photo.thumbnailUrl} alt={photo.title} />
            <p>{photo.title}</p>
          </li>
        ))}
      </ul>
    </div>
  );
}

export default Test;
