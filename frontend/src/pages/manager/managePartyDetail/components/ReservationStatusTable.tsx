import styles from './styles/reservationStatusTable.module.scss';

interface ReservationStatusTableProps {
  data: {
    id: number;
    partyDate: string;
    number: number;
    partyOpen: boolean;
    partyTime: string;
    participant: number;
  };
  participantCount: number;
}

function ReservationStatusTable({ data, participantCount }: ReservationStatusTableProps) {
  return (
    <div className={styles.table_container}>
      <table className={styles.guest_house_table}>
        <thead>
          <tr>
            <th className={styles.th_left_blank}></th>
            <th className={styles.text_center}>NO.</th>
            <th className={styles.text_center}>파티날짜</th>
            <th className={styles.text_center}>시작 시간</th>
            <th className={styles.text_center}>최대 인원</th>
            <th className={styles.text_center}>예약 인원</th>
            <th className={styles.th_right_blank}></th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td className={styles.td_left_black}></td>
            <td className={styles.text_center}>{data.id}</td>
            <td className={styles.text_center}>{data.partyDate}</td>
            <td className={styles.text_center}>{data.partyTime}</td>
            <td className={styles.text_center}>{data.number}명</td>
            <td className={styles.text_center}>{participantCount}명</td>
            <td className={styles.td_right_black}></td>
          </tr>
        </tbody>
      </table>
    </div>
  );
}

export default ReservationStatusTable;
