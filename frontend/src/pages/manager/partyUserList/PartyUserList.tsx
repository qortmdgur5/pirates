import { useLocation, useNavigate } from "react-router-dom";
import BackButton from "../../../components/common/backButton/BackButton";
import HomeButton from "../../../components/common/homeButton/HomeButton";
import HouseNameAndDate from "../../../components/common/houseNameAndDate/HouseNameAndDate";
import TeamDropDown from "../../../components/common/teamDropDown/TeamDropDown";
import UserListCard from "./components/UserListCard";
import styles from "./styles/partyUserList.module.scss";
import { useRecoilValue } from "recoil";
import { accomoAtoms, authAtoms } from "../../../atoms/authAtoms";
import { useEffect, useState } from "react";

interface UserPartyInfo {
  id: number; // User 테이블 Primary key
  name: string; // 유저 이름
  gender: boolean; // true: 남자, false: 여자
  team: number | null; // 팀 번호 (nullable)
  partyOn: boolean; // 파티 실시간 참석여부
}

function PartyUserList() {
  const { state } = useLocation();
  const partyId = state.partyId;
  const partyDate = state.partyDate;
  const maxTeam = state.team;
  const [partyUsers, setPartyUsers] = useState<UserPartyInfo[]>([]);
  const accomodation = useRecoilValue(accomoAtoms);
  const manager = useRecoilValue(authAtoms);
  const guestHouseName = accomodation.accomodation_name;
  const navigate = useNavigate();

  useEffect(() => {
    async function fetchPartyUsers() {
      try {
        if (!manager) {
          alert("로그인을 진행해주세요.");
          navigate("/manager/login");
          return;
        }

        if (!partyId) {
          navigate(`/manager/manageParty`);
          return;
        }

        const response = await fetch(`/api/manager/partyInfo/${partyId}`);
        if (!response.ok) {
          throw new Error("데이터를 가져오는 데 실패했습니다.");
        }

        const responseData = await response.json();
        const data: UserPartyInfo[] = responseData.data;
        setPartyUsers(data);
      } catch (error) {
        console.error("API 호출 에러:", error);
        alert("참여자 정보를 불러오는 데 실패했습니다.");
      }
    }

    fetchPartyUsers();
  }, [manager, navigate]);

  const groupByTeam = (
    users: UserPartyInfo[]
  ): Map<string | number, UserPartyInfo[]> => {
    // 그룹화
    const grouped = users.reduce((acc, user) => {
      const teamKey = user.team ?? "미지정";
      if (!acc.has(teamKey)) acc.set(teamKey, []);
      acc.get(teamKey)?.push(user);
      return acc;
    }, new Map<string | number, UserPartyInfo[]>());

    // 키 정렬
    const sortedEntries = Array.from(grouped.entries()).sort(
      ([keyA], [keyB]) => {
        if (keyA === "미지정") return -1; // "미지정"은 항상 맨 앞
        if (keyB === "미지정") return 1; // "미지정"은 항상 맨 앞
        return Number(keyA) - Number(keyB); // 숫자는 오름차순 정렬
      }
    );

    return new Map(sortedEntries);
  };

  const groupedUsers = groupByTeam(partyUsers);

  // 팀 변경 처리 함수
  const handleTeamChange = (userId: number, newTeam: number | null) => {
    setPartyUsers((prevUsers) =>
      prevUsers.map((user) =>
        user.id === userId ? { ...user, team: newTeam } : user
      )
    );
  };

  return (
    <div className={styles.container}>
      <div className={styles.container_contents}>
        <HouseNameAndDate guestHouseName={guestHouseName} date={partyDate} />
        <button className={styles.love_matching_button} type="button">
          ❤️ 짝매칭
        </button>
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
        <button className={styles.team_assign_button} type="button">
          조 배정
        </button>
        <div className={styles.user_list_box}>
          {groupedUsers.size > 0 ? (
            Array.from(groupedUsers.entries()).map(([team, users]) => (
              <div key={team} className={styles.team_section}>
                <TeamDropDown
                  team={team === "미지정" ? "미지정" : `${team}조`}
                />
                {users.map((user) => (
                  <UserListCard
                    key={user.id}
                    id={user.id}
                    team={user.team}
                    userName={user.name}
                    gender={user.gender}
                    partyOn={true}
                    maxTeam={maxTeam != null ? maxTeam : null}
                    onTeamChange={handleTeamChange} // 팀 변경 핸들러 전달
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
