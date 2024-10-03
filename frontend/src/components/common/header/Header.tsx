import styles from "./styles/header.module.scss"
function Header() {
  return (
    <header className={styles.container}>
      <div className={styles.header_logo_box}>
        <div className={styles.header_logo_img_box}>
          <img src="/src/assets/image/pirates_logo_img.png" alt="logo_img" />
        </div>
        <p className={styles.header_logo_box_text}>해적</p>
      </div>
      <button className={styles.logout_button}>
        로그아웃
        <img src="/src/assets/image/naver_login_button.png" alt="logout_img" />
      </button>
    </header>
  )
}

export default Header