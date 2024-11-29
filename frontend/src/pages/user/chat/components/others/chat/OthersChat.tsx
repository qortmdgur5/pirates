import styles from "./othersChat.module.scss";

interface OthersChatProps {
  text: string; // 유저 채팅 내역
}

function OthersChat({ text }: OthersChatProps) {
  return (
    <div className={styles.chat_box}>
      <p className={styles.chat_text}>{text}</p>
    </div>
  );
}

export default OthersChat;
