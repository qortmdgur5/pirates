import styles from "./styles/managerApproveTable.module.scss";
import Modal from "react-modal";

// 컴포넌트
import ApproveButton from "../../../../components/common/button/ApproveButton";
import DenyButton from "../../../../components/common/button/DenyButton";
import { useEffect, useState } from "react";
import axios from "axios";
import Pagination from "../../../../components/common/pagination/Pagination";
import { useRecoilValue } from "recoil";
import { authAtoms } from "../../../../atoms/authAtoms";

Modal.setAppElement("#root"); // 앱의 최상위 요소를 설정

interface Manager {
  id: number;
  name: string;
  username: string;
  phoneNumber: string;
  date: string;
  isAuth: boolean;
}

interface ManagerAPIResponse {
  data: Manager[];
  totalCount: number;
}

interface ManagerApproveTableProps {
  isOldestOrders: boolean;
  name: string;
}

const ManagerApproveTable: React.FC<ManagerApproveTableProps> = ({
  isOldestOrders,
  name,
}) => {
  const [data, setData] = useState<Manager[]>([]);
  const [page, setPage] = useState(0); // 페이지 상태 관리
  const [pageSize, setPageSize] = useState(10); // 페이지 사이즈 상태 관리
  const [totalCount, setTotalCount] = useState(0); // 총 항목 개수 상태 관리
  const [isApproveModalOpen, setIsApproveModalOpen] = useState<boolean>(false);
  const [isDenyModalOpen, setIsDenyModalOpen] = useState<boolean>(false);
  const [selectedManagerName, setSelectedManagerName] = useState<string>(""); // 클릭한 아이템의 이름 저장
  const [selectedManagerId, setSelectedManagerId] = useState<number>(); // 클릭한 아이템의 id 저장
  const user = useRecoilValue(authAtoms);
  const ownerId = user.userId; // 사장님 id
  const token = user.token; // 로그인 token

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
      top: "85%",
      left: "50%",
      transform: "translate(-50%, -50%)",
      borderRadius: "1.563vw",
      boxShadow: "0.104vw 0.104vw 0.104vw rgba(0, 0, 0, 0.25)",
      backgroundColor: "white",
      padding: "2.344vw 0 1.042vw 0",
    },
  };

  // 매니저 리스트 가져오기 API
  useEffect(() => {
    const fetchData = async (id: number) => {
      try {
        const response = await axios.get<ManagerAPIResponse>(
          `/api/owner/managers/${id}`,
          {
            params: { isOldestOrders, page, pageSize, token, name },
            headers: { accept: "application/json" },
          }
        );
        setData(response.data.data);
        setTotalCount(response.data.totalCount);
      } catch (error) {
        console.error("데이터를 불러오는데 실패했습니다.", error);
      }
    };

    if (ownerId) fetchData(ownerId);
  }, [isOldestOrders, page, pageSize, name]); // isOldestOrders가 변경될 때마다 데이터 갱신

  // 승인 모달 open
  const openApproveModal = (name: string, id: number) => {
    setSelectedManagerName(name); // 클릭한 아이템의 이름 저장
    setSelectedManagerId(id); // 클릭한 아이템의 id 저장
    setIsApproveModalOpen(true);
  };

  // 승인 모달 내 확인 버튼 클릭 시 호출되는 함수
  const handleApproveClick = () => {
    if (selectedManagerId) {
      // 데이터 업데이트
      setData((prevData) =>
        prevData.map((manager) =>
          manager.id === selectedManagerId
            ? { ...manager, isAuth: true }
            : manager
        )
      );
      approveManager(selectedManagerId); // 승인 요청
      closeApproveModal(); // 모달 닫기
    }
  };

  // 승인 모달 close
  const closeApproveModal = () => setIsApproveModalOpen(false);

  // 취소 모달 open
  const openDenyModal = (name: string, id: number) => {
    setSelectedManagerName(name); // 클릭한 매니저의 이름 저장
    setSelectedManagerId(id); // 클릭한 매니저의 id 저장
    setIsDenyModalOpen(true);
  };

  // 취소 모달 내 확인 버튼 클릭 시 호출되는 함수
  const handleDenyClick = () => {
    if (selectedManagerId) {
      // 데이터 업데이트
      setData((prevData) =>
        prevData.map((manager) =>
          manager.id === selectedManagerId
            ? { ...manager, isAuth: false }
            : manager
        )
      );
      denyManager(selectedManagerId); // 거절 요청
      closeDenyModal(); // 모달 닫기
    }
  };

  // 취소 모달 close
  const closeDenyModal = () => setIsDenyModalOpen(false);

  // 매니저 승인 API
  const approveManager = async (id: number) => {
    try {
      const response = await axios.put(
        `/api/owner/manager/auth/${id}`,
        {}, // request body (빈 객체)
        {
          params: { token },
          headers: { accept: "application/json" },
        }
      );
      console.log(response);
    } catch (error) {
      console.error("매니저 승인 요청을 실패하였습니다.", error);
    }
  };

  // 매니저 취소 API
  const denyManager = async (id: number) => {
    try {
      const response = await axios.put(
        `/api/owner/manager/deny/${id}`,
        {}, // request body (빈 객체)
        {
          params: { token },
          headers: { accept: "application/json" },
        }
      );
    } catch (error) {
      console.error("매니저 취소 요청을 실패하였습니다.", error);
    }
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
              <td className={styles.text_left}>{index + 1}</td>
              <td className={styles.text_left}>{item.name}</td>
              <td className={styles.text_left}>{item.username}</td>
              <td className={styles.text_left}>{item.phoneNumber}</td>
              <td className={styles.text_left}>{item.date}</td>
              <td className={styles.text_center}>
                {item.isAuth ? "Yes" : "No"}
              </td>
              <td className={styles.text_center}>
                <ApproveButton
                  isApprove={item.isAuth}
                  onClick={() => openApproveModal(item.name, item.id)}
                />
              </td>
              <td className={styles.text_center}>
                <DenyButton
                  isApprove={item.isAuth}
                  onClick={() => openDenyModal(item.name, item.id)}
                />
              </td>
              <td className={styles.td_right_black}></td>
            </tr>
          ))}
        </tbody>
      </table>
      <Pagination
        page={page}
        pageSize={pageSize}
        totalCount={totalCount}
        onPageChange={setPage} // 페이지 변경 시 호출
        onPageSizeChange={setPageSize} // 페이지 사이즈 변경 시 호출
      />
      <Modal
        isOpen={isApproveModalOpen}
        onRequestClose={closeApproveModal}
        contentLabel="승인 확인 모달"
        style={customModalStyles}
        ariaHideApp={false}
      >
        <p
          className={styles.modal_text_1}
        >{`"${selectedManagerName}" 님을 승인하시겠습니까?`}</p>
        <div className={styles.modal_button_box}>
          <button
            className={styles.modal_blue_button}
            onClick={handleApproveClick}
          >
            확인
          </button>
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
        >{`"${selectedManagerName}" 님을 취소하시겠습니까?`}</p>
        <div className={styles.modal_button_box}>
          <button
            className={styles.modal_blue_button}
            onClick={handleDenyClick}
          >
            확인
          </button>
          <button className={styles.modal_gray_button} onClick={closeDenyModal}>
            취소
          </button>
        </div>
      </Modal>
    </div>
  );
};

export default ManagerApproveTable;
