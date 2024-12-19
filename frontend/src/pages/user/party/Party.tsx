import { useRecoilState } from "recoil";
import HomeButton from "../../../components/common/homeButton/HomeButton";
import HouseNameAndDate from "../../../components/common/houseNameAndDate/HouseNameAndDate";
import styles from "./styles/party.module.scss";
import { userAtom, UserInfo } from "../../../atoms/userAtoms";
import { useEffect, useState } from "react";
import { jwtDecode } from "jwt-decode";
import { useNavigation } from "../../../utils/navigation";
import axios from "axios"; // API 호출을 위한 axios 사용
import { useNavigate } from "react-router-dom";

// 파티 정보 타입 정의
interface PartyInfo {
  name: string; // 게스트 하우스 이름
  introduction: string; // 게스트 하우스 소개말
  address: string; // 게스트 하우스 주소
  number: string | null; // 게스트 하우스 전화번호
  phoneNumber: string | null; // 게스트 하우스 사장 전화번호
  score: number | null; // 게스트 하우스 평점
  loveCount: number | null; // 게스트 하우스 짝매칭 카운트
  party_on: boolean; // 파티 오픈 상태
}

function Party() {
  const [user, setUser] = useRecoilState(userAtom);
  const [partyInfo, setPartyInfo] = useState<PartyInfo | null>(null); // 파티 정보 상태 추가
  const [loading, setLoading] = useState<boolean>(true); // 로딩 상태 추가
  const [error, setError] = useState<string | null>(null); // 에러 상태 추가
  const navigate = useNavigation(); // 네비게이션 함수 사용
  const navigation = useNavigate();

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
        navigate("/"); // 홈으로 이동
        return;
      }

      // user 상태 설정
      setUser({
        token: jwt,
        id: decodedUser.id,
        party_id: decodedUser.party_id,
        userInfo: decodedUser.userInfo,
      });

      // userInfo가 없으면 /user/signup으로 리다이렉트
      if (!decodedUser.userInfo) {
        navigate("/user/signup");
      }

      // 파티 정보가 있다면 API 호출
      if (decodedUser.party_id !== null) {
        getPartyInfo(decodedUser.party_id);
      } else {
        setLoading(false); // 파티 ID가 없다면 로딩 종료
      }
    } catch (error) {
      console.error("JWT 디코딩 오류:", error);
      // 에러가 발생한 경우 적절한 처리 (예: 로그인 화면으로 리디렉션)
      navigate("/");
    }
  }, [setUser, navigate]);

  const getPartyInfo = async (partyId: number) => {
    try {
      const response = await axios.get(`/user/party/${partyId}`);
      setPartyInfo(response.data);
    } catch (err) {
      console.error("파티 정보 가져오기 오류:", err);
      setError("파티 정보를 불러오는 데 실패했습니다.");
    } finally {
      setLoading(false); // 로딩 상태 종료
    }
  };

  if (loading) {
    return <div>로딩 중...</div>; // 로딩 중 상태 표시
  }

  if (error) {
    return <div>{error}</div>; // 오류 표시
  }

  return (
    <div className={styles.container}>
      <div className={styles.container_contents}>
        <HouseNameAndDate
          guestHouseName={partyInfo ? partyInfo.name : "게스트 하우스"}
        />
        <HomeButton />
        {partyInfo ? (
          <>
            <div className={styles.house_info_box}>
              <div className={styles.house_info_lane}>
                <div className={styles.house_info_left}>소개</div>
                <div className={styles.house_info_right}>
                  {partyInfo.introduction}
                </div>
              </div>
              <div className={styles.house_info_lane}>
                <div className={styles.house_info_left}>주소</div>
                <div className={styles.house_info_right}>
                  {partyInfo.address}
                </div>
              </div>
              <div className={styles.house_info_lane}>
                <div className={styles.house_info_left}>전화번호</div>
                <div className={styles.house_info_right}>
                  {partyInfo.number}
                </div>
              </div>
              <div className={styles.house_info_lane}>
                <div className={styles.house_info_left}>사장님 전화번호</div>
                <div className={styles.house_info_right}>
                  {partyInfo.phoneNumber}
                </div>
              </div>
              <div className={styles.house_info_lane}>
                <div className={styles.house_info_left}>평점</div>
                <div className={styles.house_info_right}>
                  ⭐ {partyInfo.score}
                </div>
              </div>
              <div className={styles.house_info_lane}>
                <div className={styles.house_info_left}>짝 매칭 카운트</div>
                <div className={styles.house_info_right}>
                  ❤️ {partyInfo.loveCount}
                </div>
              </div>
            </div>
            <div className={styles.button_box}>
              <button
                className={styles.house_party_button}
                type="button"
                onClick={() =>
                  navigation(`/user/party/userList/${user?.party_id}`, {
                    state: { guestHouseName: partyInfo.name },
                  })
                }
              >
                파티방 참여
              </button>
              <button
                className={styles.personal_chat_button}
                type="button"
                onClick={() => navigation('/user/chatRooms')}
              >
                개인 채팅방
              </button>
              <button className={styles.love_button} type="button">
                짝 매칭
              </button>
            </div>
          </>
        ) : (
          <div className={styles.noPartyInfo}>
            <p>파티에 입장하셨다면 QR 을 찍어주시기 바랍니다.</p>
          </div>
        )}
      </div>
    </div>
  );
}

export default Party;
