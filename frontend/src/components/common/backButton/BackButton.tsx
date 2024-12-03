import styles from './styles/backButton.module.scss'

function BackButton() {
  return (
    <button type='button' className={styles.container}>
      <div className={styles.back_img_box}>
        <img src="/src/assets/image/back.png" alt="back_button_img" />
      </div>
      <p className={styles.back_text}>BACK</p>
    </button>
  )
}

export default BackButton