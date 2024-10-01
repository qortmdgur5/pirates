import styles from "./styles/login.module.scss";

function Login() {
  return (
    <div className={styles.container}>
      <div className={styles.login_box}>
        <div className={styles.login_box_left}>
          <div className={styles.login_box_left_inner}>
            <p className={styles.login_box_left_inner_text_1}>해적</p>
            <p className={styles.login_box_left_inner_text_2}>Pirates</p>
            <p className={styles.login_box_left_inner_text_3}>
              게스트 하우스 정보가 한눈에!
            </p>
            <div className={styles.login_box_left_inner_img_box}>
              <img
                src="/src/assets/image/pirates_logo_img.png"
                alt="pirates main image"
              />
            </div>
          </div>
        </div>
        <div className={styles.login_box_right}></div>
      </div>
    </div>
  );
}

export default Login;
