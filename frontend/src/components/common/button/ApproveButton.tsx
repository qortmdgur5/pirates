import { useState } from "react";
import Modal from "react-modal";
import styled from "styled-components";

interface ApproveInterface {
  isApprove: boolean;
}

const ApproveButtonBox = styled.button`
  display: flex;
  justify-content: center;
  align-items: center;
  width: 100%;
  height: 100%;
  background-color: transparent;

  img {
    width: 50px;
  }
`;

const customModalStyles: ReactModal.Styles = {
  overlay: {
    backgroundColor: " rgba(0, 0, 0, 0.4)",
    width: "100%",
    height: "100vh",
    zIndex: "10",
    position: "fixed",
    top: "0",
    left: "0",
  },
  content: {
    width: "360px",
    height: "180px",
    zIndex: "150",
    position: "absolute",
    top: "50%",
    left: "50%",
    transform: "translate(-50%, -50%)",
    borderRadius: "10px",
    boxShadow: "2px 2px 2px rgba(0, 0, 0, 0.25)",
    backgroundColor: "white",
    justifyContent: "center",
    overflow: "auto",
  },
};

Modal.setAppElement("#root"); // 앱의 최상위 요소를 설정

function ApproveButton({ isApprove }: ApproveInterface) {
  const [isModalOpen, setIsModalOpen] = useState(false);

  const openModal = () => setIsModalOpen(true);
  const closeModal = () => setIsModalOpen(false);

  const handleApprove = () => {
    // 승인 처리 로직 (예: 서버로 데이터 전송 등)
    console.log("승인 처리 완료");
    closeModal(); // 모달 닫기
  };

  return (
    <>
      <ApproveButtonBox onClick={openModal} disabled={isApprove}>
        {isApprove ? (
          <img
            src="/src/assets/image/approvedButton.png"
            alt="approvedButton_img"
          />
        ) : (
          <img
            src="/src/assets/image/approveButton.png"
            alt="approveButton_img"
          />
        )}
      </ApproveButtonBox>

      {/* 모달 컴포넌트 */}
      <Modal
        isOpen={isModalOpen}
        onRequestClose={closeModal}
        contentLabel="승인 확인 모달"
        style={customModalStyles}
        ariaHideApp={false}
      >
        <h2>승인하시겠습니까?</h2>
        <button onClick={handleApprove}>승인</button>
        <button onClick={closeModal}>취소</button>
      </Modal>
    </>
  );
}

export default ApproveButton;
