import { useState } from "react";
import styles from "./styles/userListCard.module.scss";
import axios from "axios";
import { useRecoilValue } from "recoil";
import { authAtoms } from "../../../../atoms/authAtoms";

interface UserListCardProps {
  id: number;
  team: number | null; // 팀 번호 또는 null
  userName: string; // 유저 이름
  gender: boolean; // true: 남자, false: 여자
  maxTeam: number | null; // 최대 팀
  partyOn: boolean; // 파티 실시간 참석 여부
  onTeamChange: (userId: number, newTeam: number | null) => void; // 팀 변경 처리 함수
}

function UserListCard({
  id,
  team,
  userName,
  gender,
  maxTeam,
  partyOn: initialPartyOn,
  onTeamChange,
}: UserListCardProps) {
  // 팀 상태 및 파티 참석 상태 관리
  const [selectedTeam, setSelectedTeam] = useState<number | null>(team);
  const [partyOn, setPartyOn] = useState<boolean>(initialPartyOn);
  const user = useRecoilValue(authAtoms);
  const token = user.token;

  const handleTeamChange = (event: React.ChangeEvent<HTMLSelectElement>) => {
    const newTeam = event.target.value;
    const newTeamValue = newTeam === "없음" ? null : parseInt(newTeam, 10);

    setSelectedTeam(newTeamValue);
    onTeamChange(id, newTeamValue); // 팀 변경 처리
  };

  const handlePartyToggle = async () => {
    const newPartyOnState = !partyOn;

    try {
      // 서버에 PUT 요청
      await axios.put(`/api/manager/partyUserOn/${id}`, null, {
        params: { partyOn: newPartyOnState, token },
      });

      // 요청 성공 시 상태 업데이트
      setPartyOn(newPartyOnState);
    } catch (error) {
      console.error("Error updating partyOn state:", error);
      alert("파티 상태 변경 중 문제가 발생했습니다.");
    }
  };

  const renderOptions = () => {
    const options = [];
    if (team === null) {
      // 미지정 조일 경우 "없음" 옵션을 표시
      options.push(
        <option key="없음" value="">
          없음
        </option>
      );
    }

    if (maxTeam === null) {
      return options; // maxTeam이 null일 경우 "없음" 옵션만 렌더링
    }

    // maxTeam이 존재할 경우, 1조부터 maxTeam까지의 팀 번호 옵션을 렌더링
    for (let index = 1; index <= maxTeam; index++) {
      // 미지정 조일 경우에도 다른 조를 선택할 수 있도록 함
      options.push(
        <option key={index} value={index}>
          {index}조
        </option>
      );
    }

    return options;
  };

  return (
    <div className={styles.container}>
      <div className={styles.user_img_box}>
        <img
          src={`/src/assets/image/${gender ? "man" : "woman"}_icon_img.png`}
          alt={`${gender ? "man" : "woman"}_icon_img`}
        />
      </div>
      <div className={styles.team_and_name_box}>
        {team === null ? (
          <p className={styles.team_and_name_text}>{userName}</p>
        ) : (
          <p className={styles.team_and_name_text}>
            {team}조 {userName}
          </p>
        )}
        <div className={styles.gender_img_box}>
          <img
            src={`/src/assets/image/gender_${gender ? "man" : "woman"}.png`}
            alt={`gender_${gender ? "man" : "woman"}_img`}
          />
        </div>
      </div>
      <div className={styles.team_select_box}>
        <select
          className={styles.team_select}
          value={selectedTeam === null ? "없음" : selectedTeam}
          onChange={handleTeamChange}
        >
          {renderOptions()}
        </select>
      </div>
      <button
        className={`${styles.on_off_button} ${
          partyOn ? styles.party_on : styles.party_off
        }`}
        type="button"
        onClick={handlePartyToggle} // 버튼 클릭 시 상태 변경
      >
        {partyOn ? "ON" : "OFF"}
      </button>
    </div>
  );
}

export default UserListCard;
