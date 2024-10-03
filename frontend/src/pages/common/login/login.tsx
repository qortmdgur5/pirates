import Input from "../../../components/common/input/Input";
import styles from "./styles/login.module.scss";
import styled from "styled-components";

const RoundButton = styled.button<{ iconUrl: string }>`
  width: 90px;
  height: 90px;
  border-radius: 50%; /* 동그란 모양 */
  background-image: url(${(props) => props.iconUrl}); /* 이미지 설정 */
  background-size: cover; /* 이미지를 버튼 크기에 맞게 조절 */
  background-position: center; /* 이미지 위치 중앙 정렬 */
  border: none; /* 기본 버튼 스타일 제거 */
  cursor: pointer; /* 마우스 커서 스타일 */
  transition: transform 0.2s; /* 클릭할 때 애니메이션 효과 */

  &:hover {
    transform: scale(1.1); /* 호버 시 크기 확대 */
  }

  &:active {
    transform: scale(0.9); /* 클릭 시 크기 축소 */
  }
`;

function Login() {
  return (
    <div className={styles.container}>
      <div className={styles.login_box}>
        <div className={styles.login_box_left}>
          <div className={styles.login_box_left_inner}>
            <p className={styles.login_box_left_inner_text_1}>해적</p>
            <p className={styles.login_box_left_inner_text_2}>Pirates</p>
            <p className={styles.login_box_left_inner_text_3}>
              게스트 하우스 정보가 한눈에!
            </p>
            <div className={styles.login_box_left_inner_img_box}>
              <img
                src="/src/assets/image/pirates_logo_img.png"
                alt="pirates main image"
              />
            </div>
          </div>
        </div>
        <div className={styles.login_box_right}>
          <div className={styles.login_box_right_inner}>
            <p className={styles.login_box_right_inner_text_1}>안녕하세요.<br />해적입니다.</p>
            <p className={styles.login_box_right_inner_text_2}>회원 서비스 이용을 위해 로그인 해주세요.</p>
            <div className={styles.login_box_right_inner_input_box}>
              <Input placeholder="아이디 입력" type="text" />
              <Input placeholder="비밀번호 입력" type="password" />
              <button className={styles.login_box_right_inner_login_button}>로그인</button>
            </div>
            <div className={styles.login_box_right_inner_signup_box}>
              <p className={styles.login_box_right_inner_signup_text}>아직 회원이 아니신가요?</p>
              <button className={styles.login_box_right_inner_signup_button}>회원가입</button>
            </div>
            <div className={styles.login_box_right_inner_sns_text}>
              SNS 계정으로 로그인
            </div>
            <div className={styles.sns_login_button_box}>
              <RoundButton iconUrl="/src/assets/image/naver_login_button.png" />
              <RoundButton iconUrl="/src/assets/image/naver_login_button.png" />
              <RoundButton iconUrl="/src/assets/image/naver_login_button.png" />
              <RoundButton iconUrl="/src/assets/image/naver_login_button.png" />
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default Login;
