import styles from "./othersChat.module.scss";

interface OthersChatProps {
  text: string; // 유저 채팅 내역
  time: string; // 유저 채팅 시간
  gender: string; // 상대방 성별
}

function OthersChat({ text, time, gender }: OthersChatProps) {
  // gender에 따라 이미지 변경
  const userImage =
    gender === "male"
      ? "/src/assets/image/man_icon_img.png"
      : "/src/assets/image/woman_icon_img.png"; // 예시로 남성/여성 아이콘 사용

  return (
    <div className={styles.container}>
      <button className={styles.info_image} type="button">
        <img src={userImage} alt="user_icon_image" />
      </button>
      <div className={styles.chat_box}>
        {text.split("\n").map((line, index) => (
          <p key={index} className={styles.chat_text}>
            {line}
          </p>
        ))}
      </div>
      <p className={styles.time_text}>{time}</p>
    </div>
  );
}

export default OthersChat;
