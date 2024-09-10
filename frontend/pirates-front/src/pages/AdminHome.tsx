import styled from "styled-components";

const WrapperContainer = styled.div`
  width: 100%;
  padding: 15px;
`;

const Wrapper = styled.div`
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 15px;
  width: 100%;
  height: 600px;
  border-radius: 15px;
  border: 2px solid #eae4dd;
  padding: 15px;
`;

const AdminBox1 = styled.div`
  flex: 1;
  height: 100%;
  border-radius: 15px;
  border: 2px solid #eae4dd;
`;

const AdminBox2 = styled.div`
  flex: 5;
  height: 100%;
  border-radius: 15px;
  border: 2px solid #eae4dd;
`;

function AdminHome() {
  return (
    <WrapperContainer>
      <Wrapper>
        <AdminBox1></AdminBox1>
        <AdminBox2></AdminBox2>
      </Wrapper>
    </WrapperContainer>
  );
}

export default AdminHome;
