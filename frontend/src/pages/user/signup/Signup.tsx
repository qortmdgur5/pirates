import { useState, ChangeEvent, useEffect } from "react";
import { useRecoilValue } from "recoil";
import { userAtom } from "../../../atoms/userAtoms";
import RadioButton from "../../../components/common/radio/RadioButton";
import styles from "./styles/signup.module.scss";
import { useNavigate } from "react-router-dom";

// 타입 정의
interface SignupFormData {
  name: string;
  phone: string;
  email: string;
  job: string;
  age: number | null;
  mbti: string;
  region: string;
  gender: boolean;
}

function Signup() {
  // 초기 상태 정의
  const initialFormData: SignupFormData = {
    name: "",
    phone: "",
    email: "",
    job: "",
    age: null,
    mbti: "",
    region: "",
    gender: true,
  };

  const [formData, setFormData] = useState<SignupFormData>(initialFormData);

  // Recoil에서 userAtom 상태 가져오기
  const user = useRecoilValue(userAtom);

  // useNavigate 훅 초기화
  const navigate = useNavigate();

  // 페이지 진입 시 user_id가 없으면 = 로그인 하지 않은 유저라면
  useEffect(() => {
    if (!user?.id) {
      alert("로그인을 진행하여야 합니다.");
      navigate("/"); // 홈으로 이동
    }
  }, [user?.id, navigate]);

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

  // 상태 업데이트 함수
  const handleInputChange = (
    e: ChangeEvent<HTMLInputElement | HTMLSelectElement>
  ) => {
    const { name, value } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]: value,
    }));
  };

  const handleGenderChange = (value: boolean) => {
    setFormData((prev) => ({
      ...prev,
      gender: value,
    }));
  };

  const handleSignup = async () => {
    const { name, phone, email, age, region, mbti, gender } = formData;

    if (
      !name ||
      !phone ||
      !email ||
      !age ||
      !region ||
      !mbti ||
      gender === null
    ) {
      alert("모든 필드를 입력해주세요.");
      return;
    }

    const payload = {
      user_id: user?.id, // Recoil 상태에서 가져온 ID
      ...formData,
    };

    try {
      const response = await fetch("/api/user/signup", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(payload),
      });

      if (!response.ok) {
        throw new Error("회원가입에 실패했습니다.");
      }

      const result = await response.json();
      alert("회원가입이 완료되었습니다.");
    } catch (error) {
      console.error(error);
      alert("오류가 발생했습니다. 다시 시도해주세요.");
    }
  };

  // 옵션 렌더링 함수
  const renderOptions = (options: string[]) =>
    options.map((option) => (
      <option key={option} value={option}>
        {option}
      </option>
    ));

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
          {[
            {
              label: "이름",
              name: "name",
              type: "text",
              placeholder: "이름 입력",
            },
            {
              label: "핸드폰번호",
              name: "phone",
              type: "text",
              placeholder: "010xxxxxxxx",
            },
            {
              label: "이메일",
              name: "email",
              type: "text",
              placeholder: "example@naver.com",
            },
            {
              label: "직업",
              name: "job",
              type: "text",
              placeholder: "회사원, 학생 ...",
            },
            {
              label: "나이",
              name: "age",
              type: "text",
              placeholder: "나이 입력",
            },
          ].map(({ label, name, type, placeholder }) => (
            <div className={styles.signup_input_line} key={name}>
              <label className={styles.signup_input_label}>{label}</label>
              <div className={styles.signup_input_input_area}>
                <input
                  type={type}
                  name={name}
                  placeholder={placeholder}
                  value={formData.name}
                  onChange={handleInputChange}
                />
              </div>
            </div>
          ))}
          <div className={styles.signup_input_line}>
            <label className={styles.signup_input_label}>성별</label>
            <div className={styles.signup_input_input_area}>
              <div className={styles.radio_box}>
                <RadioButton
                  label="남성"
                  name="genderMan"
                  value={true}
                  checked={formData.gender === true}
                  onChange={handleGenderChange}
                />
                <RadioButton
                  label="여성"
                  name="genderWoman"
                  value={false}
                  checked={formData.gender === false}
                  onChange={handleGenderChange}
                />
              </div>
            </div>
          </div>
          <div className={styles.signup_input_line}>
            <label className={styles.signup_input_label}>MBTI</label>
            <div className={styles.signup_input_input_area}>
              <select
                name="mbti"
                id="mbti"
                value={formData.mbti}
                onChange={handleInputChange}
              >
                {renderOptions(mbtiList)}
              </select>
            </div>
          </div>
          <div className={styles.signup_input_line}>
            <label className={styles.signup_input_label}>지역</label>
            <div className={styles.signup_input_input_area}>
              <select
                name="region"
                id="region"
                value={formData.region}
                onChange={handleInputChange}
              >
                {renderOptions(regions)}
              </select>
            </div>
          </div>
        </div>
        <div className={styles.signup_box_container}>
          <button
            className={styles.signup_button}
            type="button"
            onClick={handleSignup}
          >
            가입하기
          </button>
          <button className={styles.cancel_button} type="button">
            가입취소
          </button>
        </div>
      </div>
    </div>
  );
}

export default Signup;
