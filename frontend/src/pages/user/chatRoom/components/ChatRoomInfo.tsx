import styles from "./chatRoomInfo.module.scss";

interface ChatRoomInfoProps {
  name: string; // 상대방 팀 및 이름
  text: string; // 가장 최신 채팅
  time: string; // 가장 최신 채팅 시간
  newAlert: number | null; // 안읽은 채팅 수
  gender: boolean; // 상대방 성별
}

function ChatRoomInfo({
  name,
  text,
  time,
  newAlert,
  gender,
}: ChatRoomInfoProps) {
  return (
    <div className={styles.container}>
      <div className={styles.user_image_box}>
        <img
          src={
            gender
              ? "/src/assets/image/man_icon_img.png"
              : "/src/assets/image/woman_icon_img.png"
          }
          alt={gender ? "man_img" : "woman_img"}
        />
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
