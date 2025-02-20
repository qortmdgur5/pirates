import { useLocation, useNavigate } from "react-router-dom";
import BackButton from "../../../components/common/backButton/BackButton";
import HomeButton from "../../../components/common/homeButton/HomeButton";
import HouseNameAndDate from "../../../components/common/houseNameAndDate/HouseNameAndDate";
import TeamDropDown from "../../../components/common/teamDropDown/TeamDropDown";
import UserListCard from "./components/UserListCard";
import styles from "./styles/partyUserList.module.scss";
import { useEffect, useState } from "react";
import axios from "axios";
import { useRecoilValue } from "recoil";
import { userAtom } from "../../../atoms/userAtoms";
import glasses from "../../../assets/image/glasses.png";

// API 응답 타입 정의
interface UserPartyInfo {
  id: number; // User 테이블 Primary key
  name: string; // 유저 이름
  gender: boolean; // true: 남자, false: 여자
  team: number | null; // 팀 번호 (nullable)
  chatRoomId: number | null; // 서로의 채팅방 번호
}

function PartyUserList() {
  const location = useLocation();
  const { guestHouseName } = location.state || {}; // /user/party 페이지에서 useNavigate state 로 데이터 추출
  const [partyUsers, setPartyUsers] = useState<UserPartyInfo[]>([]);
  const user = useRecoilValue(userAtom); // userAtom에서 현재 로그인된 사용자 정보 가져오기
  const userId = user?.id || null;
  const partyId = user?.party_id || null;
  const token = user?.token;
  const navigate = useNavigate();

  // 각 팀의 토글 상태 관리 (팀마다 열기/닫기 상태를 저장)
  const [teamVisibility, setTeamVisibility] = useState<
    Map<string | number, boolean>
  >(new Map());

  useEffect(() => {
    async function fetchPartyUsers() {
      try {
        if (!user || !partyId) return; // 유저 로그인 정보, partyId 없으면 대기

        // 1. 첫 번째 API 호출 (파티 참여자 목록)
        const { data: partyResponse } = await axios.get(
          `/api/user/partyInfo/${partyId}`,
          {
            params: { token },
          }
        );
        const partyUsers: UserPartyInfo[] = partyResponse.data;

        // 2. 두 번째 API 호출 (현재 사용자와 이미 채팅방이 있는 유저 목록)
        const { data: chatResponse } = await axios.get(
          `/api/user/partyInfo/chatExist/${partyId}/${user.id}`,
          {
            params: { token },
          }
        );
        const chatUsers: { id: number; chatRoom_id: number }[] =
          chatResponse.data;

        // 3. 서로 채팅중인 유저들의 정보를 Map 으로 저장 (빠른검색 위해)
        const chatUserMap = new Map(
          chatUsers.map((chatUser) => [chatUser.id, chatUser.chatRoom_id])
        );

        // 4. 모든 유저 정보를 저장 (채팅방 여부 추가)
        const usersWithChatInfo = partyUsers.map((partyUser) => ({
          ...partyUser,
          chatRoomId: chatUserMap.get(partyUser.id) || null, // 채팅방이 서로 존재하면 ID 추가 없으면 null
        }));

        setPartyUsers(usersWithChatInfo);
      } catch (error) {
        console.error("API 호출 에러:", error);
        alert("참여자 정보를 불러오는 데 실패했습니다.");
      }
    }

    fetchPartyUsers();
  }, [user, navigate]);

  // 유저 리스트 팀으로 그룹화
  const groupByTeam = (
    users: UserPartyInfo[]
  ): Map<string | number, UserPartyInfo[]> => {
    if (!users) return new Map(); // 유저 데이터가 없다면 빈 맵 반환
    const grouped = users.reduce((acc, user) => {
      const teamKey = user.team ?? "미지정";
      if (!acc.has(teamKey)) acc.set(teamKey, []);
      acc.get(teamKey)?.push(user);
      return acc;
    }, new Map<string | number, UserPartyInfo[]>());

    const sortedEntries = Array.from(grouped.entries()).sort(
      ([keyA], [keyB]) => {
        if (keyA === "미지정") return -1;
        if (keyB === "미지정") return 1;
        return Number(keyA) - Number(keyB);
      }
    );

    return new Map(sortedEntries);
  };

  const groupedUsers = groupByTeam(partyUsers);

  useEffect(() => {
    // groupedUsers가 변경될 때만 팀을 열려있는 상태로 설정
    if (groupedUsers.size > 0) {
      // 초기화 된 상태라면, setTeamVisibility를 한 번만 호출
      groupedUsers.forEach((_, team) => {
        setTeamVisibility((prev) => {
          // 이미 해당 팀이 있으면 상태 업데이트를 하지 않음
          if (!prev.has(team)) {
            return new Map(prev).set(team, true);
          }
          return prev;
        });
      });
    }
  }, [groupedUsers]); // groupedUsers가 변경될 때만 실행

  const toggleTeamVisibility = (team: string | number) => {
    setTeamVisibility((prev) => new Map(prev).set(team, !prev.get(team)));
  };

  return (
    <div className={styles.container}>
      <div className={styles.container_contents}>
        <HouseNameAndDate guestHouseName={guestHouseName || "게스트 하우스"} />
        <div className={styles.home_and_back_box}>
          <HomeButton />
          <BackButton navigateTo="/user/party" />
        </div>
        <div className={styles.search_and_participant_box}>
          <div className={styles.search_box}>
            <input
              className={styles.name_input}
              type="text"
              placeholder="검색"
            />
            <img src={glasses} alt="search_icon_img" />
          </div>
          <div className={styles.participant_box}>
            <p className={styles.participant_text}>참여자수</p>
            <p className={styles.participant_status}>
              {partyUsers?.length || 0}
            </p>
          </div>
        </div>
        <div className={styles.user_list_box}>
          {groupedUsers.size > 0 ? (
            Array.from(groupedUsers.entries()).map(([team, users]) => (
              <div key={team} className={styles.team_section}>
                <TeamDropDown
                  team={team === "미지정" ? "미지정" : `${team}조`}
                  onClick={() => toggleTeamVisibility(team)} // 클릭 시 토글
                />
                {teamVisibility.get(team) && // 토글된 상태가 true일 때만 보여줌
                  users.map((user) => (
                    <UserListCard
                      key={user.id}
                      id={user.id}
                      team={user.team}
                      userName={user.name}
                      gender={user.gender}
                      chatRoomId={user.chatRoomId}
                      userId={userId}
                      partyId={partyId}
                    />
                  ))}
              </div>
            ))
          ) : (
            <p
              style={{
                display: "flex",
                alignItems: "center",
                justifyContent: "center",
                fontSize: "26px",
              }}
            >
              참여자가 없습니다.
            </p>
          )}
        </div>
      </div>
    </div>
  );
}

export default PartyUserList;
