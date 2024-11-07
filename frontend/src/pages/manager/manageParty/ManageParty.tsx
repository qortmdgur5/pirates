import { useState } from "react";
import Modal from "react-modal";
import DatePicker from "react-datepicker";
import "react-datepicker/dist/react-datepicker.css";
import { ko } from "date-fns/locale"; // 한국어 로케일 추가

// 컴포넌트
import Header from "../../../components/common/header/Header";
import MenuBox from "../../../components/common/menuBox/MenuBox";
import ProfileBox from "../../../components/common/profileBox/ProfileBox";
import RadioButton from "../../../components/common/radio/RadioButton";
import styles from "./styles/manageParty.module.scss";
import NameSearch from "../../../components/common/search/NameSearch";
import ManagePartyTable from "./components/ManagePartyTable";
import axios from "axios";

Modal.setAppElement("#root"); // 앱의 최상위 요소를 설정

function ManageParty() {
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

  // 현재 날짜 yyyy-MM-dd 형식으로 설정
  const getTodayDate = () => {
    const today = new Date();
    today.setHours(0, 0, 0, 0); // 시간 제거
    return today;
  };

  // 폼 데이터 상태
  const [id, setId] = useState<number>(1); // 초기 숙소 PK 키 임시 1로 지정
  const [partyDate, setPartyDate] = useState<Date>(getTodayDate);
  const [partyOpen, setPartyOpen] = useState<boolean>(false);
  const [partyTime, setPartyTime] = useState<string>("");
  const [number, setNumber] = useState<number | null>(null);

  // 최신 순 오래된 순 상태
  const [selectedOption, setSelectedOption] = useState(false);
  // 페이지 상태
  const [page, setPage] = useState<number>(0);
  // 페이지 사이즈 상태 기본 10 사이즈로 설정
  const [pageSize, setSageSize] = useState<number>(10);


  const handleRadioChange = (value: boolean) => {
    setSelectedOption(value);
  };

  const handleSubmit = async (event: React.FormEvent) => {
    event.preventDefault();

    // 서버로 보낼 데이터
    const postData = {
      id,
      partyDate,
      partyOpen,
      partyTime,
      number,
    };

    try {
      const response = await axios.post("/api/manager/party", postData, {
        headers: { "Content-Type": "application/json" },
      });
      console.log("파티방 개설 성공:", response.data);
      closeModal(); // 모달 닫기
    } catch (error) {
      console.error("파티방 개설 실패:", error);
    }
  };

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

  const [isDatePickerOpen, setIsDatePickerOpen] = useState(false);
  const [isTimePickerOpen, setIsTimePickerOpen] = useState(false);

  // 날짜를 'yyyy-MM-dd' 형식으로 변환하는 함수
  const formatDate = (date: Date) => {
    return date.toISOString().split("T")[0]; // YYYY-MM-DD 형식
  };

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
                    value={false}
                    checked={selectedOption === false}
                    onChange={handleRadioChange}
                  />
                  <RadioButton
                    label="오래된 순"
                    name="oldestOrders"
                    value={true}
                    checked={selectedOption === true}
                    onChange={handleRadioChange}
                  />
                </div>
                <NameSearch />
              </div>
              <ManagePartyTable isOldestOrders={selectedOption} page={page} pageSize={pageSize} />
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
                <form
                  onSubmit={handleSubmit}
                  className={styles.party_register_form}
                >
                  <div className={styles.party_register_form_input_box}>
                    <p className={styles.party_register_form_input_left}>
                      파티 날짜
                    </p>
                    <div
                      className={styles.party_register_form_input_right}
                      style={{ position: "relative" }}
                    >
                      <p className={styles.date_input_text}>{formatDate(partyDate)}</p>
                      <button
                        type="button"
                        onClick={() => setIsDatePickerOpen(true)}
                        className={styles.date_calendar_emoji}
                      >
                        🗓️
                      </button>
                      {isDatePickerOpen && (
                        <div
                          style={{
                            position: "absolute",
                            top: "100%",
                            left: 0,
                            zIndex: 10,
                          }}
                        >
                          <DatePicker
                            selected={partyDate}
                            onChange={(date: Date | null) => {
                              setPartyDate(date || getTodayDate());
                              setIsDatePickerOpen(false);
                            }}
                            dateFormat="yyyy-MM-dd"
                            locale={ko} // 한글 설정
                            inline
                          />
                        </div>
                      )}
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
                          type="radio"
                          className={styles.party_register_check_box}
                          name="partyExist"
                          value="true"
                          checked={partyOpen === true}
                          onChange={() => setPartyOpen(true)}
                        />
                      </div>
                      <div className={styles.party_not_exist_check_box}>
                        <p className={styles.party_register_input_text}>무</p>
                        <input
                          type="radio"
                          className={styles.party_register_check_box}
                          name="partyExist"
                          value="false"
                          checked={partyOpen === false}
                          onChange={() => setPartyOpen(false)}
                        />
                      </div>
                    </div>
                  </div>
                  <div className={styles.party_register_form_input_box}>
                    <p className={styles.party_register_form_input_left}>
                      시작시간
                    </p>
                    <div className={styles.party_register_form_input_right}>
                      <p className={styles.time_input_text}>8:00PM</p>
                      <button type="button" className={styles.time_clock_emoji}>
                        🕜
                      </button>
                    </div>
                  </div>
                  <div className={styles.party_register_form_input_box}>
                    <p className={styles.party_register_form_input_left}>
                      최대인원
                    </p>
                    <div className={styles.party_register_form_input_right}>
                      <input
                        className={styles.party_register_max_input}
                        type="text"
                      />
                    </div>
                  </div>
                  <div className={styles.button_box}>
                    <button type="button" className={styles.blue_button}>
                      등록
                    </button>
                    <button
                      type="button"
                      onClick={closeModal}
                      className={styles.gray_button}
                    >
                      취소
                    </button>
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
