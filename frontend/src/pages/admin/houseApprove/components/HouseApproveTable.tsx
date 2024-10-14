import styles from "./styles/houseApproveTable.module.scss";
import Modal from "react-modal";

// 컴포넌트
import ApproveButton from "../../../../components/common/button/ApproveButton";
import DenyButton from "../../../../components/common/button/DenyButton";
import { useState } from "react";

Modal.setAppElement("#root"); // 앱의 최상위 요소를 설정

function HouseApproveTable() {
  const data = [
    {
      no: "01",
      name: "백승혁",
      id: "qortmdgur",
      phone: "010-3345-7789",
      isApprove: true,
    },
    {
      no: "02",
      name: "김철수",
      id: "rlacjftn",
      phone: "010-3345-7789",
      isApprove: false,
    },
    {
      no: "03",
      name: "백찬영",
      id: "qorcksdud",
      phone: "010-3345-7789",
      isApprove: true,
    },
  ];

  const customModalStyles: ReactModal.Styles = {
    // overlay 모달 창 외부 영역 디자인
    overlay: {
      backgroundColor: " rgba(0, 0, 0, 0.529)",
      width: "100%",
      height: "100vh",
      zIndex: "10",
      position: "fixed",
      top: "0",
      left: "0",
    },
    // content 모달 창 영역 디자인
    content: {
      display: "flex",
      alignItems: "center",
      justifyContent: "center",
      flexDirection: "column",
      width: "845px",
      height: "fit-content",
      zIndex: "20",
      position: "absolute",
      top: "85%",
      left: "50%",
      transform: "translate(-50%, -50%)",
      borderRadius: "30px",
      boxShadow: "2px 2px 2px rgba(0, 0, 0, 0.25)",
      backgroundColor: "white",
      padding: "45px 0 20px 0",
    },
  };

  const [isModalOpen, setIsModalOpen] = useState(false);

  const openModal = () => setIsModalOpen(true);
  const closeModal = () => setIsModalOpen(false);

  const handleApprove = () => {
    closeModal(); // 모달 닫기
  };

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
              <td className={styles.text_center}>
                {item.isApprove ? "Yes" : "No"}
              </td>
              <td className={styles.text_center}>
                <ApproveButton isApprove={item.isApprove} onClick={openModal}/>
              </td>
              <td className={styles.text_center}>
                <DenyButton />
              </td>
              <td className={styles.td_right_black}></td>
            </tr>
          ))}
        </tbody>
      </table>
      <Modal
        isOpen={isModalOpen}
        onRequestClose={closeModal}
        contentLabel="승인 확인 모달"
        style={customModalStyles}
        ariaHideApp={false}
      >
        <p className={styles.modal_text_1}>"김철수" 님을 승인하시겠습니까?</p>
        <div className={styles.modal_button_box}>
          <button className={styles.modal_blue_button}>확인</button>
          <button className={styles.modal_gray_button} onClick={closeModal}>취소</button>
        </div>
      </Modal>
    </div>
  );
}

export default HouseApproveTable;
