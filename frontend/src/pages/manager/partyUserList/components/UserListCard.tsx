import styles from "./styles/userListCard.module.scss";

function UserListCard() {
  return (
    <div className={styles.container}>
      <div className={styles.user_img_box}>
        <img src="/src/assets/image/man_icon_img.png" alt="man_icon_img" />
      </div>
      <div className={styles.team_and_name_box}>
        <p className={styles.team_and_name_text}>1조 철수</p>
        <div className={styles.gender_img_box}>
          <img src="/src/assets/image/gender_man.png" alt="gender_man_img" />
        </div>
      </div>
      <div className={styles.team_select_box}>
        <select className={styles.team_select}>
          <option value="1조">1조</option>
          <option value="2조">2조</option>
          <option value="3조">3조</option>
        </select>
      </div>
      <button className={styles.on_off_button} type="button">
        ON
      </button>
    </div>
  );
}

export default UserListCard;
