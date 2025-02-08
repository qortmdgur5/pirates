import styles from "./styles/matchListCard.module.scss";

function MatListCard() {
  return (
    <div className={styles.container}>
      <div className={styles.match_box}>
        <div className={styles.man_box}>
          <div className={styles.man_img_box}>
            <img src="/src/assets/image/man_icon_img.png" alt="man_img" />
          </div>
          <div className={styles.name_and_gender_box}>
            <p className={styles.name_info}>김병민</p>
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
            <p className={styles.name_info}>구슬기</p>
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
