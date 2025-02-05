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
  const { chatRoom_id, gender, yourName } = location.state || {}; // state에서 chatRoom_id, gender 받아오기
  const [chatData, setChatData] = useState<ChatData[]>([]);
  const [lastChatId, setLastChatId] = useState<number | null>(null); // 현재 채팅 데이터 중 가장 오래된 채팅 id
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);
  const [message, setMessage] = useState<string>(""); // 입력된 메시지 상태 추가
  const [isMyMessageSent, setIsMyMessageSent] = useState(false); // 내가 보낸 채팅 여부
  const [hasMore, setHasMore] = useState(true);
  const pageSize = 30; // 우리가 임의로 정해준 한번에 가져오는 데이터 수. 서버에서 정함
  const chatEndRef = useRef<HTMLDivElement>(null); // 새로운 채팅 전송 하면 최하단으로 스크롤 위한 ref
  const chatContainerRef = useRef<HTMLDivElement>(null); // 최상단 스크롤 할 시 이전 채팅 내역 로드 위한 ref
  const isFetchingRef = useRef(false); // 중복 요청 방지
  const isFirstRender = useRef(true); // 첫 렌더링 여부 체크

  // WebSocket 연결을 위한 ref
  const socketRef = useRef<WebSocket | null>(null);

  // chatData가 업데이트될 때마다 lastChatId를 계산
  useEffect(() => {
    if (chatData.length > 0) {
      setLastChatId(chatData[0].id);
    }
  }, [chatData]);

  // 채팅 데이터 가져오기 (lastChat_id 기반)
  const fetchChatContents = async (append: boolean = false) => {
    // 비동기 중복 방지 -> true 일때는 실행되지 않도록
    if (isFetchingRef.current) return;
    isFetchingRef.current = true;

    try {
      const chatBox = chatContainerRef.current;
      const previousScrollHeight = chatBox?.scrollHeight || 0;

      const response = await axios.post<ChatResponse>(
        "/api/user/chat/contents",
        { chatRoom_id, lastChat_id: append ? lastChatId : null }
      );

      const newData = response?.data?.data || [];

      // 로드한 데이터가 pageSize 보다 더 작으면 더 가져올 데이터가 없으므로
      if (newData.length < pageSize) setHasMore(false);

      setChatData((prevData) =>
        append ? [...newData, ...prevData] : [...prevData, ...newData]
      );

      if (newData.length > 0 && isFirstRender) {
        setLastChatId(newData[0].id);
      }

      // 이전 채팅이 추가된 후에도 스크롤 위치 유지
      requestAnimationFrame(() => {
        if (chatBox) {
          chatBox.scrollTop = chatBox.scrollHeight - previousScrollHeight;
        }
      });
    } catch (e) {
      setError("채팅 데이터를 불러오는 데 실패했습니다.");
    } finally {
      setLoading(false);
      isFetchingRef.current = false;
    }
  };

  // 초기 데이터 로드
  useEffect(() => {
    if (chatRoom_id) {
      fetchChatContents(false);
    }
  }, [chatRoom_id]);

  // WebSocket 연결 설정
  useEffect(() => {
    if (chatRoom_id && userId) {
      socketRef.current = new WebSocket(
        `ws://localhost:9000/user/ws/chat/${chatRoom_id}/${userId}`
      );

      socketRef.current.onopen = () => {
        console.log("WebSocket 연결됨.");
      };

      socketRef.current.onmessage = (event) => {
        const messageData = JSON.parse(event.data); // 서버에서 온 메시지가 JSON 형식이라면 파싱

        const { user_id, content } = messageData; // 서버에서 받은 메시지 데이터

        // 서버에서 메시지를 받으면 채팅 데이터에 추가
        setChatData((prevData) => [
          ...prevData,
          {
            id: prevData.length > 0 ? prevData[prevData.length - 1].id + 1 : 1, // 마지막 id에 1을 더함, 첫 번째 채팅은 1부터 시작 - 임시로 처리
            user_id: user_id, // 채팅을 보낸 사람의 user_id
            contents: content, // 메시지 내용
            date: new Date().toISOString(), // 메시지 전송 시간
          },
        ]);
      };

      socketRef.current.onerror = (error) => {
        console.error("WebSocket 에러:", error);
      };

      socketRef.current.onclose = () => {
        console.log("WebSocket 연결 종료");
      };
    }

    return () => {
      if (socketRef.current) {
        socketRef.current.close();
      }
    };
  }, [chatRoom_id, userId]);

  // 채팅 전송
  // const sendChat = async () => {
  //   if (!message.trim()) return;
  //   try {
  //     await axios.post("/api/user/chat", {
  //       user_id: userId,
  //       contents: message,
  //       chatRoom_id,
  //     });
  //     setMessage("");
  //     setIsMyMessageSent(true);
  //   } catch (e) {
  //     alert("메시지 전송에 실패했습니다.");
  //   }
  // };
  const sendChat = async () => {
    if (!message.trim()) return;

    // WebSocket이 연결된 상태일 때만 메시지 전송
    if (socketRef.current) {
      if (socketRef.current.readyState === WebSocket.OPEN) {
        // 연결 완료된 경우 메시지 전송
        socketRef.current.send(message);
        setMessage("");
        setIsMyMessageSent(true);
      } else if (socketRef.current.readyState === WebSocket.CONNECTING) {
        console.log("WebSocket 연결 중입니다...");
      } else {
        console.error("WebSocket 연결이 완료되지 않았습니다.");
      }
    } else {
      console.error("WebSocket 객체가 존재하지 않습니다.");
    }
  };

  // 초기 페이지 진입시 최초 렌더링 후 스크롤 최하단으로 이동
  useEffect(() => {
    if (isFirstRender.current && chatData.length > 0) {
      if (chatData.length > 0 && chatEndRef.current) {
        chatEndRef.current.scrollIntoView({ behavior: "auto" });
      }
      isFirstRender.current = false; // 첫 렌더링 완료 후 false로 설정
    }
  }, [chatData]);

  // 내가 채팅을 보낸 경우에만 스크롤 최하단 이동
  useEffect(() => {
    if (isMyMessageSent && chatEndRef.current) {
      chatEndRef.current.scrollIntoView({ behavior: "auto" });
      setIsMyMessageSent(false);
    }
  }, [chatData]);

  // 스크롤 최상단 도달 시 이전 채팅 불러오기
  const handleScroll = () => {
    const chatBox = chatContainerRef.current;
    if (!chatBox || !hasMore) return;

    if (chatBox.scrollTop === 0) {
      fetchChatContents(true);
      console.log(chatData);
    }
  };

  useEffect(() => {
    const chatBox = chatContainerRef.current;
    if (chatBox) {
      chatBox.addEventListener("scroll", handleScroll);
    }
    return () => {
      if (chatBox) {
        chatBox.removeEventListener("scroll", handleScroll);
      }
    };
  }, [chatData]);

  if (loading) return <div>Loading...</div>;
  if (error) return <div>{error}</div>;

  // date 속성 2025-01-31T16:05:11 -> 오전 or 오후 hh:tt 형식 변환
  const formatTime = (dateString: string | null): string => {
    if (!dateString) return ""; // null일 경우 빈 문자열 반환

    const date = new Date(dateString + "Z"); // UTC 기반 시간 보정
    const hours = date.getHours();
    const minutes = date.getMinutes().toString().padStart(2, "0"); // 항상 두 자리 유지
    const period = hours < 12 ? "오전" : "오후";

    // 12시간 형식으로 변환 (0시는 12시로 처리)
    const formattedHours = hours % 12 === 0 ? 12 : hours % 12;

    return `${period} ${formattedHours}:${minutes}`;
  };

  // 같은 유저의 연속된 메시지 그룹화
  const groupedChats: { user_id: number; contents: string[]; time: string }[] =
    [];

  chatData.forEach((chat) => {
    const chatTime = new Date(chat.date);
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
          <p className={styles.chat_header_text}>{yourName} 님과의 채팅</p>
        </div>
        <div className={styles.chat_contents} ref={chatContainerRef}>
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
          {/* 본인이 채팅을 전송하고 최하단 으로 움직여줄 ref */}
          <div ref={chatEndRef} />
        </div>
        <div className={styles.chat_input_box}>
          <div className={styles.chat_box}>
            <input
              className={styles.chat_input}
              placeholder="메시지 입력"
              value={message}
              onChange={(e) => setMessage(e.target.value)}
              onKeyDown={(e) => {
                if (e.key === "Enter") {
                  sendChat();
                }
              }}
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
