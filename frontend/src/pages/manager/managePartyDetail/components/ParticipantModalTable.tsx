import styles from "./styles/participantModalTable.module.scss";

function ParticipantModalTable() {
  const data = [
    {
      name: "백승혁",
      phone: "010-0000-1122",
      age: "100",
      sex: true,
    },
    {
      name: "김철수",
      phone: "010-0000-1122",
      age: "100",
      sex: false,
    },
    {
      name: "백찬영",
      phone: "010-0000-1122",
      age: "22",
      sex: false,
    },
  ];

  return (
    <div className={styles.table_container}>
      <table className={styles.participant_modal_table}>
        <thead>
          <tr>
            <th className={styles.th_left_blank}></th>
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
              <td className={styles.text_center}>{item.name}</td>
              <td className={styles.text_center}>{item.phone}</td>
              <td className={styles.text_center}>{item.age}</td>
              <td className={styles.text_center}>{item.sex ? `남` : `여`}</td>
              <td className={styles.text_center}>
                <button className={styles.x_button}>X</button>
              </td>
              <td className={styles.td_right_black}></td>
            </tr>
          ))}
          <tr>
            <td className={styles.td_left_black}></td>
            <td className={styles.modal_input}>
              <input type="text" placeholder="이름" />
            </td>
            <td className={styles.modal_input}>
              <input type="text" placeholder="연락처" />
            </td>
            <td className={styles.modal_input}>
              <input type="text" placeholder="나이" />
            </td>
            <td className={styles.modal_input}>
              <input type="text" placeholder="성별" />
            </td>
            <td className={styles.modal_input}></td>
            <td className={styles.td_right_black}></td>
          </tr>
        </tbody>
      </table>
      <div className={styles.modal_blue_button_box}>
        <button className={styles.blue_button}>등록하기</button>
      </div>
    </div>
  );
}

export default ParticipantModalTable;
