import { useNavigate } from "react-router-dom";
import styles from "./styles/userListCard.module.scss";

interface UserListCardProps {
  id: number; // 해당 유저 id 값
  team: number | null; // 팀 번호 또는 null
  userName: string; // 유저 이름
  gender: boolean; // true: 남자, false: 여자
  chatRoomId: number | null; // 채팅방 ID
}

function UserListCard({
  id,
  team,
  userName,
  gender,
  chatRoomId,
}: UserListCardProps) {
  const navigate = useNavigate();

  const handleChatClick = () => {
    if (chatRoomId) {
      navigate(`/chat/${chatRoomId}`); // 기존 채팅방으로 이동
    } else {
      console.log(`새로운 채팅 시작: 상대 유저 ID = ${id}`);
      // 새로운 채팅방 생성 API 호출 로직 추가 가능
    }
  };

  return (
    <div className={styles.container}>
      <div className={styles.user_img_box}>
        <img
          src={`/src/assets/image/${gender ? "man" : "woman"}_icon_img.png`}
          alt={`${gender ? "man" : "woman"}_icon_img`}
        />
      </div>
      <div className={styles.team_and_name_box}>
        {team === null ? (
          <p className={styles.team_and_name_text}>{userName}</p>
        ) : (
          <p className={styles.team_and_name_text}>
            {team}조 {userName}
          </p>
        )}
        <div className={styles.gender_img_box}>
          <img
            src={`/src/assets/image/gender_${gender ? "man" : "woman"}.png`}
            alt={`gender_${gender ? "man" : "woman"}_img`}
          />
        </div>
      </div>
      <button
        className={chatRoomId ? styles.chat_button_enter : styles.chat_button}
        type="button"
        onClick={handleChatClick}
      >
        {chatRoomId ? "입장" : "채팅"}
      </button>
    </div>
  );
}

export default UserListCard;
