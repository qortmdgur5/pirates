import styles from "./styles/login.module.scss";
import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { useRecoilValue } from "recoil";
import { userAtom } from "../../../atoms/userAtoms";
import pirates_logo from "../../../assets/image/pirates_logo_img.png";
import kakao_button from "../../../assets/image/kakao_login_button.png";

function Login() {
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();
  const user = useRecoilValue(userAtom);

  useEffect(() => {
    if (user?.id) {
      // userInfo가 배열인지 확인하고, 배열이 비어있지 않은지 확인
      if (
        !user.userInfo ||
        !Array.isArray(user.userInfo) ||
        user.userInfo.length === 0
      ) {
        navigate("/user/signup");
      } else {
        navigate("/user/party");
      }
    }
  }, [user, navigate]);

  // 카카오 로그인 진행
  const handleLogin = () => {
    setLoading(true); // 로그인 중 상태로 설정
    // 백엔드 로그인 엔드포인트로 리디렉션
    window.location.href = "/api/user/auth/kakao/login?id=64";
  };

  return (
    <div className={styles.container}>
      <div className={styles.container_contents}>
        <div className={styles.logo_text_box}>
          <p className={styles.logo_text_1}>해적</p>
          <p className={styles.logo_text_2}>Pirates</p>
          <p className={styles.logo_text_3}>게스트 하우스 정보가 한눈에!</p>
        </div>
        <div className={styles.logo_box}>
          <img src={pirates_logo} alt="main_logo" />
        </div>
        <p className={styles.login_text_1}>
          회원 서비스 이용을 위해 로그인 해주세요.
        </p>
        <div className={styles.sns_login_box}>
          <button
            className={styles.kakao_login_button}
            onClick={handleLogin}
            disabled={loading}
          >
            <img src={kakao_button} alt="kakao_login_img" />
            <span>{loading ? "로그인 중..." : "카카오 로그인"}</span>
          </button>
        </div>
      </div>
    </div>
  );
}

export default Login;
