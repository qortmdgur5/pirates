import styles from "./styles/userListCard.module.scss";

interface MatchUserListCardProps {
  id: number; // 해당 유저 id 값
  userName: string; // 유저 이름
  gender: boolean; // true: 남자, false: 여자
}

function UserListCard({ id, userName, gender }: MatchUserListCardProps) {
  return (
    <div className={styles.container}>
      <div className={styles.img_box}>
        <div className={styles.img_info}>
          <img
            src={
              gender
                ? "/src/assets/image/man_icon_img.png"
                : "/src/assets/image/woman_icon_img.png"
            }
            alt="user_img_png"
          />
        </div>
      </div>
      <div className={styles.name_and_gender_box}>
        <div className={styles.name_and_gender_info}>
          <p className={styles.name_text}>{userName}</p>
          <div className={styles.gender_box}>
            <img
              src={
                gender
                  ? "/src/assets/image/gender_man.png"
                  : "/src/assets/image/gender_woman.png"
              }
              alt="gender_img_png"
            />
          </div>
        </div>
      </div>
      <div className={styles.check_box}>
        <img src="/src/assets/image/check.png" alt="check_img" />
      </div>
      <div className={styles.rank_box}>
        <p className={styles.rank_text}>1</p>
      </div>
    </div>
  );
}

export default UserListCard;
