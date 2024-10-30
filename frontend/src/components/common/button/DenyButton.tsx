import styled from "styled-components";

const DenyButtonBox = styled.button`
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

interface DenyButtonInterface {
  isApprove: boolean;
  onClick: () => void;
}

function DenyButton({ isApprove, onClick }: DenyButtonInterface) {
  return (
    <DenyButtonBox onClick={onClick} disabled={!isApprove}>
      <img src="/src/assets/image/denyButton.png" alt="denyButton_img" />
    </DenyButtonBox>
  );
}

export default DenyButton;
