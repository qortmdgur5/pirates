import styles from "./styles/login.module.scss";
import { useNavigation } from "../../../utils/navigation";

function Login() {
  // 네비게이션 함수
  const navigation = useNavigation();

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
          <button className={styles.kakao_login_button}>
            <img
              src="/src/assets/image/kakao_login_button.png"
              alt="kakao_login_img"
            />
            <span>카카오 로그인</span>
          </button>
        </div>
      </div>
    </div>
  );
}

export default Login;
