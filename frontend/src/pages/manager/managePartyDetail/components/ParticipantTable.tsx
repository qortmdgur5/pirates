import styles from './styles/reservationStatusTable.module.scss'

function ParticipantTable() {
  const data = [
    {
      no: "01",
      name: "백승혁",
      phone: "010-0000-1122",
      age:"100",
      sex: true,
    },
    {
      no: "02",
      name: "김철수",
      phone: "010-0000-1122",
      age:"100",
      sex: false,
    },
    {
      no: "03",
      name: "백찬영",
      phone: "010-0000-1122",
      age:"22",
      sex: false,
    },
  ];

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
            <th className={styles.text_center}>삭제</th>
            <th className={styles.th_right_blank}></th>
          </tr>
        </thead>
        <tbody>
          {data.map((item, index) => (
            <tr key={index}>
              <td className={styles.td_left_black}></td>
              <td className={styles.text_center}>{item.no}</td>
              <td className={styles.text_center}>{item.name}</td>
              <td className={styles.text_center}>{item.phone}</td>
              <td className={styles.text_center}>{item.age}</td>
              <td className={styles.text_center}>{item.sex ? `남` : `여`}</td>
              <td className={styles.text_center}>삭제버튼</td>
              <td className={styles.td_right_black}></td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default ParticipantTable