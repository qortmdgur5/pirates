import styles from "./meChat.module.scss";

interface MyChatProps {
  text: string; // 유저 채팅 내역
  time: string; // 유저 채팅 시간
}

function MeChat({ text, time }: MyChatProps) {
  const textLines = text.split("\n"); // \n 기준으로 메시지 분리

  return (
    <div className={styles.container}>
      <p className={styles.time_text}>{time}</p>
      <div className={styles.chat_box}>
        {textLines.map((line, index) => (
          <p key={index} className={styles.chat_text}>
            {line}
          </p>
        ))}
      </div>
    </div>
  );
}

export default MeChat;
