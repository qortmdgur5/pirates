import styles from "./styles/backButton.module.scss";
import { useNavigate } from "react-router-dom";

// Props 타입 정의 (TypeScript 사용 시)
interface BackButtonProps {
  navigateTo: string; // 이동할 주소
}

function BackButton({ navigateTo }: BackButtonProps) {
  const navigate = useNavigate();

  const handleBackClick = () => {
    navigate(navigateTo); // props로 받은 주소로 이동
  };

  return (
    <button
      type="button"
      className={styles.container}
      onClick={handleBackClick}
    >
      <div className={styles.back_img_box}>
        <img src="/src/assets/image/back.png" alt="back_button_img" />
      </div>
      <p className={styles.back_text}>BACK</p>
    </button>
  );
}

export default BackButton;
