import { useState } from "react";
import Modal from "react-modal";

// 컴포넌트
import Header from "../../../components/common/header/Header";
import MenuBox from "../../../components/common/menuBox/MenuBox";
import ProfileBox from "../../../components/common/profileBox/ProfileBox";
import RadioButton from "../../../components/common/radio/RadioButton";
import styles from "./styles/manageParty.module.scss";
import NameSearch from "../../../components/common/search/NameSearch";
import ManagePartyTable from "./components/ManagePartyTable";

Modal.setAppElement("#root"); // 앱의 최상위 요소를 설정

function ManageParty() {
  // 메뉴 탭 데이터
  const managerMenuTabs = [
    { text: "게스트 하우스 관리", isActive: false, path: "/manager/houseRegister" },
    { text: "매니저 등록 관리", isActive: false, path: "/manager/managerApprove" },
    { text: "파티방 관리", isActive: true, path: "/manager/manageParty" },
    { text: "마이페이지", isActive: false, path: "#" },
  ];

  const [selectedOption, setSelectedOption] = useState("recentlyRegistered");

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
      top: "50%",
      left: "50%",
      transform: "translate(-50%, -50%)",
      borderRadius: "15px",
      boxShadow: "2px 2px 2px rgba(0, 0, 0, 0.25)",
      backgroundColor: "white",
      padding: "48px 84px 90px 84px",
    },
  };

  // 파티방 개설 모달 상태 관리
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
            <p className={styles.manage_title}>파티방 관리</p>
            <div className={styles.manage_box}>
              <div className={styles.search_box}>
                <div className={styles.radio_box}>
                  <RadioButton
                    label="최근 등록 순"
                    name="recentlyRegistered"
                    value="recentlyRegistered"
                    checked={selectedOption === "recentlyRegistered"}
                    onChange={setSelectedOption}
                  />
                  <RadioButton
                    label="오래된 순"
                    name="oldRegistered"
                    value="oldRegistered"
                    checked={selectedOption === "oldRegistered"}
                    onChange={setSelectedOption}
                  />
                </div>
                <NameSearch />
              </div>
              <ManagePartyTable />
              <button className={styles.blue_button} onClick={openModal}>
                파티방 개설하기
              </button>
              <Modal
                isOpen={isModalOpen}
                onRequestClose={closeModal}
                contentLabel="파티방 개설 모달"
                style={customModalStyles}
                ariaHideApp={false}
              >
                <div className={styles.modal_logo_box}>
                  <div className={styles.modal_logo_img_box}>
                    <img
                      src="/src/assets/image/pirates_logo_img.png"
                      alt="modal_logo_img"
                    />
                  </div>
                  <p className={styles.modal_logo_text}>해적</p>
                </div>
                <p className={styles.modal_text_1}>파티방 개설</p>
                <p className={styles.modal_text_2}>
                  회원정보는 개인정보취급방침에 따라 안전하게 보호되며 회원님의
                  명확한 동의 없이 공개 또는 제 3자에게 제공되지 않습니다.
                </p>
                <form className={styles.party_register_form}>
                  <div className={styles.party_register_form_input_box}>
                    <p className={styles.party_register_form_input_left}>
                      파티 날짜
                    </p>
                    <div className={styles.party_register_form_input_right}>
                      <p className={styles.date_input_text}>24.09.29</p>
                      <button className={styles.date_calendar_emoji}>🗓️</button>
                    </div>
                  </div>
                  <div className={styles.party_register_form_input_box}>
                    <p className={styles.party_register_form_input_left}>
                      파티 여부
                    </p>
                    <div className={styles.party_register_form_input_right}>
                      <div className={styles.party_exist_check_box}>
                        <p className={styles.party_register_input_text}>유</p>
                        <input
                          type="checkbox"
                          className={styles.party_register_check_box}
                        ></input>
                      </div>
                      <div className={styles.party_not_exist_check_box}>
                        <p className={styles.party_register_input_text}>무</p>
                        <input
                          type="checkbox"
                          className={styles.party_register_check_box}
                        ></input>
                      </div>
                    </div>
                  </div>
                  <div className={styles.party_register_form_input_box}>
                    <p className={styles.party_register_form_input_left}>
                      시작시간
                    </p>
                    <div className={styles.party_register_form_input_right}>
                      <p className={styles.time_input_text}>8:00PM</p>
                      <button className={styles.time_clock_emoji}>🕜</button>
                    </div>
                  </div>
                  <div className={styles.party_register_form_input_box}>
                    <p className={styles.party_register_form_input_left}>
                      최대인원
                    </p>
                    <div className={styles.party_register_form_input_right}>
                      <input className={styles.party_register_max_input} type="text" />
                    </div>
                  </div>
                  <div className={styles.button_box}>
                    <button type="button" className={styles.blue_button}>등록</button>
                    <button type="button" onClick={closeModal} className={styles.gray_button}>취소</button>
                  </div>
                </form>
              </Modal>
            </div>
          </div>
        </div>
      </div>
    </>
  );
}

export default ManageParty;
