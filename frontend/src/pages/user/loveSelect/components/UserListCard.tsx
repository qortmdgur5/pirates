import styles from "./styles/userListCard.module.scss";

function UserListCard() {
  return (
    <div className={styles.container}>
      <div className={styles.img_box}>
        <div className={styles.img_info}>
          <img src="/src/assets/image/woman_icon_img.png" alt="user_img_png" />
        </div>
      </div>
      <div className={styles.name_and_gender_box}>
        <div className={styles.name_and_gender_info}>
          <p className={styles.name_text}>김철수</p>
          <div className={styles.gender_box}>
            <img
              src="/src/assets/image/gender_woman.png"
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
