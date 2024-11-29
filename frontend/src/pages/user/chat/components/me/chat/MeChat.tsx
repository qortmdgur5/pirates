import styles from "./meChat.module.scss";

interface MyChatProps {
  text: string; // 유저 채팅 내역
}

function MeChat({ text }: MyChatProps) {
  return (
    <div className={styles.chat_box}>
      <p className={styles.chat_text}>{text}</p>
    </div>
  );
}

export default MeChat;
