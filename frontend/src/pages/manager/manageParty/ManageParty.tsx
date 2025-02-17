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
import ManagePartyTable from "./components/ManagePartyTable";
import axios from "axios";
import { useRecoilValue } from "recoil";
import { accomoAtoms, authAtoms } from "../../../atoms/authAtoms";

Modal.setAppElement("#root"); // 앱의 최상위 요소를 설정

function ManageParty() {
  const user = useRecoilValue(authAtoms);
  const role = user.role;
  const token = user.token;
  const accomoAtom = useRecoilValue(accomoAtoms);
  const accomoId = accomoAtom.accomodation_id;

  // 메뉴 탭 데이터
  const allManagerMenuTabs = [
    {
      text: "게스트 하우스 관리",
      isActive: false,
      path: "/owner/manageHouse",
    },
    {
      text: "매니저 등록 관리",
      isActive: false,
      path: "/owner/managerApprove",
    },
    {
      text: "파티방 관리",
      isActive: true,
      path: "/manager/manageParty",
    },
  ];

  // ROLE_NOTAUTH_OWNER 또는 ROLE_AUTH_OWNER이면 전체 메뉴, 아니면 파티방 관리만 표시
  const managerMenuTabs =
    role === "ROLE_NOTAUTH_OWNER" || role === "ROLE_AUTH_OWNER"
      ? allManagerMenuTabs
      : allManagerMenuTabs.filter((tab) => tab.text === "파티방 관리");

  // 현재 날짜 yyyy-MM-dd 형식으로 설정
  const getTodayDate = () => {
    const today = new Date();
    today.setHours(0, 0, 0, 0); // 시간 제거
    return today;
  };

  // 날짜를 'yyyy-MM-dd' 형식으로 변환하는 함수
  const formatDate = (date: Date | null) => {
    if (date === null) {
      date = calendarDate as Date;
    }
    // 로컬 시간대의 연, 월, 일 가져오기
    const year = date.getFullYear();
    const month = String(date.getMonth() + 1).padStart(2, "0"); // 월은 0부터 시작하므로 +1 필요
    const day = String(date.getDate()).padStart(2, "0");

    const formattedDate = `${year}-${month}-${day}`;
    return formattedDate; // YYYY-MM-DD 형식
  };

  // 시간 노출 포맷팅 함수 8:00 PM 형식으로
  const formatTime = (date: Date | undefined): string => {
    if (!date) {
      return "8:00 PM"; // date가 undefined인 경우 기본값 처리
    }
    // date를 12시간 형식으로 포맷
    const hours = date.getHours();
    const minutes = date.getMinutes();

    // 오전/오후 판단
    const period = hours >= 12 ? "PM" : "AM";

    // 12시간 형식으로 시간 변환 (12시일 때는 0시로, 24시를 12시로 변환)
    const formattedHours = hours % 12 || 12;
    const formattedMinutes = String(minutes).padStart(2, "0");

    return `${formattedHours}:${formattedMinutes} ${period}`; // 예시: "8:00 PM"
  };

  // 폼 데이터로 보낼 시간 변수 포맷팅
  const formatTimeToHHMM00 = (date: Date): string => {
    const hours = date.getHours();
    const minutes = date.getMinutes();

    // 24시간 형식으로 시간 변환 (2자리로 표현)
    const formattedHours = String(hours).padStart(2, "0");
    const formattedMinutes = String(minutes).padStart(2, "0");

    return `${formattedHours}-${formattedMinutes}-00`; // 예시: "08-00-00"
  };

  const [calendarDate, setCalendarDate] = useState<Date | null>(getTodayDate); // 파티방 개설 캘린더 날짜 상태
  const [AMPMTime, setAMPMTime] = useState<Date>(); // 파티방 개설 시간 상태

  // 폼 데이터 상태
  const [partyDate, setPartyDate] = useState<string>(formatDate(calendarDate));
  const [partyOpen, setPartyOpen] = useState<boolean>(false);
  const [partyTime, setPartyTime] = useState<string>("20-00-00");
  const [number, setNumber] = useState<number>(100);
  const [team, setTeam] = useState<number>(0);

  // 최신 순 오래된 순 상태
  const [selectedOption, setSelectedOption] = useState(false);

  // 파티방 시작 끝 검색조건 날짜
  const [startCalendarDate, setStartCalendarDate] = useState<Date | null>(
    getTodayDate
  ); // 시작날짜 캘린더 날짜 상태
  const [endCalendarDate, setEndCalendarDate] = useState<Date | null>(
    getTodayDate
  ); // 끝날짜 개설 캘린더 날짜 상태
  const [startDate, setStartDate] = useState<string>(""); // 시작날짜
  const [endDate, setEndDate] = useState<string>(""); // 끝날짜

  // 컴포넌트 안의 fetch 함수 트리거 상태
  const [fetchTrigger, setFetchTriger] = useState<boolean>(false);

  // 라디오 버튼 변경 함수
  const handleRadioChange = (value: boolean) => {
    setSelectedOption(value);
  };

  // 파티방 개설 버튼 함수
  const handleSubmit = async (event: React.FormEvent) => {
    event.preventDefault();

    // 서버로 보낼 데이터
    const postData = {
      id: accomoId,
      partyDate,
      partyOpen,
      partyTime,
      number,
      team,
    };

    try {
      const response = await axios.post("/api/manager/party", postData, {
        params: { token },
        headers: { "Content-Type": "application/json" },
      });
      closeModal(); // 모달 닫기
      setFetchTriger((prev) => !prev);
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
      width: "44.01vw",
      height: "fit-content",
      zIndex: "20",
      position: "absolute",
      top: "50%",
      left: "50%",
      transform: "translate(-50%, -50%)",
      borderRadius: "0.781vw",
      boxShadow: "0.104vw 0.104vw 0.104vw rgba(0, 0, 0, 0.25)",
      backgroundColor: "white",
      padding: "2.5vw 4.375vw 4.688vw 4.375vw",
    },
  };

  // 파티방 개설 모달 상태 관리
  const [isModalOpen, setIsModalOpen] = useState(false);

  const openModal = () => setIsModalOpen(true);
  const closeModal = () => setIsModalOpen(false);

  // 달력 오픈 상태
  const [isDatePickerOpen, setIsDatePickerOpen] = useState(false);
  // 시작 날짜 달력 오픈 상태
  const [isStartDatePickerOpen, setIsStartDatePickerOpen] = useState(false);
  // 끝 날짜 달력 오픈 상태
  const [isEndDatePickerOpen, setIsEndDatePickerOpen] = useState(false);
  // 시계 오픈 상태
  const [isTimePickerOpen, setIsTimePickerOpen] = useState(false);

  return (
    <>
      <Header />
      <div className={styles.container}>
        <div className={styles.house_manage_left_box}>
          <ProfileBox />
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
                <div className={styles.date_box}>
                  <div
                    className={styles.start_date_input_box}
                    style={{ position: "relative" }}
                  >
                    <p className={styles.date_input_text}>{startDate}</p>
                    <button
                      type="button"
                      onClick={() => setIsStartDatePickerOpen((prev) => !prev)}
                      className={styles.date_calendar_emoji}
                    >
                      🗓️
                    </button>
                    {isStartDatePickerOpen && (
                      <div
                        style={{
                          position: "absolute",
                          top: "100%",
                          left: 0,
                          zIndex: 10,
                        }}
                      >
                        <DatePicker
                          selected={startCalendarDate}
                          onChange={(date: Date | null) => {
                            setStartDate(formatDate(date));
                            setStartCalendarDate(date);
                            setIsStartDatePickerOpen(false);
                          }}
                          dateFormat="yyyy-MM-dd"
                          locale={ko} // 한글 설정
                          inline
                        />
                      </div>
                    )}
                  </div>
                  <p className={styles.middle_text}>~</p>
                  <div
                    className={styles.end_date_input_box}
                    style={{ position: "relative" }}
                  >
                    <p className={styles.date_input_text}>{endDate}</p>
                    <button
                      type="button"
                      onClick={() => setIsEndDatePickerOpen((prev) => !prev)}
                      className={styles.date_calendar_emoji}
                    >
                      🗓️
                    </button>
                    {isEndDatePickerOpen && (
                      <div
                        style={{
                          position: "absolute",
                          top: "100%",
                          left: 0,
                          zIndex: 10,
                        }}
                      >
                        <DatePicker
                          selected={endCalendarDate}
                          onChange={(date: Date | null) => {
                            setEndDate(formatDate(date));
                            setEndCalendarDate(date);
                            setIsEndDatePickerOpen(false);
                          }}
                          dateFormat="yyyy-MM-dd"
                          locale={ko} // 한글 설정
                          inline
                        />
                      </div>
                    )}
                  </div>
                </div>
              </div>
              <ManagePartyTable
                isOldestOrders={selectedOption}
                fetchTrigger={fetchTrigger}
                token={token}
                accomoId={accomoId}
                startDate={startDate}
                endDate={endDate}
              />
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
                      <p className={styles.date_input_text}>{partyDate}</p>
                      <button
                        type="button"
                        onClick={() => setIsDatePickerOpen((prev) => !prev)}
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
                            selected={calendarDate}
                            onChange={(date: Date | null) => {
                              setPartyDate(formatDate(date));
                              setCalendarDate(date);
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
                    <div
                      className={styles.party_register_form_input_right}
                      style={{ position: "relative" }}
                    >
                      <p className={styles.time_input_text}>
                        {formatTime(AMPMTime)}
                      </p>
                      <button
                        type="button"
                        className={styles.time_clock_emoji}
                        onClick={() => setIsTimePickerOpen((prev) => !prev)}
                      >
                        🕜
                      </button>
                      {isTimePickerOpen && (
                        <div
                          style={{
                            position: "absolute",
                            top: "100%",
                            left: 0,
                            zIndex: 10,
                          }}
                        >
                          <DatePicker
                            onChange={(date: Date | null) => {
                              if (date) {
                                setPartyTime(formatTimeToHHMM00(date)); // 포맷된 시간 문자열을 상태로 업데이트
                                setAMPMTime(date);
                                setIsTimePickerOpen(false);
                              }
                            }} // 날짜가 선택되면 상태 업데이트
                            showTimeSelect // 시간 선택 가능
                            showTimeSelectOnly // 날짜를 숨기고 시간만 선택
                            timeIntervals={15} // 시간 간격 설정 (15분 간격)
                            timeCaption="시간" // 시간 캡션
                            dateFormat="HH:mm" // 시간 형식 (날짜는 제외)
                            timeFormat="HH:mm" // 시간 형식
                            placeholderText="시간을 선택하세요" // 기본 텍스트
                          />
                        </div>
                      )}
                    </div>
                  </div>
                  <div className={styles.party_register_form_input_box}>
                    <p className={styles.party_register_form_input_left}>
                      최대인원
                    </p>
                    <div className={styles.party_register_form_input_right}>
                      <input
                        className={styles.party_register_max_input}
                        type="number"
                        value={number} // 상태를 input 값에 연결
                        onChange={(e) => setNumber(Number(e.target.value))} // 입력값을 숫자로 변환 후 상태 업데이트
                      />
                    </div>
                  </div>
                  <div className={styles.party_register_form_input_box}>
                    <p className={styles.party_register_form_input_left}>
                      팀 OR 테이블
                    </p>
                    <div className={styles.party_register_form_input_right}>
                      <input
                        className={styles.party_register_max_input}
                        type="number"
                        value={team} // 상태를 input 값에 연결
                        onChange={(e) => setTeam(Number(e.target.value))} // 입력값을 숫자로 변환 후 상태 업데이트
                      />
                    </div>
                  </div>
                  <div className={styles.button_box}>
                    <button
                      type="button"
                      className={styles.blue_button}
                      onClick={handleSubmit}
                    >
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
