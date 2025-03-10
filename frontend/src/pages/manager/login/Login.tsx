import styles from "./styles/login.module.scss";
import TabsComponent from "../../../components/common/tabs/Tabs";
import { useEffect, useState } from "react";
import axios from "axios";
import { jwtDecode } from "jwt-decode";
import { authAtoms, accomoAtoms } from "../../../atoms/authAtoms";
import { useSetRecoilState } from "recoil";
import { useNavigate } from "react-router-dom";
import pirates_logo from "../../../assets/image/pirates_logo_img.png";

interface DecodedToken {
  role: string | null;
  sub: number | null;
  accommodation_id?: number | null;
}

function Login() {
  // 네비게이션 함수
  const navigation = useNavigate();

  // 상태관리 모음
  const [isOwner, setIsOwner] = useState<boolean>(true); // 매니저 사장님 상태 관리
  const [username, setUserName] = useState<string>(""); // 아이디 입력값 관리
  const [password, setPassword] = useState<string>(""); // 비밀번호 입력값 관리

  // 전역 상태관리 모음
  // Recoil 상태 훅
  const setAuthAtom = useSetRecoilState(authAtoms); // 매니저 or 사장님 로그인 상태
  const setAccomoAtom = useSetRecoilState(accomoAtoms); // 숙소 정보 상태

  // 아이디 입력창 관리
  const handleUserNameChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setUserName(e.target.value);
  };

  // 비밀번호 입력창 관리
  const handlePasswordChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setPassword(e.target.value);
  };

  // 탭이 변경될 때 (사장님, 매니저 변경) 모든 입력 필드 초기화
  useEffect(() => {
    setUserName("");
    setPassword("");
  }, [isOwner]);

  // 회원가입 처리
  const handleLogin = async () => {
    const data = new URLSearchParams();
    data.append("username", username); // 입력한 사용자명
    data.append("password", password); // 입력한 비밀번호

    const apiUrl = isOwner ? "/api/owner/login" : "/api/manager/login";

    try {
      const response = await axios.post(apiUrl, data, {
        headers: {
          "Content-Type": "application/x-www-form-urlencoded",
          accept: "application/json",
        },
      });
      const token = response.data.access_token; // 서버에서 반환한 토큰
      const decoded: DecodedToken = jwtDecode(token);
      const userRole = decoded.role;
      const userId = decoded.sub ?? null;
      const accommodationId = decoded.accommodation_id || null;

      // Recoil 상태 업데이트
      setAuthAtom({
        userId: userId,
        role: userRole,
        token: token,
        username: username,
      }); // 사용자 정보 저장
      setAccomoAtom({
        accomodation_id: accommodationId,
        accomodation_name: null,
      }); // 숙소 ID 저장

      isOwner
        ? navigation("/owner/manageHouse")
        : navigation("/manager/manageParty");
    } catch (error) {
      console.error("로그인 오류:", error);
      alert("로그인 정보가 올바르지 않습니다.");
    }
  };

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
              <img src={pirates_logo} alt="pirates main image" />
            </div>
          </div>
        </div>
        <div className={styles.login_box_right}>
          <div className={styles.login_box_right_inner}>
            <p className={styles.login_box_right_inner_text_1}>
              안녕하세요.
              <br />
              해적입니다.
            </p>
            <p className={styles.login_box_right_inner_text_2}>
              회원 서비스 이용을 위해 로그인 해주세요.
            </p>
            <TabsComponent
              tabs={["사장님", "매니저"]}
              setIsOwner={setIsOwner}
            />
            <div className={styles.login_box_right_inner_input_box}>
              <input
                type="text"
                placeholder="아이디 입력"
                value={username}
                onChange={handleUserNameChange}
              />
              <input
                type="password"
                placeholder="비밀번호 입력"
                value={password}
                onChange={handlePasswordChange}
              />
              <button
                className={styles.login_box_right_inner_login_button}
                onClick={handleLogin}
              >
                로그인
              </button>
            </div>
            <div className={styles.login_box_right_inner_signup_box}>
              <p className={styles.login_box_right_inner_signup_text}>
                아직 회원이 아니신가요?
              </p>
              <button
                className={styles.login_box_right_inner_signup_button}
                onClick={() => navigation("/manager/signup")}
              >
                회원가입
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default Login;
