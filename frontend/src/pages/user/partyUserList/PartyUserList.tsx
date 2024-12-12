import { useLocation, useNavigate } from "react-router-dom";
import BackButton from "../../../components/common/backButton/BackButton";
import HomeButton from "../../../components/common/homeButton/HomeButton";
import HouseNameAndDate from "../../../components/common/houseNameAndDate/HouseNameAndDate";
import TeamDropDown from "../../../components/common/teamDropDown/TeamDropDown";
import UserListCard from "./components/UserListCard";
import styles from "./styles/partyUserList.module.scss";
import { useEffect, useState } from "react";
import { useRecoilValue } from "recoil";
import { userAtom } from "../../../atoms/userAtoms";

// API 응답 타입 정의
interface UserPartyInfo {
  id: number; // User 테이블 Primary key
  name: string; // 유저 이름
  gender: boolean; // true: 남자, false: 여자
  team: number | null; // 팀 번호 (nullable)
}

function PartyUserList() {
  const location = useLocation();
  const { guestHouseName } = location.state || {}; // state에서 데이터 추출
  const [partyUsers, setPartyUsers] = useState<UserPartyInfo[]>([]);
  const user = useRecoilValue(userAtom); // userAtom에서 현재 로그인된 사용자 정보 가져오기
  const navigate = useNavigate();

  useEffect(() => {
    async function fetchPartyUsers() {
      try {
        if (!user) {
          alert("로그인을 진행해주세요.");
          navigate("/");
          return;
        }

        const partyId = user.party_id;
        if (!partyId) {
          navigate(`/user/party/${user.token}`);
          return;
        }

        const response = await fetch(`/user/partyInfo/${partyId}`);
        if (!response.ok) {
          throw new Error("데이터를 가져오는 데 실패했습니다.");
        }

        const data: UserPartyInfo[] = await response.json();
        setPartyUsers(data);
      } catch (error) {
        console.error("API 호출 에러:", error);
        alert("참여자 정보를 불러오는 데 실패했습니다.");
      }
    }

    fetchPartyUsers();
  }, [user, navigate]);

  // 팀별로 유저를 그룹화하는 함수
  const groupByTeam = (users: UserPartyInfo[]) => {
    return users.reduce((acc, user) => {
      const teamKey = user.team ?? "미지정";
      if (!acc[teamKey]) acc[teamKey] = [];
      acc[teamKey].push(user);
      return acc;
    }, {} as Record<string | number, UserPartyInfo[]>);
  };

  const groupedUsers = groupByTeam(partyUsers);

  return (
    <div className={styles.container}>
      <div className={styles.container_contents}>
        <HouseNameAndDate guestHouseName={guestHouseName} />
        <div className={styles.home_and_back_box}>
          <HomeButton />
          <BackButton />
        </div>
        <div className={styles.search_and_participant_box}>
          <div className={styles.search_box}>
            <input
              className={styles.name_input}
              type="text"
              placeholder="검색"
            />
            <img src="/src/assets/image/glasses.png" alt="search_icon_img" />
          </div>
          <div className={styles.participant_box}>
            <p className={styles.participant_text}>참여자수</p>
            <p className={styles.participant_status}>{partyUsers.length}</p>
          </div>
        </div>
        <div className={styles.user_list_box}>
          {Object.keys(groupedUsers).length > 0 ? (
            Object.entries(groupedUsers).map(([team, users]) => (
              <div key={team} className={styles.team_section}>
                <TeamDropDown
                  team={team === "미지정" ? "미지정" : `${team}조`}
                />
                {users.map((user) => (
                  <UserListCard
                    key={user.id}
                    team={user.team}
                    userName={user.name}
                    gender={user.gender}
                  />
                ))}
              </div>
            ))
          ) : (
            <p>참여자가 없습니다.</p>
          )}
        </div>
      </div>
    </div>
  );
}

export default PartyUserList;
