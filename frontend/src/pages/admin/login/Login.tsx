import styles from "./styles/login.module.scss";
import { useNavigation } from "../../../utils/navigation";
import { useEffect, useState } from "react";
import axios from "axios";
import { jwtDecode } from "jwt-decode";
import { authAtoms, accomoAtoms } from "../../../atoms/authAtoms";
import { useRecoilState } from "recoil";

interface DecodedToken {
  id: number | null;
  role: string | null;
}

function Login() {
  // 네비게이션 함수
  const navigation = useNavigation();

  // 상태관리 모음
  const [username, setUserName] = useState<string>(""); // 아이디 입력값 관리
  const [password, setPassword] = useState<string>(""); // 비밀번호 입력값 관리

  // 전역 상태관리 모음
  // Recoil 상태 훅
  const [authAtom, setAuthAtom] = useRecoilState(authAtoms); // 사용자 정보 상태

  // 아이디 입력창 관리
  const handleUserNameChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setUserName(e.target.value);
  };

  // 비밀번호 입력창 관리
  const handlePasswordChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setPassword(e.target.value);
  };

  // 로그인 처리
  const handleLogin = async () => {
    const data = new URLSearchParams();
    data.append("username", username); // 입력한 사용자명
    data.append("password", password); // 입력한 비밀번호
    try {
      const response = await axios.post(
        "http://61.73.191.42:19000/admin/login",
        data,
        {
          headers: {
            "Content-Type": "application/x-www-form-urlencoded",
            accept: "application/json",
          },
        }
      );
      const token = response.data.access_token; // 서버에서 반환한 토큰
      const decoded: DecodedToken = jwtDecode(token);
      console.log("디코딩된 토큰 정보:", decoded);

      const userRole = decoded.role;
      const userId = decoded.id;

      // Recoil 상태 업데이트
      setAuthAtom({
        userId: userId,
        role: userRole,
        token: token,
        username: null,
      }); // 사용자 정보 저장
      navigation("/admin/houseManage");
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
              <img
                src="/src/assets/image/pirates_logo_img.png"
                alt="pirates main image"
              />
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
              관리자가 아니라면 돌아가 주시기 바랍니다.
            </p>
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
          </div>
        </div>
      </div>
    </div>
  );
}

export default Login;
