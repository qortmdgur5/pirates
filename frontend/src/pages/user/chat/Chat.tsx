import { useEffect, useState } from "react";
import { useLocation } from "react-router-dom";
import axios from "axios";
import styles from "./styles/chat.module.scss";
import MeChat from "./components/me/chat/MeChat";
import OthersChat from "./components/others/chat/OthersChat";
import useSessionUser from "../../hook/useSessionUser";

// Chat 데이터 타입 (인터페이스로 변경)
interface ChatData {
  id: number;
  user_id: number;
  contents: string;
  date: string;
}

interface ChatResponse {
  data: ChatData[] | null;
}

function Chat() {
  const user = useSessionUser();
  const userId = user?.id;
  const location = useLocation();
  const { chatRoom_id, gender } = location.state || {}; // state에서 chatRoom_id 받아오기
  const [chatData, setChatData] = useState<ChatResponse | null>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  // 채팅 데이터 가져오기
  const fetchChatContents = async () => {
    try {
      const response = await axios.post<ChatResponse>(
        "/api/user/chat/contents",
        {
          chatRoom_id,
        }
      );
      setChatData(response.data);
    } catch (e) {
      setError("채팅 데이터를 불러오는 데 실패했습니다.");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    if (chatRoom_id) {
      fetchChatContents();
    }
  }, [chatRoom_id]);

  if (loading) return <div>Loading...</div>;
  if (error) return <div>{error}</div>;

  // 같은 유저의 연속된 메시지 그룹화
  const groupedChats: { user_id: number; contents: string[]; time: string }[] =
    [];
  chatData?.data?.forEach((chat) => {
    const isSameUser =
      groupedChats.length > 0 &&
      groupedChats[groupedChats.length - 1].user_id === chat.user_id;
    if (isSameUser) {
      groupedChats[groupedChats.length - 1].contents.push(chat.contents);
    } else {
      groupedChats.push({
        user_id: chat.user_id,
        contents: [chat.contents],
        time: chat.date,
      });
    }
  });

  return (
    <div className={styles.container}>
      <div className={styles.container_contens}>
        <div className={styles.chat_header}>
          <button type="button" className={styles.back_button}>
            &lt;
          </button>
          <p className={styles.chat_header_text}>김병만두님과의 채팅</p>
        </div>
        <div className={styles.chat_contents}>
          {groupedChats.map((chatGroup, index) => {
            const isMyChat = chatGroup.user_id === userId;
            const ChatComponent = isMyChat ? MeChat : OthersChat;
            return (
              <ChatComponent
                key={index}
                text={chatGroup.contents.join("\n")}
                time={chatGroup.time}
                gender={gender}
              />
            );
          })}
        </div>
        <div className={styles.chat_input_box}>
          <div className={styles.chat_box}>
            <input className={styles.chat_input} placeholder="메시지 입력" />
            <button className={styles.send_button}>전송</button>
          </div>
        </div>
      </div>
    </div>
  );
}

export default Chat;
