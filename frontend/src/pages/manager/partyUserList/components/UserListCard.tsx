import { useState } from "react";
import styles from "./styles/userListCard.module.scss";

interface UserListCardProps {
  team: number | null; // 팀 번호 또는 null
  userName: string; // 유저 이름
  gender: boolean; // true: 남자, false: 여자
  maxTeam: number | null; // 최대 팀
}

function UserListCard({ team, userName, gender, maxTeam }: UserListCardProps) {
  // 팀 상태 관리
  const [selectedTeam, setSelectedTeam] = useState<number | "없음" | null>(
    team ?? "없음"
  );

  const handleTeamChange = (event: React.ChangeEvent<HTMLSelectElement>) => {
    const newTeam = event.target.value;
    setSelectedTeam(newTeam === "없음" ? null : parseInt(newTeam, 10));
  };

  const renderOptions = () => {
    if (maxTeam === null) {
      return <option value="없음">없음</option>;
    } else if (typeof maxTeam === "number") {
      return Array.from({ length: maxTeam }, (_, index) => (
        <option key={index + 1} value={index + 1}>
          {index + 1}조
        </option>
      ));
    }
    return null;
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
        {/* team 값에 따라 초기값 설정 */}
        <select
          className={styles.team_select}
          value={selectedTeam === null ? "없음" : selectedTeam}
          onChange={handleTeamChange}
        >
          {renderOptions()}
        </select>
      </div>
      <button className={styles.on_off_button} type="button">
        ON
      </button>
    </div>
  );
}

export default UserListCard;
