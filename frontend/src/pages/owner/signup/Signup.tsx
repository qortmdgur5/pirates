import { useEffect, useState } from "react";
import TabsComponent from "../../../components/common/tabs/Tabs";
import styles from "./styles/Signup.module.scss";
import AutoComplete from "../../../components/common/autoComplete/AutoComplete";
import axios from "axios";

function Signup() {
  const [isOwner, setIsOwner] = useState<boolean>(true);
  const [onwerId, setOwnerId] = useState<number | undefined>(); // 매니저의 게스트하우스 리스트 owner_id 관리
  const [username, setUserName] = useState<string>(""); // 아이디 입력값 관리
  const [password, setPassword] = useState<string>("");
  const [confirmPassword, setConfirmPassword] = useState<string>("");
  const [name, setName] = useState<string>("");
  const [phoneNumber, setPhoneNumber] = useState<string>("");
  const [guesthouseList, setGuesthouseList] = useState<
    { id: number; label: string }[]
  >([]);
  const [hasFetched, setHasFetched] = useState<boolean>(false); // API 호출 여부를 확인하는 상태 추가
  const [isOwnerDuplication, setIsOwnerDuplication] = useState<boolean | null>(
    null
  ); // 사장님 중복 여부 상태
  const [isManagerDuplication, setIsManagerDuplication] = useState<
    boolean | null
  >(null); // 매니저 중복 여부 상태
  const [isPasswordValid, setIsPasswordValid] = useState<boolean | null>(null); // 비밀번호 유효성 검사 상태
  const [isPasswordMatch, setIsPasswordMatch] = useState<boolean | null>(null); // 비밀번호 일치 여부 상태

  // 비밀번호 유효성 검사 함수
  const validatePassword = (password: string) => {
    const passwordRegex =
      /^(?=.*[A-Za-z])(?=.*\d)(?=.*[!@#$%^&*])[A-Za-z\d!@#$%^&*]{6,20}$/;
    return passwordRegex.test(password);
  };

  useEffect(() => {
    // isOwner가 false로 변경되었을 때, 한 번만 API 호출
    if (!isOwner && !hasFetched) {
      axios
        .get("/api/manager/getAccomodation")
        .then((response) => {
          const formattedGuesthouses = response.data.data.map(
            (guesthouse: { owner_id: number; accomodationName: string }) => ({
              id: guesthouse.owner_id, // owner_id를 id로 변환
              label: guesthouse.accomodationName, // accomodationName을 label로 변환
            })
          );
          setGuesthouseList(formattedGuesthouses); // 변환된 데이터로 상태 업데이트
          setHasFetched(true); // 데이터를 받아오면 hasFetched를 true로 설정
        })
        .catch((error) => {
          console.error("API 호출 오류:", error);
        });
    }
  }, [isOwner, hasFetched]); // isOwner와 hasFetched가 변경될 때마다 실행

  const handleUserNameChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setUserName(e.target.value); // 아이디 입력값 관리
  };

  const handlePasswordChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setPassword(e.target.value);
  };

  const handlePasswordBlur = () => {
    setIsPasswordValid(validatePassword(password)); // 입력창 떠날 때 유효성 검사
  };

  const handleConfirmPasswordChange = (
    e: React.ChangeEvent<HTMLInputElement>
  ) => {
    setConfirmPassword(e.target.value);
    setIsPasswordMatch(e.target.value === password); // 입력할 때마다 비밀번호 일치 검사
  };

  const handleNameChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setName(e.target.value);
  };

  const handlePhoneNumberChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const input = e.target.value.replace(/\D/g, "").slice(0, 11); // 숫자만 허용하고 최대 길이 11로 제한
    setPhoneNumber(input);
  };

  // 중복검사
  const checkIdDuplication = () => {
    const apiUrl = isOwner ? "/api/owner/duplicate" : "/api/manager/duplicate";
    axios
      .post(apiUrl, null, {
        params: { username: username },
      })
      .then((response) => {
        if (response.data.duplicate) {
          // 중복된 경우 - 중복되면 false로 설정
          isOwner
            ? setIsOwnerDuplication(false)
            : setIsManagerDuplication(false);
        } else {
          // 중복되지 않은 경우 - 중복되지 않으면 true로 설정
          isOwner ? setIsOwnerDuplication(true) : setIsManagerDuplication(true);
        }
      })
      .catch((error) => {
        console.error("중복 검사 오류:", error);
      });
  };

  // 탭이 변경될 때 (사장님, 매니저 변경) 모든 입력 필드 초기화
  useEffect(() => {
    setUserName("");
    setPassword("");
    setConfirmPassword("");
    setName("");
    setPhoneNumber("");
    setOwnerId(undefined);
    setIsOwnerDuplication(null);
    setIsManagerDuplication(null);
    setIsPasswordValid(null);
    setIsPasswordMatch(null);
  }, [isOwner]);

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
          <TabsComponent tabs={["사장님", "매니저"]} setIsOwner={setIsOwner} />
          <div className={styles.signup_input_box}>
            <div className={styles.signup_input_line}>
              <label className={styles.signup_input_label}>아이디</label>
              <div className={styles.signup_input_id_input_area}>
                <input
                  type="text"
                  placeholder="아이디 입력(6~20자)"
                  value={username}
                  onChange={handleUserNameChange} // 아이디 변경시 상태 업데이트
                />
                <button
                  className={styles.duplicate_button}
                  onClick={checkIdDuplication} // 중복검사 실행
                >
                  중복확인
                </button>
              </div>
            </div>
            {isOwner ? (
              <>
                <p
                  className={styles.danger_message}
                  style={{
                    display: isOwnerDuplication === false ? "block" : "none",
                  }}
                >
                  * 중복된 아이디 입니다.
                </p>
                <p
                  className={styles.success_message}
                  style={{
                    display: isOwnerDuplication === true ? "block" : "none",
                  }}
                >
                  * 사용 가능한 아이디 입니다.
                </p>
              </>
            ) : (
              <>
                <p
                  className={styles.danger_message}
                  style={{
                    display: isManagerDuplication === false ? "block" : "none",
                  }}
                >
                  * 중복된 아이디 입니다.
                </p>
                <p
                  className={styles.success_message}
                  style={{
                    display: isManagerDuplication === true ? "block" : "none",
                  }}
                >
                  * 사용 가능한 아이디 입니다.
                </p>
              </>
            )}
            <div className={styles.signup_input_line}>
              <label className={styles.signup_input_label}>비밀번호</label>
              <div className={styles.signup_input_input_area}>
                <input
                  type="password"
                  placeholder="비밀번호 입력 (문자,숫자,특수문자 포함 6~20자)"
                  value={password}
                  onChange={handlePasswordChange}
                  onBlur={handlePasswordBlur} // 입력창 떠날 때 유효성 검사
                />
              </div>
            </div>
            <p
              className={styles.danger_message}
              style={{
                display: isPasswordValid === false ? "block" : "none",
              }}
            >
              * 유효하지 않은 비밀번호입니다.
            </p>
            <div className={styles.signup_input_line}>
              <label className={styles.signup_input_label}>비밀번호 확인</label>
              <div className={styles.signup_input_input_area}>
                <input
                  type="password"
                  placeholder="비밀번호 재입력"
                  value={confirmPassword}
                  onChange={handleConfirmPasswordChange}
                />
              </div>
            </div>
            <p
              className={
                isPasswordMatch ? styles.success_message : styles.danger_message
              }
              style={{
                display: isPasswordMatch !== null ? "block" : "none",
              }}
            >
              {isPasswordMatch
                ? "* 비밀번호가 일치합니다."
                : "* 비밀번호가 일치하지 않습니다."}
            </p>
            <div className={styles.signup_input_line}>
              <label className={styles.signup_input_label}>이름</label>
              <div className={styles.signup_input_input_area}>
                <input
                  type="text"
                  placeholder="이름을 입력해주세요."
                  value={name}
                  onChange={handleNameChange}
                />
              </div>
            </div>
            <div className={styles.signup_input_line}>
              <label className={styles.signup_input_label}>전화번호</label>
              <div className={styles.signup_input_input_area}>
                <input
                  type="text"
                  placeholder="ex) 01012345678"
                  value={phoneNumber}
                  onChange={handlePhoneNumberChange}
                />
              </div>
            </div>
            {!isOwner && (
              <>
                <div className={styles.signup_input_line}>
                  <label className={styles.signup_input_label}>
                    게스트하우스
                  </label>
                  <div className={styles.signup_input_input_area}>
                    <AutoComplete
                      options={guesthouseList}
                      setValue={setOwnerId}
                    />
                  </div>
                </div>
              </>
            )}
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
