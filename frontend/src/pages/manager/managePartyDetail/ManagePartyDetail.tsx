import { useState } from "react";
import Header from "../../../components/common/header/Header";
import MenuBox from "../../../components/common/menuBox/MenuBox";
import ProfileBox from "../../../components/common/profileBox/ProfileBox";
import ParticipantTable from "./components/ParticipantTable";
import ReservationStatusTable from "./components/ReservationStatusTable";
import styles from "./styles/managePartyDetail.module.scss";
import Modal from "react-modal";
import ParticipantModalTable from "./components/ParticipantModalTable";

Modal.setAppElement("#root"); // 앱의 최상위 요소를 설정

function ManagePartyDetail() {
  // 메뉴 탭 데이터
  const managerMenuTabs = [
    {
      text: "게스트 하우스 관리",
      isActive: false,
      path: "/manager/manageHouse",
    },
    {
      text: "매니저 등록 관리",
      isActive: false,
      path: "/manager/managerApprove",
    },
    { text: "파티방 관리", isActive: true, path: "/manager/manageParty" },
    { text: "마이페이지", isActive: false, path: "#" },
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
      width: "1112px",
      height: "fit-content",
      zIndex: "20",
      position: "absolute",
      top: "50%",
      left: "50%",
      transform: "translate(-50%, -50%)",
      backgroundColor: "transparent",
      border: "none",
      padding: "0",
      overflow: "visible",
    },
  };

  // 참석자 등록 삭제 모달 상태 관리
  const [isModalOpen, setIsModalOpen] = useState(false);

  const openModal = () => setIsModalOpen(true);
  const closeModal = () => setIsModalOpen(false);

  return (
    <>
      <Header />
      <div className={styles.container}>
        <div className={styles.house_manage_left_box}>
          <ProfileBox
            name="매니저님"
            imgSrc="/src/assets/image/woman_icon_img.png"
            userId="sky1004"
          />
          <MenuBox menuTabs={managerMenuTabs} />
        </div>
        <div className={styles.house_manage_right_box}>
          <div className={styles.manage_container}>
            <p className={styles.manage_title}>예약 현황</p>
            <div className={styles.manage_box}>
              <ReservationStatusTable />
            </div>
            <p className={styles.manage_title}>참석자 명단</p>
            <div className={styles.manage_box}>
              <button className={styles.blue_button} onClick={openModal}>
                등록
              </button>
              <Modal
                isOpen={isModalOpen}
                onRequestClose={closeModal}
                contentLabel="파티방 개설 모달"
                style={customModalStyles}
                ariaHideApp={false}
              >
                <button
                  className={styles.modal_close_button}
                  onClick={closeModal}
                >
                  닫기 X
                </button>

                <ParticipantModalTable />
              </Modal>
              <ParticipantTable />
            </div>
          </div>
        </div>
      </div>
    </>
  );
}

export default ManagePartyDetail;
