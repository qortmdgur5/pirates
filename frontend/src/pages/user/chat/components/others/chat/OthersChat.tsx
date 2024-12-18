import styles from "./othersChat.module.scss";

interface OthersChatProps {
  text: string; // 유저 채팅 내역
  time: string; // 유저 채팅 시간
}

function OthersChat({ text, time }: OthersChatProps) {
  return (
    <div className={styles.container}>
      <button className={styles.info_image} type="button">
        <img src="/src/assets/image/man_icon_img.png" alt="user_icon_image" />
      </button>
      <div className={styles.chat_box}>
        <p className={styles.chat_text}>{text}</p>
        <p className={styles.chat_text}>{text}</p>
        <p className={styles.chat_text}>{text}</p>
      </div>
      <p className={styles.time_text}>{time}</p>
    </div>
  );
}

export default OthersChat;
