import { useNavigate } from "react-router-dom";
import styles from "./styles/userListCard.module.scss";
import axios from "axios";

interface UserListCardProps {
  id: number; // 해당 유저 id 값
  team: number | null; // 팀 번호 또는 null
  userName: string; // 유저 이름
  gender: boolean; // true: 남자, false: 여자
  chatRoomId: number | null; // 채팅방 ID
  userId: number | null; // 본인 id
  partyId: number | null; // 파티 id
}

function UserListCard({
  id,
  team,
  userName,
  gender,
  chatRoomId,
  userId,
  partyId,
}: UserListCardProps) {
  const navigate = useNavigate();

  // 채팅방 생성 API
  const makeParty = async () => {
    if (!userId || !partyId) {
      return; // 유저 id 값이 없거나 partyId 값이 없으면 대기
    }

    // 사용자에게 채팅방 생성을 확인하는 창 띄우기
    const isConfirmed = window.confirm("정말 채팅방을 만드시겠습니까?");
    if (!isConfirmed) {
      return; // 사용자가 취소하면 함수 종료
    }

    try {
      // 더 큰 값이 user_id_1에 오도록 처리
      const [user_id_1, user_id_2] = userId > id ? [userId, id] : [id, userId];
      const response = await axios.post("/api/user/chatRoom", {
        user_id_1: user_id_1,
        user_id_2: user_id_2,
        party_id: partyId,
      });

      const newChatRoomId = response.data.data.chatRoom_id; // 생성된 채팅방 id

      if (newChatRoomId) {
        navigate("/user/chat", {
          state: {
            chatRoom_id: newChatRoomId,
            gender: gender,
            yourName: userName,
          },
        });
      } else {
        alert("채팅방을 생성하지 못했습니다. 관리자에게 문의 바랍니다.");
      }
    } catch (error) {
      console.log(error);
      alert("채팅방을 생성하지 못했습니다. 관리자에게 문의 바랍니다.");
    }
  };

  const handleChatClick = () => {
    if (chatRoomId) {
      navigate("/user/chat", {
        state: {
          chatRoom_id: chatRoomId,
          gender: gender,
          yourName: userName,
        },
      });
    } else {
      makeParty();
    }
  };

  const isSelf = id === userId; // 본인인지 확인

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
        className={
          isSelf
            ? styles.chat_button_self
            : chatRoomId
            ? styles.chat_button_enter
            : styles.chat_button
        }
        type="button"
        onClick={handleChatClick}
        disabled={isSelf} // 본인일 경우 버튼 비활성화
      >
        {isSelf ? "본인" : chatRoomId ? "입장" : "채팅"}
      </button>
    </div>
  );
}

export default UserListCard;
