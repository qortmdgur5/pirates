import styles from "./styles/chat.module.scss";

// 컴포넌트
import MeChat from "./components/me/chat/MeChat";
import MeInfo from "./components/me/info/MeInfo";
import OthersChat from "./components/others/chat/OthersChat";
import OthersInfo from "./components/others/info/OthersInfo";

function Chat() {
  return (
    <div className={styles.container}>
      <div className={styles.container_contens}>
        <div className={styles.chat_header}>
          <p className={styles.chat_header_text}>김병만두님과의 채팅</p>
        </div>
        <div className={styles.chat_contents}>
          <OthersInfo id={1} name={"상대방 이름"} time={"09:14 AM"} />
          <OthersChat
            text={
              "dskjfhsdkjfhksdjfhkjdshfkjhdsnmkasndmnasmdnasbdasbdnsmabdmnsadjhasgdjkhwjkehwqkjehkqwjehkwqjhekjh"
            }
          />
          <OthersChat
            text={
              "dskjfhsdkjfhksdjfhkjdshfkjhdsnmkasndmnasmdnasbdasbdnsmabdmnsadjhasgdjkhwjkehwqkjehkqwjehkwqjhekjh"
            }
          />
          <OthersChat
            text={
              "dskjfhsdkjfhksdjfhkjdshfkjhdsnmkasndmnasmdnasbdasbdnsmabdmnsadjhasgdjkhwjkehwqkjehkqwjehkwqjhekjh"
            }
          />
          <MeInfo name={"내 이름"} time={"09:25 AM"} />
          <MeChat
            text={
              "bjjhjfkkjbkjewjhewrhuweqkjdjkhsdjkbsdjhfejkbfeuhfewjkbewjkewjbksdfbjksdjbsdfjhbwefrierwkjbwerjkwerjkbwerjkbwer"
            }
          />
          <MeChat
            text={
              "bjjhjfkkjbkjewjhewrhuweqkjdjkhsdjkbsdjhfejkbfeuhfewjkbewjkewjbksdfbjksdjbsdfjhbwefrierwkjbwerjkwerjkbwerjkbwer"
            }
          />
          <MeChat
            text={
              "bjjhjfkkjbkjewjhewrhuweqkjdjkhsdjkbsdjhfejkbfeuhfewjkbewjkewjbksdfbjksdjbsdfjhbwefrierwkjbwerjkwerjkbwerjkbwer"
            }
          />
        </div>
        <div className={styles.chat_input_box}>
          <div className={styles.chat_box}>
            <textarea
              className={styles.chat_input}
              placeholder="메시지 입력"
              rows={1}
            />
            <button className={styles.send_button}>전송</button>
          </div>
        </div>
      </div>
    </div>
  );
}

export default Chat;
