import { useLocation } from "react-router-dom";
import BackButton from "../../../components/common/backButton/BackButton";
import HomeButton from "../../../components/common/homeButton/HomeButton";
import HouseNameAndDate from "../../../components/common/houseNameAndDate/HouseNameAndDate";
import UserListCard from "./components/UserListCard";
import styles from "./styles/loveSelect.module.scss";
import dayjs from "dayjs";
import duration from "dayjs/plugin/duration";
import { useEffect, useState } from "react";
import useSessionUser from "../../hook/useSessionUser";
import axios from "axios";

dayjs.extend(duration);

interface UserListProps {
  id: number; // 해당 유저 id 값
  team: number | null; // 팀 번호 또는 null
  name: string; // 유저 이름
  gender: boolean; // true: 남자, false: 여자
}

function LoveSelect() {
  const location = useLocation();
  const { houseName, matchStartTime } = location.state || {};
  const [userList, setUserList] = useState<UserListProps[]>([]); // 짝 매칭 같은 조 유저 리스트
  const [team, setTeam] = useState<number | null>(null);
  const [remainingTime, setRemainingTime] = useState<number | null>(null); // 남은 시간
  const [endTime, setEndTime] = useState<dayjs.Dayjs | null>(null); // 짝매칭 종료 시간
  const [selectedUserId, setSelectedUserId] = useState<number | null>(null); // 선택한 유저 ID
  const [confirm, setConfirm] = useState<boolean>(false);
  const user = useSessionUser();
  const userId = user?.id || null; // 본인 id
  const partyId = user?.party_id || null; // 파티 id
  const [matchStatus, setMatchStatus] = useState<
    "notStarted" | "inProgress" | "finished"
  >("notStarted"); // 짝매칭 상태

  useEffect(() => {
    if (!matchStartTime) return; // matchStartTime이 없으면 종료

    const startTime = dayjs(matchStartTime);

    // 첫 렌더링 시에만 종료 시간을 설정
    if (!endTime) {
      setEndTime(startTime.add(5, "minute")); // 5분 뒤를 종료 시간으로 설정
    }

    const updateTimer = () => {
      const now = dayjs();

      if (now.isBefore(startTime)) {
        // 아직 시작 전
        setMatchStatus("notStarted");
      } else if (endTime && now.isBefore(endTime)) {
        // 진행 중
        setMatchStatus("inProgress");
        setRemainingTime(endTime.diff(now, "second"));
      } else {
        // 종료됨
        setMatchStatus("finished");
        setRemainingTime(null);
      }
    };

    updateTimer();
    const interval = setInterval(updateTimer, 1000); // 1초마다 카운트 갱신

    return () => clearInterval(interval); // cleanup 함수
  }, [matchStartTime, endTime]);

  // 시간이 0 이하로 떨어지면 "끝" 표시
  const displayTime =
    matchStatus === "finished"
      ? "끝"
      : remainingTime !== null
      ? `${String(Math.floor(remainingTime / 60)).padStart(2, "0")}:${String(
          remainingTime % 60
        ).padStart(2, "0")}`
      : "--:--";

  const getMatchUserList = async () => {
    try {
      const response = await axios.post("/api/user/match/userList", {
        user_id: user?.id,
        party_id: user?.party_id,
      });
      const data = response.data.data;
      setUserList(data);
      setTeam(data[0].team || "X");
    } catch (err) {
      console.log("짝매칭 유저 리스트 가져오기 실패:", err);
    }
  };

  useEffect(() => {
    // if (matchStatus !== "inProgress") return; // 짝매칭 진행중 아니면 대기
    getMatchUserList();
  }, [matchStatus]);

  // 본인의 gender 값을 userList에서 찾기
  const userGender = userList.find((user) => user.id === userId)?.gender;

  // 필터링된 유저 리스트 -> 자신 제외 && 동성 제외
  const filteredUserList = userList.filter(
    (user) => user.id !== userId && user.gender !== userGender
  );

  // 이미 선택한 상대방 데이터 가져오기
  const getConfirmUser = async () => {
    try {
      const response = await axios.get(
        `/api/user/match/confirm/${partyId}/${userId}`
      );
      const confirmedUserId = response.data.user_id_2;
      if (confirmedUserId) {
        setSelectedUserId(confirmedUserId);
        setConfirm(true); // 이미 확정된 경우 confirm을 true로 설정
      }
    } catch (err) {
      console.log("선택한 상대방 데이터 가져오기 에러:", err);
    }
  };

  useEffect(() => {
    if (userId && partyId && matchStatus === "inProgress") {
      getConfirmUser(); // 페이지가 로드될 때 & 진행중일때 확인
    }
  }, [userId, partyId, matchStatus]);

  // matchStatus가 "notStarted"일 경우 대기 메시지 표시
  if (matchStatus === "notStarted") return <p>매칭 시작 대기 중...</p>;

  return (
    <div className={styles.container}>
      <div className={styles.container_contents}>
        <HouseNameAndDate guestHouseName={`${houseName} 짝매칭`} />
        <div className={styles.home_and_back_box}>
          <HomeButton />
          <BackButton navigateTo="/user/party" />
        </div>
        <div className={styles.team_and_time_box}>
          <p className={styles.team_text}>{team}조 짝 매칭</p>
          <p className={styles.time_box}>{displayTime}</p> {/* 시간 표시 */}
        </div>
        <div className={styles.love_select_container}>
          <div className={styles.info_intro_box}>
            <p className={styles.img_intro}>짝</p>
            <p className={styles.name_and_gender_intro}>이름 및 성별</p>
            <p className={styles.check_intro}>체크</p>
            <p className={styles.rank_intro}>확정</p>
          </div>
          <div className={styles.user_list_box}>
            {/* UserListCard 컴포넌트를 map으로 돌려 렌더링 */}
            {filteredUserList.map((user) => (
              <UserListCard
                key={user.id}
                id={user.id}
                userName={user.name}
                gender={user.gender}
                isChecked={user.id === selectedUserId} // 선택된 유저 ID 비교
                onSelect={() => setSelectedUserId(user.id)} // 유저 선택 시 selectedUserId 업데이트
                userId={userId}
                partyId={partyId}
                confirm={confirm}
                setConfirm={setConfirm}
              />
            ))}
          </div>
        </div>
        <div className={styles.love_match_container}></div>
      </div>
    </div>
  );
}

export default LoveSelect;
