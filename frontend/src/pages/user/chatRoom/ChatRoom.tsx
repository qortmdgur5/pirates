import { useEffect, useState } from "react";
import axios from "axios";
import ChatRoomInfo from "./components/ChatRoomInfo";
import styles from "./styles/chatRoom.module.scss";
import useSessionUser from "../../hook/useSessionUser";
import { useNavigate } from "react-router-dom";

// ChatRoomResponse 타입을 정의합니다.
type ChatRoomResponse = {
  id: number; // 해당 채팅방 Primary key
  user_id_2: number; // 해당 채팅방 상대 유저 User Primary key
  gender: boolean; // 해당 채팅방 상대 유저 gender
  team: number | null; // 해당 채팅방 상대 유저 team but, 미지정 팀일수도 있어서 Null 가능
  name: string; // 해당 채팅방 상대 유저 name
  contents: string | null; // 해당 채팅방
  date: string | null;
  unreadCount: number | null;
};

const ChatRoom = () => {
  // 상태값을 설정합니다.
  const [chatRooms, setChatRooms] = useState<ChatRoomResponse[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  // 네비게이션 훅
  const navigate = useNavigate();

  // 유저 상태 관리 변수 Recoil
  const user = useSessionUser();
  const user_id = user?.id;
  // const party_id = user?.party_id;

  // user_id와 party_id는 예시로 설정합니다. 실제로는 로그인된 유저 정보를 사용해야 합니다.
  // const user_id = 45;
  const party_id = 2;

  // 채팅방 리스트를 가져오는 함수입니다.
  const fetchChatRooms = async () => {
    try {
      // API 요청을 보냅니다.
      const response = await axios.post<{ data: ChatRoomResponse[] }>(
        "/api/user/chatRooms",
        {
          user_id,
          party_id,
        }
      );

      // 응답 데이터를 상태에 저장합니다.
      setChatRooms(response.data.data);
    } catch (error) {
      // 에러를 처리합니다.
      setError("채팅방 데이터를 가져오는 데 실패했습니다.");
    } finally {
      setLoading(false);
    }
  };

  // date 속성 2025-01-31T16:05:11 -> 오전 or 오후 hh:tt 형식 변환
  const formatTime = (dateString: string | null): string => {
    if (!dateString) return ""; // null일 경우 빈 문자열 반환

    const date = new Date(dateString);
    const hours = date.getHours();
    const minutes = date.getMinutes().toString().padStart(2, "0"); // 항상 두 자리 유지
    const period = hours < 12 ? "오전" : "오후";

    // 12시간 형식으로 변환 (0시는 12시로 처리)
    const formattedHours = hours % 12 === 0 ? 12 : hours % 12;

    return `${period} ${formattedHours}:${minutes}`;
  };

  // 컴포넌트가 처음 렌더링될 때 채팅방 리스트를 가져옵니다.
  useEffect(() => {
    fetchChatRooms();
  }, []);

  // 로딩 중일 때 보여줄 화면
  if (loading) return <div>Loading...</div>;

  // 에러가 있을 때 보여줄 화면
  if (error) return <div>{error}</div>;

  return (
    <div className={styles.container}>
      <div className={styles.container_contents}>
        <div className={styles.header}>
          <p className={styles.header_text}>채팅방</p>
        </div>
        <div className={styles.chat_rooms_contents}>
          {chatRooms.map((chatRoom) => (
            <div
              key={chatRoom.id}
              onClick={() =>
                navigate("/user/chat", {
                  state: {
                    chatRoom_id: chatRoom.id,
                    gender: chatRoom.gender,
                  },
                })
              }
            >
              <ChatRoomInfo
                name={
                  chatRoom.team
                    ? `${chatRoom.team}조 ${chatRoom.name}`
                    : chatRoom.name
                }
                text={chatRoom.contents || ""}
                time={formatTime(chatRoom.date) || ""}
                newAlert={chatRoom.unreadCount || null}
                gender={chatRoom.gender}
              />
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default ChatRoom;
