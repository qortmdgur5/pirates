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
  onClick: () => void; // 클릭 핸들러 타입 정의
}

function DenyButton({ onClick }: DenyButtonInterface) {
  return (
    <DenyButtonBox onClick={onClick}>
      <img src="/src/assets/image/denyButton.png" alt="denyButton_img" />
    </DenyButtonBox>
  );
}

export default DenyButton;
