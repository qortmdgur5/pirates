import styled from "styled-components";

const InputComponents = styled.input`
  width: 100%;
  height: 84px;
  border-radius: 18px;
  font-size: 28px;
  color: #8c8c8c;
  border: 1px solid #c9c9c9;
  padding: 0 25px 0 25px;
`;

interface InputProps {
  placeholder: string;
  type: string;
}

function Input({ placeholder, type }: InputProps) {
  return <InputComponents placeholder={placeholder} type={type} />;
}

export default Input;
