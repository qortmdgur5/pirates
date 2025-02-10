import styles from "./styles/matchListCard.module.scss";

// 타입 정의
interface MatchUser {
  user_id: number;
  phone: string;
  team: number;
  name: string;
}

interface MatchPairProps {
  man: MatchUser;
  woman: MatchUser;
}

interface MatchListCardProps {
  match: MatchPairProps;
}

function MatListCard({ match }: MatchListCardProps) {
  return (
    <div className={styles.container}>
      <div className={styles.match_box}>
        <div className={styles.man_box}>
          <div className={styles.man_img_box}>
            <img src="/src/assets/image/man_icon_img.png" alt="man_img" />
          </div>
          <div className={styles.name_and_gender_box}>
            <p className={styles.name_info}>{match.man.team} 조 {match.man.name}</p>
            <div className={styles.gender_box}>
              <img
                src="/src/assets/image/gender_man.png"
                alt="gender_img_png"
              />
            </div>
          </div>
        </div>
        <div className={styles.love_img_box}>
          <img src="/src/assets/image/loveMatch.png" alt="loveMatch_img" />
        </div>
        <div className={styles.woman_box}>
          <div className={styles.woman_img_box}>
            <img src="/src/assets/image/woman_icon_img.png" alt="woman_img" />
          </div>
          <div className={styles.name_and_gender_box}>
          <p className={styles.name_info}>{match.woman.team} 조 {match.woman.name}</p>
            <div className={styles.gender_box}>
              <img
                src="/src/assets/image/gender_woman.png"
                alt="gender_img_png"
              />
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default MatListCard;
