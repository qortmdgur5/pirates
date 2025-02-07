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
  const [matchStatus, setMatchStatus] = useState<
    "notStarted" | "inProgress" | "finished"
  >("notStarted"); // 짝매칭 상태
  const [endTime, setEndTime] = useState<dayjs.Dayjs | null>(null); // 짝매칭 종료 시간
  const user = useSessionUser();
  const userId = user?.id; // 본인 id

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

    const interval = setInterval(updateTimer, 1000); // 1초마다 카운트 갱신

    return () => clearInterval(interval); // cleanup 함수
  }, [matchStartTime, endTime]);

  // 시간이 0 이하로 떨어지면 "끝" 표시
  const displayTime =
    matchStatus === "finished"
      ? "끝"
      : `${Math.floor(remainingTime! / 60)
          .toString()
          .padStart(2, "0")}:${(remainingTime! % 60)
          .toString()
          .padStart(2, "0")}`;

  const getMatchUserList = async () => {
    try {
      const response = await axios.post("/api/user/match/userList", {
        user_id: user?.id,
        party_id: user?.party_id,
      });
      const data = response.data.data;
      setUserList(data);
      setTeam(data[0].team);
    } catch (err) {
      console.log("짝매칭 유저 리스트 가져오기 실패:", err);
    }
  };

  useEffect(() => {
    // if (matchStatus !== "inProgress") return; // 짝매칭 진행중 아니면 대기
    getMatchUserList();
  }, [matchStatus]);

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
            {userList.map((user) => (
              <UserListCard
                key={user.id}
                id={user.id}
                userName={user.name}
                gender={user.gender}
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
