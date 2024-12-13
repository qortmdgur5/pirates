import styles from "./styles/login.module.scss";
import { useState } from "react";

function Login() {
  const [loading, setLoading] = useState(false);

  // 카카오 로그인 버튼 클릭 시 API 호출 - api 호출로 하면 안됨 url 로 리다이렉트 바로 연결시켜줘야 하기에 일단 주석
  // const handleLogin = async () => {
  //   try {
  //     setLoading(true);

  //     // 카카오 로그인 API 호출
  //     const response = await fetch("http://localhost:9000/user/auth/kakao/login/1", {
  //       method: "GET",
  //       headers: {
  //         "Content-Type": "application/json",
  //       },
  //     });

  //     if (response.ok) {
  //       console.log("로그인 성공");
  //       // 추가적인 응답 처리 로직이 필요하면 이곳에서 처리
  //     } else {
  //       alert("로그인에 실패했습니다.");
  //     }
  //   } catch (error) {
  //     console.error("로그인 중 오류 발생:", error);
  //     alert("로그인 중 오류가 발생했습니다.");
  //   } finally {
  //     setLoading(false);
  //   }
  // };
  // 카카오 로그인 버튼 클릭 시 리디렉션
  const handleLogin = () => {
    // 백엔드 로그인 엔드포인트로 리디렉션
    window.location.href = "http://localhost:9000/user/auth/kakao/login?id=1";
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
          <img src="/src/assets/image/pirates_logo_img.png" alt="main_logo" />
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
            <img
              src="/src/assets/image/kakao_login_button.png"
              alt="kakao_login_img"
            />
            <span>{loading ? "로그인 중..." : "카카오 로그인"}</span>
          </button>
        </div>
      </div>
    </div>
  );
}

export default Login;
