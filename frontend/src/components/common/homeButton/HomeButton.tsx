import styles from "./styles/homeButton.module.scss";

function HomeButton() {
  return (
    <div className={styles.home_text_box}>
      <img src="/src/assets/image/home_icon.png" alt="home_icon_image" />
      <span className={styles.home_text}>HOME</span>
    </div>
  );
}

export default HomeButton;
