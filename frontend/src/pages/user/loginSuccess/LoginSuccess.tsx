import { jwtDecode } from "jwt-decode";
import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { useRecoilState } from "recoil";
import { userAtom, UserInfo } from "../../../atoms/userAtoms";

function LoginSuccess() {
  const [user, setUser] = useRecoilState(userAtom);
  const [loading, setLoading] = useState<boolean>(true); // 로딩 상태 추가
  const navigate = useNavigate();

  useEffect(() => {
    // URL에서 access_token 파라미터를 추출
    const urlParams = new URLSearchParams(window.location.search);
    const access_token = urlParams.get("access_token"); // 'access_token'을 URL에서 가져옴

    if (!access_token) {
      alert("카카오 계정이 없습니다. 계정을 만들어주세요.");
      navigate("/"); // 홈으로 리디렉션
      return;
    }

    try {
      // 디코딩 후 첫 번째 요소 접근
      const decodedData = jwtDecode<any>(access_token);
      const decodedUser = decodedData.data[0]; // 'data' 배열의 첫 번째 요소에 접근

      if (!decodedUser.id) {
        // id가 없으면 에러 처리
        alert("로그인을 진행해주세요.");
        return;
      }

      // user 상태 설정
      const userData = {
        token: access_token,
        id: decodedUser.id,
        role: decodedUser.role,
        party_id: decodedUser.party_id,
        userInfo: decodedUser.userInfo,
      };

      // user Recoil 상태 설정
      setUser(userData);

      // 로컬 스토리지에 사용자 데이터 저장
      sessionStorage.setItem("user", JSON.stringify(userData));

      // userInfo가 없으면 /user/signup으로 있으면 /user/party 페이지로 리다이렉트
      if (!decodedUser.userInfo || decodedUser.userInfo.length === 0) {
        navigate("/user/signup");
      } else {
        navigate("/user/party");
      }
    } catch (error) {
      console.error("JWT 디코딩 오류:", error);
      // 에러가 발생한 경우 적절한 처리 (예: 로그인 화면으로 리디렉션)
      alert("로그인에 문제가 생겼습니다. 관리자에게 문의해 주세요.");
      navigate("/");
    } finally {
      setLoading(false); // 로딩 상태 종료
    }
  }, [setUser, navigate]);

  return <div>{loading ? "로그인 중..." : "로그인 성공"}</div>;
}

export default LoginSuccess;
