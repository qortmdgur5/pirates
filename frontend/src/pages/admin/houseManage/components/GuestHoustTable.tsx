import styles from "./styles/guestHouseTable.module.scss";

function GuestHouseTable() {
  const data = [
    {
      no: "01",
      name: "부산 게스트 하우스",
      address: "부산광역시 어디어디",
      contact: "051-123-4567",
      registrationDate: "21.09.15",
    },
    {
      no: "02",
      name: "서울 게스트 하우스",
      address: "서울특별시 어디어디",
      contact: "02-111-2222",
      registrationDate: "23.01.04",
    },
    {
      no: "03",
      name: "인천 게스트 하우스",
      address: "인천광역시 어디어디",
      contact: "031-111-3333",
      registrationDate: "24.10.29",
    },
  ];

  return (
    <div className={styles.table_container}>
      <table className={styles.guest_house_table}>
        <thead>
          <tr>
            <th className={styles.th_left_blank}></th>
            <th className={styles.text_left}>NO.</th>
            <th className={styles.text_left}>게스트 하우스 이름</th>
            <th className={styles.text_left}>주소</th>
            <th className={styles.text_left}>숙소 연락처</th>
            <th className={styles.text_left}>숙소 등록일</th>
            <th className={styles.th_right_blank}></th>
          </tr>
        </thead>
        <tbody>
          {data.map((item, index) => (
            <tr key={index}>
              <td className={styles.td_left_black}></td>
              <td className={styles.text_left}>{item.no}</td>
              <td className={styles.text_left}>{item.name}</td>
              <td className={styles.text_left}>{item.address}</td>
              <td className={styles.text_left}>{item.contact}</td>
              <td className={styles.text_left}>{item.registrationDate}</td>
              <td className={styles.td_right_black}></td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default GuestHouseTable;
