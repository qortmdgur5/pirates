import styles from './styles/reservationStatusTable.module.scss'

function ReservationStatusTable() {
  const data = [
    {
      no: "01",
      date: "24.09.29",
      time: "8:00PM",
      max:"100",
      participant: "72",
    },
  ];

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
          {data.map((item, index) => (
            <tr key={index}>
              <td className={styles.td_left_black}></td>
              <td className={styles.text_center}>{item.no}</td>
              <td className={styles.text_center}>{item.date}</td>
              <td className={styles.text_center}>{item.time}</td>
              <td className={styles.text_center}>{item.max + `명`}</td>
              <td className={styles.text_center}>{item.participant + `명`}</td>
              <td className={styles.td_right_black}></td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default ReservationStatusTable