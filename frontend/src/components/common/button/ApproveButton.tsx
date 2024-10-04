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

function ApproveButton({ isApprove }: ApproveInterface) {
  return (
    <ApproveButtonBox>
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
  );
}

export default ApproveButton;
