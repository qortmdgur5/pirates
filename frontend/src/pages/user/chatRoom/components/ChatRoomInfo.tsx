import styles from "./chatRoomInfo.module.scss";

interface ChatRoomInfoProps {
  name: string;
  text: string;
  time: string;
  newAlert: number | null;
}

function ChatRoomInfo({ name, text, time, newAlert }: ChatRoomInfoProps) {
  return (
    <div className={styles.container}>
      <div className={styles.user_image_box}>
        <img src="/src/assets/image/man_icon_img.png" alt="man_img" />
      </div>
      <div className={styles.user_chat_info_box}>
        <div className={styles.user_chat_info_left}>
          <p className={styles.user_name}>{name}</p>
          <p className={styles.user_chat_text}>{text}</p>
        </div>
        <div className={styles.user_chat_info_right}>
          <p className={styles.user_chat_time}>{time}</p>
          <p
            className={styles.user_chat_new_alert}
            style={{ visibility: newAlert === null ? "hidden" : "visible" }}
          >
            {newAlert}
          </p>
        </div>
      </div>
    </div>
  );
}

export default ChatRoomInfo;
