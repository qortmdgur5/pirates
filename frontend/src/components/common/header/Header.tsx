import { useSetRecoilState } from "recoil";
import styles from "./styles/header.module.scss";
import { useNavigate } from "react-router-dom";
import { accomoAtoms, authAtoms } from "../../../atoms/authAtoms";

function Header() {
  const setUser = useSetRecoilState(authAtoms);
  const setAccomodation = useSetRecoilState(accomoAtoms);
  const navigate = useNavigate(); // useNavigate 훅 사용

  // 로그아웃 처리 함수
  const handleLogout = () => {
    // Recoil 상태를 초기화하여 로그인 정보 삭제
    setUser({
      role: null,
      token: null,
      userId: null,
      username: null,
    });

    setAccomodation({
      accomodation_id: null,
      accomodation_name: null,
    });

    // 인덱스 페이지로 리디렉션
    navigate("/manager/login"); // '/'는 인덱스 페이지를 의미합니다.
  };

  return (
    <header className={styles.container}>
      <div className={styles.header_logo_box}>
        <div className={styles.header_logo_img_box}>
          <img src="/src/assets/image/pirates_logo_img.png" alt="logo_img" />
        </div>
        <p className={styles.header_logo_box_text}>해적</p>
      </div>
      <button className={styles.logout_button} onClick={handleLogout}>
        로그아웃
        <img src="/src/assets/image/logout_button.png" alt="logout_img" />
      </button>
    </header>
  );
}

export default Header;
