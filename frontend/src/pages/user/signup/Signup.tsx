import { useState } from "react";
import RadioButton from "../../../components/common/radio/RadioButton";
import styles from "./styles/signup.module.scss";

function Signup() {
  // 성별 선택 상태
  const [selectedOption, setSelectedOption] = useState(false);

  // 지역 및 MBTI 데이터
  const regions = [
    "서울",
    "부산",
    "대구",
    "인천",
    "광주",
    "대전",
    "울산",
    "세종",
    "경기",
    "강원",
    "충청북도",
    "충청남도",
    "전북",
    "전라",
    "경상북도",
    "경상남도",
    "제주도",
  ];
  const mbtiList = [
    "INTJ",
    "INTP",
    "ENTJ",
    "ENTP",
    "INFJ",
    "INFP",
    "ENFJ",
    "ENFP",
    "ISTJ",
    "ISFJ",
    "ESTJ",
    "ESFJ",
    "ISTP",
    "ISFP",
    "ESTP",
    "ESFP",
  ];

  // 지역, mbti option 컴포넌트 생성 함수
  const renderOptions = (options: string[]) =>
    options.map((option) => (
      <option key={option} value={option}>
        {option}
      </option>
    ));

  const handleRadioChange = (value: boolean) => {
    setSelectedOption(value);
  };

  return (
    <div className={styles.container}>
      <div className={styles.container_contents}>
        <div className={styles.logo_box}>
          <div className={styles.logo_img_box}>
            <img src="/src/assets/image/pirates_logo_img.png" alt="logo_img" />
          </div>
          <p className={styles.logo_box_text}>해적</p>
        </div>
        <p className={styles.signup_text_1}>회원가입</p>
        <p className={styles.signup_text_2}>
          회원정보는 개인정보취급방침에 따라 안전하게 보호되며 회원님의 명확한
          동의 없이 공개 또는 제 3자에게 제공되지 않습니다.
        </p>
        <div className={styles.input_container}>
          <div className={styles.signup_input_line}>
            <label className={styles.signup_input_label}>이름</label>
            <div className={styles.signup_input_input_area}>
              <input
                type="text"
                placeholder="이름 입력"
                // value={name}
                // onChange={handleNameChange}
              />
            </div>
          </div>
          <div className={styles.signup_input_line}>
            <label className={styles.signup_input_label}>핸드폰번호</label>
            <div className={styles.signup_input_phone_area}>
              <input
                type="text"
                placeholder="010xxxxxxxx"
                // value={phone}
                // onChange={handlePhoneChange}
              />
              <button className={styles.send_sms_button}>전송</button>
            </div>
          </div>
          <div className={styles.signup_input_line}>
            <div className={styles.signup_input_auth_area}>
              <input
                type="text"
                placeholder="인증번호 입력"
                // value={authNum}
                // onChange={handleAuthNumChange}
              />
              <button className={styles.phone_auth_button}>인증</button>
            </div>
          </div>
          <div className={styles.signup_input_line}>
            <label className={styles.signup_input_label}>이메일</label>
            <div className={styles.signup_input_input_area}>
              <input
                type="text"
                pattern="/^[a-zA-Z0-9.!#$%&'*+\/=?^_`{|}~-]+@[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(?:\.[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)*$/"
                placeholder="example@naver.com"
                // value={email}
                // onChange={handleEmailChange}
                // onBlur={handleEmaildBlur} // 입력창 떠날 때 유효성 검사
              />
            </div>
          </div>
          <div className={styles.signup_input_line}>
            <label className={styles.signup_input_label}>성별</label>
            <div className={styles.signup_input_input_area}>
              <div className={styles.radio_box}>
                <RadioButton
                  label="남성"
                  name="genderMan"
                  value={true}
                  checked={selectedOption === false}
                  onChange={handleRadioChange}
                />
                <RadioButton
                  label="여성"
                  name="genderWoman"
                  value={false}
                  checked={selectedOption === true}
                  onChange={handleRadioChange}
                />
              </div>
            </div>
          </div>
          <div className={styles.signup_input_line}>
            <label className={styles.signup_input_label}>직업</label>
            <div className={styles.signup_input_input_area}>
              <input
                type="text"
                placeholder="회사원, 학생 ..."
                // value={job}
                // onChange={handleJobChange}
              />
            </div>
          </div>
          <div className={styles.signup_input_line}>
            <label className={styles.signup_input_label}>나이</label>
            <div className={styles.signup_input_input_area}>
              <input
                type="text"
                placeholder="나이 입력"
                // value={age}
                // onChange={handleAgeChange}
              />
            </div>
          </div>
          <div className={styles.signup_input_line}>
            <label className={styles.signup_input_label}>MBTI</label>
            <div className={styles.signup_input_input_area}>
              <select name="mbti" id="mbti">
                {renderOptions(mbtiList)}
              </select>
            </div>
          </div>
          <div className={styles.signup_input_line}>
            <label className={styles.signup_input_label}>지역</label>
            <div className={styles.signup_input_input_area}>
              <select name="region" id="region">
                {renderOptions(regions)}
              </select>
            </div>
          </div>
        </div>
        <div className={styles.signup_box_container}>
          <button className={styles.signup_button} type="button">가입하기</button>
          <button className={styles.cancel_button} type="button">가입취소</button>
        </div>
      </div>
    </div>
  );
}

export default Signup;
