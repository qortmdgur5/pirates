import styles from "./meChat.module.scss";

interface MyChatProps {
  text: string; // 유저 채팅 내역
  time: string; // 유저 채팅 시간
}

function MeChat({ text, time }: MyChatProps) {
  return (
    <div className={styles.container}>
      <p className={styles.time_text}>{time}</p>
      <div className={styles.chat_box}>
        <p className={styles.chat_text}>{text}</p>
        <p className={styles.chat_text}>{text}</p>
        <p className={styles.chat_text}>{text}</p>
      </div>
    </div>
  );
}

export default MeChat;
