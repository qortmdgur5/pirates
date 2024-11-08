import { useState, useEffect } from "react";
import styles from "./styles/reservationStatusTable.module.scss";
import Pagination from "../../../../components/common/pagination/Pagination";

// 참석자 정보를 정의하는 인터페이스
interface Participant {
  id: number;
  name: string;
  phone: string;
  age: number;
  gender: string;
  mbti: string;
  region: string;
}

// ParticipantTable의 props 타입 정의
interface ParticipantTableProps {
  data: Participant[];
  setParticipantCount: React.Dispatch<React.SetStateAction<number>>;
  page: number;
  pageSize: number;
  totalCount: number;
  onPageChange: (newPage: number) => void;
  onPageSizeChange: (newPageSize: number) => void;
}

function ParticipantTable({
  data,
  setParticipantCount,
  page,
  pageSize,
  totalCount,
  onPageChange,
  onPageSizeChange,
}: ParticipantTableProps) {
  const [participants, setParticipants] = useState<Participant[]>([]);

  useEffect(() => {
    setParticipants(data); // data가 로딩되면 participants 업데이트
  }, [data]); // data가 변경될 때마다 업데이트

  // 삭제 처리 함수
  const handleDelete = async (id: number) => {
    try {
      const response = await fetch(`/api/manager/participant/${id}`, {
        method: "DELETE",
      });

      if (response.ok) {
        // 성공적으로 삭제되면 UI에서 해당 항목을 제거
        setParticipants((prevParticipants) =>
          prevParticipants.filter((participant) => participant.id !== id)
        );
        setParticipantCount((prev) => prev - 1);
      } else {
        console.error("삭제 실패:", response.statusText);
      }
    } catch (error) {
      console.error("삭제 요청 에러:", error);
    }
  };

  return (
    <div className={styles.table_container}>
      <table className={styles.guest_house_table}>
        <thead>
          <tr>
            <th className={styles.th_left_blank}></th>
            <th className={styles.text_center}>NO.</th>
            <th className={styles.text_center}>이름</th>
            <th className={styles.text_center}>연락처</th>
            <th className={styles.text_center}>나이</th>
            <th className={styles.text_center}>성별</th>
            <th className={styles.text_center}>MBTI</th>
            <th className={styles.text_center}>지역</th>
            <th className={styles.text_center}>삭제</th>
            <th className={styles.th_right_blank}></th>
          </tr>
        </thead>
        <tbody>
          {participants.map((item, index) => (
            <tr key={index}>
              <td className={styles.td_left_black}></td>
              <td className={styles.text_center}>{index + 1}</td>
              <td className={styles.text_center}>{item.name}</td>
              <td className={styles.text_center}>{item.phone}</td>
              <td className={styles.text_center}>{item.age}</td>
              <td className={styles.text_center}>{item.gender}</td>
              <td className={styles.text_center}>{item.mbti}</td>
              <td className={styles.text_center}>{item.region}</td>
              <td className={styles.text_center}>
                <button
                  className={styles.red_button}
                  onClick={() => handleDelete(item.id)}
                >
                  삭제
                </button>
              </td>
              <td className={styles.td_right_black}></td>
            </tr>
          ))}
        </tbody>
      </table>
      <Pagination
        page={page}
        pageSize={pageSize}
        totalCount={totalCount}
        onPageChange={onPageChange} // 페이지 변경 시 호출
        onPageSizeChange={onPageSizeChange} // 페이지 사이즈 변경 시 호출
      />
    </div>
  );
}

export default ParticipantTable;
