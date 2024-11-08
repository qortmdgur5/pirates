import styles from "./styles/reservationStatusTable.module.scss";

// 참석자 정보를 정의하는 인터페이스
interface Participant {
  id: number;      // ID
  name: string;    // 이름
  phone: string;   // 연락처
  age: number;     // 나이
  gender: string;  // 성별
  mbti: string; // MBTI
  region: string; // 지역
}

// ParticipantTable의 props 타입 정의
interface ParticipantTableProps {
  data: Participant[]; // 참석자 리스트
}

function ParticipantTable({ data }: ParticipantTableProps) {
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
          {data.map((item, index) => (
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
                <button className={styles.red_button}>삭제</button>
              </td>
              <td className={styles.td_right_black}></td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default ParticipantTable;
