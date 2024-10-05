import styles from "./styles/managePartyTable.module.scss"

// 컴포넌트

function ManagePartyTable() {
  const data = [
    {
      no: "01",
      date: "24.09.29",
      participant: "99",
      max:"100",
      isActive: true,
      time: "8:00 PM",
    },
    {
      no: "02",
      date: "24.09.29",
      participant: "99",
      max:"100",
      isActive: false,
      time: "8:00 PM",
    },
    {
      no: "03",
      date: "24.09.29",
      participant: "99",
      max:"100",
      isActive: true,
      time: "8:00 PM",
    },
  ];

  return (
    <div className={styles.table_container}>
      <table className={styles.guest_house_table}>
        <thead>
          <tr>
            <th className={styles.th_left_blank}></th>
            <th className={styles.text_center}>NO.</th>
            <th className={styles.text_center}>파티 일자</th>
            <th className={styles.text_center}>참석 인원</th>
            <th className={styles.text_center}>파티여부</th>
            <th className={styles.text_center}>파티 시작 시간</th>
            <th className={styles.th_right_blank}></th>
          </tr>
        </thead>
        <tbody>
          {data.map((item, index) => (
            <tr key={index}>
              <td className={styles.td_left_black}></td>
              <td className={styles.text_center}>{item.no}</td>
              <td className={styles.text_center}>{item.date}</td>
              <td className={styles.text_center}>{item.participant}/{item.max}</td>
              <td className={styles.text_center}>{item.isActive ? `O` : `X`}</td>
              <td className={styles.text_center}>{item.time}</td>
              <td className={styles.td_right_black}></td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default ManagePartyTable