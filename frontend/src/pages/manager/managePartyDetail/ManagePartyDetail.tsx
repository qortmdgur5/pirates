import { useEffect, useState } from "react";
import Header from "../../../components/common/header/Header";
import MenuBox from "../../../components/common/menuBox/MenuBox";
import ProfileBox from "../../../components/common/profileBox/ProfileBox";
import ParticipantTable from "./components/ParticipantTable";
import ReservationStatusTable from "./components/ReservationStatusTable";
import styles from "./styles/managePartyDetail.module.scss";
import Modal from "react-modal";
import ParticipantModalTable from "./components/ParticipantModalTable";
import { useLocation, useNavigate } from "react-router-dom";
import axios from "axios";
import { useRecoilValue } from "recoil";
import { authAtoms } from "../../../atoms/authAtoms";

Modal.setAppElement("#root"); // 앱의 최상위 요소를 설정

interface Participant {
  id: number; // ID
  name: string; // 이름
  phone: string; // 연락처
  age: number; // 나이
  gender: string; // 성별
  mbti: string; // MBTI
  region: string; // 지역
}

interface ParticipantAPIResponse {
  data: Participant[];
  totalCount: number;
}

function ManagePartyDetail() {
  const { state } = useLocation(); // 전달된 state를 가져옵니다, 파티방 상세페이지 예약현황 데이터, 이전 manageParty 페이지에서 넘어온 데이터
  const partyId = state.id; // Party PK
  const partyDate = state.partyDate; // Party 날짜
  const team = state.team; // team 데이터
  const [participants, setParticipants] = useState<Participant[]>([]); // 참석자 명단 데이터
  const [participantCount, setParticipantCount] = useState<number>(
    state.participant
  ); // 참가자 수 상태
  const partyData = state;
  const [page, setPage] = useState<number>(0); // 페이지 상태
  const [pageSize, setPageSize] = useState<number>(10); // 페이지 사이즈 상태 기본 10 사이즈로 설정
  const [totalCount, setTotalCount] = useState<number>(0);
  const navigate = useNavigate();
  const user = useRecoilValue(authAtoms);
  const role = user.role;
  const token = user.token;
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
      width: "57.917vw",
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

  const fetchParticipants = () => {
    axios
      .get(`/api/manager/party/${partyId}`, {
        params: { page, pageSize, token },
      })
      .then((response) => {
        const filteredData = response.data.data.map((item: Participant) => ({
          id: item.id,
          name: item.name,
          phone: item.phone,
          age: item.age,
          gender: item.gender,
          mbti: item.mbti,
          region: item.region,
        }));
        setParticipants(filteredData);
        setTotalCount(response.data.totalCount);
      })
      .catch((error) => console.error("API 호출 실패:", error));
  };

  useEffect(() => {
    fetchParticipants();
  }, [partyId, page, pageSize]);

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
            <p className={styles.manage_title}>예약 현황</p>
            <div className={styles.manage_box}>
              <ReservationStatusTable
                data={partyData}
                participantCount={participantCount}
              />
            </div>
            <p className={styles.manage_title}>참석자 명단</p>
            <div className={styles.manage_box}>
              <button className={styles.blue_button} onClick={openModal}>
                등록
              </button>
              <Modal
                isOpen={isModalOpen}
                onRequestClose={closeModal}
                contentLabel="참석자 관리 모달"
                style={customModalStyles}
                ariaHideApp={false}
              >
                <button
                  className={styles.modal_close_button}
                  onClick={closeModal}
                >
                  닫기 X
                </button>

                <ParticipantModalTable
                  partyId={partyId}
                  onRegister={fetchParticipants}
                  participant={participantCount}
                  setParticipantCount={setParticipantCount}
                  token={token}
                />
              </Modal>
              <ParticipantTable
                data={participants}
                setParticipantCount={setParticipantCount}
                page={page}
                pageSize={pageSize}
                totalCount={totalCount}
                onPageChange={setPage} // 페이지 변경 시 호출
                onPageSizeChange={setPageSize} // 페이지 사이즈 변경 시 호출
                token={token}
              />
              <div className={styles.party_detail_button_box}>
                <button className={styles.party_modify_button} type="button">
                  파티방 수정
                </button>
                <button className={styles.party_delete_button} type="button">
                  파티방 삭제
                </button>
                <button
                  className={styles.party_enter_button}
                  type="button"
                  onClick={() =>
                    navigate(`/manager/party/userList`, {
                      state: { ...state },
                    })
                  }
                >
                  파티방 입장
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </>
  );
}

export default ManagePartyDetail;
