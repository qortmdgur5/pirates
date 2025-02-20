import { useLocation } from "react-router-dom";
import BackButton from "../../../components/common/backButton/BackButton";
import HomeButton from "../../../components/common/homeButton/HomeButton";
import HouseNameAndDate from "../../../components/common/houseNameAndDate/HouseNameAndDate";
import TeamDropDown from "../../../components/common/teamDropDown/TeamDropDown";
import UserListCard from "./components/UserListCard";
import styles from "./styles/partyUserList.module.scss";
import { useRecoilValue } from "recoil";
import { accomoAtoms, authAtoms } from "../../../atoms/authAtoms";
import { useEffect, useState } from "react";
import axios from "axios";
import dayjs from "dayjs";
import glasses from "../../../assets/image/glasses.png";

interface UserPartyInfo {
  id: number; // User 테이블 Primary key
  name: string; // 유저 이름
  gender: boolean; // true: 남자, false: 여자
  team: number | null; // 팀 번호 (nullable)
  partyOn: boolean | null; // 파티 실시간 참석여부
}

function PartyUserList() {
  const { state } = useLocation();
  const partyId = state.id;
  const partyDate = state.partyDate;
  const maxTeam = state.team;
  const [partyUsers, setPartyUsers] = useState<UserPartyInfo[]>([]);
  const [originalUsers, setOriginalUsers] = useState<UserPartyInfo[]>([]); // 원본 데이터 저장
  const accomodation = useRecoilValue(accomoAtoms);
  const user = useRecoilValue(authAtoms);
  const token = user.token;
  const guestHouseName = accomodation.accomodation_name;
  const [remainingTime, setRemainingTime] = useState<number | null>(null); // 짝매칭 남은 시간
  const [matchStatus, setMatchStatus] = useState<
    "notStarted" | "inProgress" | "finished"
  >("notStarted"); // 짝매칭 상태

  // 유저 리스트 가져오기 API
  useEffect(() => {
    const fetchPartyUsers = async () => {
      try {
        const response = await axios.get(`/api/manager/partyInfo/${partyId}`, {
          params: { token },
        });
        const data: UserPartyInfo[] = response.data.data;

        setPartyUsers(data);
        setOriginalUsers(data); // 원본 데이터 초기화
      } catch (error) {
        console.error("API 호출 에러:", error);
        alert("참여자 정보를 불러오는 데 실패했습니다.");
      }
    };

    const fetchMatchStartTime = async () => {
      try {
        const response = await axios.get(
          `/api/manager/party/matchTime/${partyId}`,
          {
            headers: { Accept: "application/json" },
            params: { token },
          }
        );
        const startTime = response.data.data.matchStartTime;
        if (startTime) {
          setMatchStatus("inProgress");
          const endTime = dayjs(startTime).add(2, "minute");
          updateRemainingTime(endTime);
        }
      } catch (error) {
        console.log("짝매칭 시간 가져오기 오류 :", error);
      }
    };

    fetchPartyUsers();
    fetchMatchStartTime();
  }, [user]);

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

  // 팀 변경 Change 함수
  const handleTeamChange = (
    userId: number,
    newTeam: number | null,
    partyOn: boolean | null
  ) => {
    setPartyUsers((prevUsers) =>
      prevUsers.map((user) =>
        user.id === userId ? { ...user, team: newTeam, partyOn: partyOn } : user
      )
    );
  };

  // 변경된 사용자 데이터 필터링
  const getChangedUsers = () => {
    return partyUsers.filter(
      (user) =>
        originalUsers.find((orig) => orig.id === user.id)?.team !== user.team
    );
  };

  // 변경 사항 저장 API 호출
  const handleSaveChanges = async () => {
    const changedUsers = getChangedUsers();
    if (changedUsers.length === 0) {
      alert("변경된 데이터가 없습니다.");
      return;
    }

    try {
      const payload = {
        data: changedUsers.map(({ id, team }) => ({ id, team })),
      };
      await axios.put(`/api/manager/partyUserInfo`, payload, {
        params: { token },
      });
      alert("변경 사항이 저장되었습니다.");
      setOriginalUsers(partyUsers); // 원본 데이터 동기화
    } catch (error) {
      console.error("저장 중 오류 발생:", error);
      alert("저장 중 문제가 발생했습니다.");
    }
  };

  // 짝매칭 타이머 함수
  const updateRemainingTime = (endTime: dayjs.Dayjs) => {
    const interval = setInterval(() => {
      const now = dayjs();
      const diff = endTime.diff(now, "second");
      if (diff <= 0) {
        clearInterval(interval);
        setMatchStatus("finished");
        setRemainingTime(null);
      } else {
        setRemainingTime(diff);
      }
    }, 1000);
  };

  const matchStart = async () => {
    if (matchStatus === "inProgress" || matchStatus === "finished") return;
    const isConfirmed = window.confirm("짝매칭을 시작하시겠습니까?");
    if (!isConfirmed) return;

    try {
      await axios.put(
        `/api/manager/party/matchStart/${partyId}`,
        {},
        { params: { token } }
      );
      setMatchStatus("inProgress");
      const endTime = dayjs().add(2, "minute");
      updateRemainingTime(endTime);
    } catch (error) {
      console.log("짝매칭 시작 오류: ", error);
    }
  };

  // 시간 디스플레이 텍스트 표시
  const displayTime =
    matchStatus === "finished"
      ? "❤️ 매칭끝"
      : matchStatus === "inProgress" && remainingTime !== null
      ? `⏳ ${dayjs.duration(remainingTime, "seconds").format("mm:ss")}`
      : "❤️ 짝매칭";

  return (
    <div className={styles.container}>
      <div className={styles.container_contents}>
        <HouseNameAndDate guestHouseName={guestHouseName} date={partyDate} />
        <button
          className={styles.love_matching_button}
          type="button"
          onClick={matchStart}
        >
          {displayTime}
        </button>
        <div className={styles.home_and_back_box}>
          <HomeButton />
          <BackButton navigateTo="/manager/managePartyDetail" state={state} />
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
        <button
          className={styles.team_assign_button}
          type="button"
          onClick={handleSaveChanges} // 변경 사항 저장 버튼
        >
          조 변경
        </button>
        <div className={styles.user_list_box}>
          {groupedUsers.size > 0 ? (
            Array.from(groupedUsers.entries()).map(([team, users]) => (
              <div key={team} className={styles.team_section}>
                <TeamDropDown
                  team={team === "미지정" ? "미지정" : `${team}조`}
                  onClick={() => {}} // 조 접엇다 폇다 토글 함수 추후
                />
                {users.map((user) => (
                  <UserListCard
                    key={user.id}
                    id={user.id}
                    team={user.team}
                    userName={user.name}
                    gender={user.gender}
                    partyOn={user.partyOn}
                    maxTeam={maxTeam != null ? maxTeam : null}
                    onTeamChange={handleTeamChange} // 팀 변경 핸들러 전달
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
