import styles from "./styles/managerApproveTable.module.scss"

// 컴포넌트
import ApproveButton from "../../../../components/common/button/ApproveButton";
import DenyButton from "../../../../components/common/button/DenyButton";

function ManagerApproveTable() {
  const data = [
    {
      no: "01",
      name: "백승혁",
      id: "qortmdgur",
      phone: "010-3345-7789",
      date: "23.02.21",
      isApprove: true,
    },
    {
      no: "02",
      name: "김철수",
      id: "rlacjftn",
      phone: "010-3345-7789",
      date: "23.02.21",
      isApprove: false,
    },
    {
      no: "03",
      name: "백찬영",
      id: "qorcksdud",
      phone: "010-3345-7789",
      date: "23.02.21",
      isApprove: true,
    },
  ];

  return (
    <div className={styles.table_container}>
      <table className={styles.guest_house_table}>
        <thead>
          <tr>
            <th className={styles.th_left_blank}></th>
            <th className={styles.text_left}>NO.</th>
            <th className={styles.text_left}>이름</th>
            <th className={styles.text_left}>아이디</th>
            <th className={styles.text_left}>연락처</th>
            <th className={styles.text_left}>가입날짜</th>
            <th className={styles.text_center}>승인여부</th>
            <th className={styles.text_center}>승인</th>
            <th className={styles.text_center}>취소</th>
            <th className={styles.th_right_blank}></th>
          </tr>
        </thead>
        <tbody>
          {data.map((item, index) => (
            <tr key={index}>
              <td className={styles.td_left_black}></td>
              <td className={styles.text_left}>{item.no}</td>
              <td className={styles.text_left}>{item.name}</td>
              <td className={styles.text_left}>{item.id}</td>
              <td className={styles.text_left}>{item.phone}</td>
              <td className={styles.text_left}>{item.date}</td>
              <td className={styles.text_center}>{item.isApprove ? "Yes" : "No"}</td>
              <td className={styles.text_center}><ApproveButton isApprove={item.isApprove} /></td>
              <td className={styles.text_center}><DenyButton /></td>
              <td className={styles.td_right_black}></td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default ManagerApproveTable