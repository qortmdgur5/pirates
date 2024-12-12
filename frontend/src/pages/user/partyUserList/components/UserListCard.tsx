import styles from "./styles/userListCard.module.scss";

interface UserListCardProps {
  team: number | null; // 팀 번호 또는 null
  userName: string; // 유저 이름
  gender: boolean; // true: 남자, false: 여자
}

function UserListCard({ team, userName, gender }: UserListCardProps) {
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
      <button className={styles.chat_button} type="button">
        채팅
      </button>
    </div>
  );
}

export default UserListCard;
