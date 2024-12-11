import { useRecoilState } from "recoil";
import HomeButton from "../../../components/common/homeButton/HomeButton";
import HouseNameAndDate from "../../../components/common/houseNameAndDate/HouseNameAndDate";
import styles from "./styles/party.module.scss";
import { userAtom, UserInfo } from "../../../atoms/userAtoms";
import { useEffect } from "react";
import { jwtDecode } from "jwt-decode";
import { useNavigation } from "../../../utils/navigation";

function Party() {
  const [user, setUser] = useRecoilState(userAtom);
  const navigate = useNavigation(); // 네비게이션 함수 사용

  useEffect(() => {
    // 실제 JWT 토큰을 받아오는 로직을 작성해야 합니다.
    const jwt = "받아온 JWT 토큰"; // 여기를 실제로 가져온 JWT 토큰으로 바꿔야 합니다.

    try {
      const decodedUser = jwtDecode<{
        id: number;
        party_id: number | null;
        userInfo: UserInfo | null;
      }>(jwt);

      if (!decodedUser.id) {
        // id가 없으면 에러 처리
        alert("로그인을 진행해주세요.");
        navigate("/");
      }

      // user 상태 설정
      setUser({
        id: decodedUser.id,
        party_id: decodedUser.party_id,
        userInfo: decodedUser.userInfo,
      });

      // userInfo가 없으면 /user/signup으로 리다이렉트
      if (!decodedUser.userInfo) {
        navigate("/user/signup");
      }
    } catch (error) {
      console.error("JWT 디코딩 오류:", error);
      // 에러가 발생한 경우 적절한 처리 (예: 로그인 화면으로 리디렉션)
      navigate("/");
    }
  }, [setUser, navigate]); // navigate를 의존성 배열에 추가

  return (
    <div className={styles.container}>
      <div className={styles.container_contents}>
        <HouseNameAndDate guestHouseName={"솔 게스트 하우스"} />
        <HomeButton />
        <div className={styles.house_info_box}>
          <div className={styles.house_info_lane}>
            <div className={styles.house_info_left}>소개</div>
            <div className={styles.house_info_right}>
              즐거운 분위기의 게스트 하우스
            </div>
          </div>
          <div className={styles.house_info_lane}>
            <div className={styles.house_info_left}>주소</div>
            <div className={styles.house_info_right}>
              경기도 부천시 토브빈 베이커리
            </div>
          </div>
          <div className={styles.house_info_lane}>
            <div className={styles.house_info_left}>전화번호</div>
            <div className={styles.house_info_right}>010-2222-3333</div>
          </div>
          <div className={styles.house_info_lane}>
            <div className={styles.house_info_left}>평점</div>
            <div className={styles.house_info_right}>⭐ 4.56</div>
          </div>
          <div className={styles.house_info_lane}>
            <div className={styles.house_info_left}>짝 매칭 카운트</div>
            <div className={styles.house_info_right}>❤️ 100</div>
          </div>
        </div>
        <div className={styles.button_box}>
          <button className={styles.house_party_button} type="button">
            파티방
          </button>
          <button className={styles.personal_chat_button} type="button">
            개인 채팅방
          </button>
          <button className={styles.love_button} type="button">
            짝 매칭
          </button>
        </div>
      </div>
    </div>
  );
}

export default Party;
