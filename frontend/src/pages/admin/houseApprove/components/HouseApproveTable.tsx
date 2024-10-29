import styles from "./styles/houseApproveTable.module.scss";
import Modal from "react-modal";
import ApproveButton from "../../../../components/common/button/ApproveButton";
import DenyButton from "../../../../components/common/button/DenyButton";
import { useEffect, useState } from "react";
import axios from "axios";

Modal.setAppElement("#root"); // 앱의 최상위 요소를 설정

interface Owner {
  id: number;
  name: string;
  username: string;
  phoneNumber: string;
  isAuth: boolean;
}

interface HouseApproveTableProps {
  isOldestOrders: boolean;
}

const HouseApproveTable: React.FC<HouseApproveTableProps> = ({
  isOldestOrders,
}) => {
  const [data, setData] = useState<Owner[]>([]);
  const [isApproveModalOpen, setIsApproveModalOpen] = useState(false);
  const [isDenyModalOpen, setIsDenyModalOpen] = useState(false);
  const [selectedOwnerName, setSelectedOwnerName] = useState<string>(""); // 클릭한 아이템의 이름 저장

  const customModalStyles: ReactModal.Styles = {
    overlay: {
      backgroundColor: "rgba(0, 0, 0, 0.529)",
      width: "100%",
      height: "100vh",
      zIndex: "10",
      position: "fixed",
      top: "0",
      left: "0",
    },
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

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await axios.get<Owner[]>("/api/admin/owners", {
          params: { isOldestOrders, skip: 0, limit: 10 },
          headers: { accept: "application/json" },
        });

        setData(response.data);
      } catch (error) {
        console.error("데이터를 불러오는데 실패했습니다.", error);
      }
    };

    fetchData();
  }, [isOldestOrders]); // isOldestOrders가 변경될 때마다 데이터 갱신

  const openApproveModal = (name: string) => {
    setSelectedOwnerName(name); // 클릭한 아이템의 이름 저장
    setIsApproveModalOpen(true);
  };

  const closeApproveModal = () => setIsApproveModalOpen(false);

  const openDenyModal = (name: string) => {
    setSelectedOwnerName(name); // 클릭한 아이템의 이름 저장
    setIsDenyModalOpen(true);
  };

  const closeDenyModal = () => setIsDenyModalOpen(false);

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
              <td className={styles.text_left}>{index + 1}</td>
              <td className={styles.text_left}>{item.name}</td>
              <td className={styles.text_left}>{item.username}</td>
              <td className={styles.text_left}>{item.phoneNumber}</td>
              <td className={styles.text_center}>
                {item.isAuth ? "Yes" : "No"}
              </td>
              <td className={styles.text_center}>
                <ApproveButton
                  isApprove={item.isAuth}
                  onClick={() => openApproveModal(item.name)}
                />
              </td>
              <td className={styles.text_center}>
                <DenyButton onClick={() => openDenyModal(item.name)} />
              </td>
              <td className={styles.td_right_black}></td>
            </tr>
          ))}
        </tbody>
      </table>
      <Modal
        isOpen={isApproveModalOpen}
        onRequestClose={closeApproveModal}
        contentLabel="승인 확인 모달"
        style={customModalStyles}
        ariaHideApp={false}
      >
        <p
          className={styles.modal_text_1}
        >{`"${selectedOwnerName}" 님을 승인하시겠습니까?`}</p>
        <div className={styles.modal_button_box}>
          <button className={styles.modal_blue_button}>확인</button>
          <button
            className={styles.modal_gray_button}
            onClick={closeApproveModal}
          >
            취소
          </button>
        </div>
      </Modal>
      <Modal
        isOpen={isDenyModalOpen}
        onRequestClose={closeDenyModal}
        contentLabel="승인 취소 모달"
        style={customModalStyles}
        ariaHideApp={false}
      >
        <p
          className={styles.modal_text_1}
        >{`"${selectedOwnerName}" 님을 취소하시겠습니까?`}</p>
        <div className={styles.modal_button_box}>
          <button className={styles.modal_blue_button}>확인</button>
          <button className={styles.modal_gray_button} onClick={closeDenyModal}>
            취소
          </button>
        </div>
      </Modal>
    </div>
  );
};

export default HouseApproveTable;
