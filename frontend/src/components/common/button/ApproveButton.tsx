import styled from "styled-components";

interface ApproveInterface {
  isApprove: boolean;
  onClick: () => void;
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

function ApproveButton({ isApprove, onClick }: ApproveInterface) {
  return (
    <>
      <ApproveButtonBox onClick={onClick} disabled={isApprove}>
        <img
          src={`/src/assets/image/${
            isApprove ? "approvedButton.png" : "approveButton.png"
          }`}
          alt="approve_button"
        />
      </ApproveButtonBox>
    </>
  );
}

export default ApproveButton;
