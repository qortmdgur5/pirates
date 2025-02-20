import styles from "./styles/matchListCard.module.scss";
import man_icon from "../../../../assets/image/man_icon_img.png";
import woman_icon from "../../../../assets/image/woman_icon_img.png";
import gender_man from "../../../../assets/image/gender_man.png";
import gender_woman from "../../../../assets/image/gender_woman.png";
import love_img from "../../../../assets/image/loveMatch.png";

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
            <img src={man_icon} alt="man_img" />
          </div>
          <div className={styles.name_and_gender_box}>
            <p className={styles.name_info}>
              {match.man.team} 조 {match.man.name}
            </p>
            <div className={styles.gender_box}>
              <img src={gender_man} alt="gender_img_png" />
            </div>
          </div>
        </div>
        <div className={styles.love_img_box}>
          <img src={love_img} alt="loveMatch_img" />
        </div>
        <div className={styles.woman_box}>
          <div className={styles.woman_img_box}>
            <img src={woman_icon} alt="woman_img" />
          </div>
          <div className={styles.name_and_gender_box}>
            <p className={styles.name_info}>
              {match.woman.team} 조 {match.woman.name}
            </p>
            <div className={styles.gender_box}>
              <img src={gender_woman} alt="gender_img_png" />
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default MatListCard;
