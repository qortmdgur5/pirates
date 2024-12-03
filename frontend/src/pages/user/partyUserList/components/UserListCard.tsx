import styles from './styles/userListCard.module.scss'

function UserListCard() {
  return (
    <div className={styles.container}>
      <div className={styles.user_img_box}>
        <img src="/src/assets/image/man_icon_img.png" alt="man_icon_img" />
      </div>
      <div className={styles.team_and_name_box}>
        <p className={styles.team_and_name_text}>
          1조 철수
        </p>
        <div className={styles.gender_img_box}>
          <img src="/src/assets/image/gender_man.png" alt="gender_man_img" />
        </div>
      </div>
      <p className={styles.chat_button}>채팅</p>
    </div>
  )
}

export default UserListCard