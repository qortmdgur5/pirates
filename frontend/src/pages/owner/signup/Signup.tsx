import styles from "./styles/Signup.module.scss";

function Signup() {
  return (
    <>
      <div className={styles.container}>
        <div className={styles.signup_container}>
          <div className={styles.logo_box}>
            <div className={styles.logo_img_box}>
              <img
                src="/src/assets/image/pirates_logo_img.png"
                alt="logo_img"
              />
            </div>
            <p className={styles.logo_box_text}>해적</p>
          </div>
          <p className={styles.signup_text_1}>회원가입</p>
          <p className={styles.signup_text_2}>
            회원정보는 개인정보취급방침에 따라 안전하게 보호되며 회원님의 명확한
            동의 없이 공개 또는 제 3자에게 제공되지 않습니다.
          </p>
          <div className={styles.signup_input_box}>
            <div className={styles.signup_input_line}>
              <label className={styles.signup_input_label}>아이디</label>
              <div className={styles.signup_input_id_input_area}>
                <input type="text" placeholder="아이디 입력(6~20자)" />
                <button className={styles.duplicate_button}>중복확인</button>
              </div>
            </div>
            <p className={styles.danger_message}>
              * 사용할 수 없는 아이디입니다.
            </p>
            <div className={styles.signup_input_line}>
              <label className={styles.signup_input_label}>비밀번호</label>
              <div className={styles.signup_input_input_area}>
                <input type="password" placeholder="비밀번호 입력 (문자,숫자,특수문자 포함 6~20자)" />
              </div>
            </div>
            <div className={styles.signup_input_line}>
              <label className={styles.signup_input_label}>비밀번호 확인</label>
              <div className={styles.signup_input_input_area}>
                <input type="text" placeholder="비밀번호 재입력" />
              </div>
            </div>
            <div className={styles.signup_input_line}>
              <label className={styles.signup_input_label}>이름</label>
              <div className={styles.signup_input_input_area}>
                <input type="text" placeholder="이름을 입력해주세요." />
              </div>
            </div>
            <div className={styles.signup_input_line}>
              <label className={styles.signup_input_label}>게스트하우스</label>
              <div className={styles.signup_input_input_area}>
                <input type="text" placeholder="게스트하우스 이름을 입력해주세요." />
              </div>
            </div>
            <div className={styles.signup_input_line}>
              <label className={styles.signup_input_label}>전화번호</label>
              <div className={styles.signup_input_input_area}>
                <input type="text" placeholder="전화번호를 입력해주세요." />
              </div>
            </div>
            <div className={styles.signup_input_line}>
              <label className={styles.signup_input_label}>이메일</label>
              <div className={styles.signup_input_email_input_area}>
                <input type="text" />
                <p>@</p>
                <select name="domain" id="domain">
                  <option value="naver.com">naver.com</option>
                  <option value="google.com">google.com</option>
                  <option value="naver.com">naver.com</option>
                </select>
              </div>
            </div>
            <div className={styles.signup_input_line}>
              <label className={styles.signup_input_label}>주소</label>
              <div className={styles.signup_input_input_area}>
                <input type="text" placeholder="게스트하우스 주소를 입력해주세요." />
              </div>
            </div>
            <div className={styles.signup_input_line}>
              <label className={styles.signup_input_label}>생년월일</label>
              <div className={styles.signup_input_birth_input_area}>
                <select name="year" id="year">
                  <option value="1994">1994</option>
                  <option value="1995">1995</option>
                  <option value="1996">1996</option>
                </select>
                <p>년</p>
                <select name="month" id="month">
                  <option value="8">8</option>
                  <option value="9">9</option>
                  <option value="10">10</option>
                </select>
                <p>월</p>
                <select name="day" id="day">
                  <option value="1">1</option>
                  <option value="2">2</option>
                  <option value="3">3</option>
                </select>
                <p>일</p>
              </div>
            </div>
          </div>
          <div className={styles.signup_button_box}>
            <button className={styles.signup_button}>가입하기</button>
            <button className={styles.cancel_button}>가입취소</button>
          </div>
        </div>
      </div>
    </>
  );
}

export default Signup;
