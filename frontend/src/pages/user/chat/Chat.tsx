import { useEffect, useRef, useState } from "react";
import { useLocation } from "react-router-dom";
import axios from "axios";
import styles from "./styles/chat.module.scss";
import MeChat from "./components/me/chat/MeChat";
import OthersChat from "./components/others/chat/OthersChat";
import useSessionUser from "../../hook/useSessionUser";

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
  const { chatRoom_id, gender } = location.state || {}; // state에서 chatRoom_id, gender 받아오기
  const [chatData, setChatData] = useState<ChatResponse | null>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);
  const [message, setMessage] = useState<string>(""); // 입력된 메시지 상태 추가
  const chatEndRef = useRef<HTMLDivElement>(null); // 채팅 전송 후 스크롤을 맨 밑으로 이동시키기 위한 ref 추가

  // 채팅 데이터 가져오기
  const fetchChatContents = async () => {
    try {
      const response = await axios.post<ChatResponse>(
        "/api/user/chat/contents",
        {
          chatRoom_id,
        }
      );
      if (response.data.data) {
        setChatData({
          data: response.data.data.reverse(), // 최신순으로 정렬
        });
      }
    } catch (e) {
      setError("채팅 데이터를 불러오는 데 실패했습니다.");
    } finally {
      setLoading(false);
    }
  };

  // 채팅 데이터 전송
  const sendChat = async () => {
    if (!message.trim()) return; // 메시지가 비어있으면 전송하지 않음
    try {
      await axios.post("/api/user/chat", {
        user_id: userId,
        contents: message,
        chatRoom_id,
      });
      setMessage(""); // 메시지 전송 후 입력 필드 초기화
      fetchChatContents(); // 전송 후 최신 데이터 다시 가져오기
    } catch (e) {
      alert("메시지 전송에 실패했습니다.");
    }
  };

  useEffect(() => {
    if (chatRoom_id) {
      fetchChatContents();
    }
  }, [chatRoom_id]);

  // 최신 메시지가 추가되었을 때 스크롤을 최하단으로 이동
  useEffect(() => {
    if (chatEndRef.current) {
      chatEndRef.current.scrollIntoView({ behavior: "smooth" });
    }
  }, [chatData]);

  if (loading) return <div>Loading...</div>;
  if (error) return <div>{error}</div>;

  // 같은 유저의 연속된 메시지 그룹화
  const groupedChats: { user_id: number; contents: string[]; time: string }[] =
    [];

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

  chatData?.data?.forEach((chat) => {
    const chatTime = new Date(chat.date); // 날짜를 Date 객체로 변환
    const isSameUser =
      groupedChats.length > 0 &&
      groupedChats[groupedChats.length - 1].user_id === chat.user_id;

    // 이전 그룹과 시간이 같으면 계속 이어서 그룹화
    const isSameTime =
      groupedChats.length > 0 &&
      groupedChats[groupedChats.length - 1].time ===
        chatTime.toISOString().substring(0, 16); // ISO 시간 포맷에서 년-월-일 T 시:분 형태 비교

    if (isSameUser && isSameTime) {
      // 같은 유저, 같은 시간(분 까지만 비교)에 이어지는 메시지
      groupedChats[groupedChats.length - 1].contents.push(chat.contents);
    } else {
      // 새로운 그룹 (유저가 다르거나 시간대가 다르면 새로운 그룹 생성)
      groupedChats.push({
        user_id: chat.user_id,
        contents: [chat.contents],
        time: chatTime.toISOString().substring(0, 16), // 시간을 년-월-일 T 시:분 형식으로 저장
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
                time={formatTime(chatGroup.time)}
                gender={gender}
              />
            );
          })}
          {/* 채팅을 작성하고 최신 채팅으로 이동시켜 줄 ref */}
          <div ref={chatEndRef} />
        </div>
        <div className={styles.chat_input_box}>
          <div className={styles.chat_box}>
            <input
              className={styles.chat_input}
              placeholder="메시지 입력"
              value={message}
              onChange={(e) => setMessage(e.target.value)}
            />
            <button
              className={styles.send_button}
              onClick={sendChat}
              disabled={!message.trim()} // 메시지가 비어있으면 비활성화
            >
              전송
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}

export default Chat;
