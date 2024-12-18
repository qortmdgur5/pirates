import styles from "./styles/chat.module.scss";

// 컴포넌트
import MeChat from "./components/me/chat/MeChat";
import OthersChat from "./components/others/chat/OthersChat";

function Chat() {
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
          <OthersChat
            text={
              "dskjfhsdkjfhksdjfhkjdshfkjhdsnmkasndmnasmdnasbdasbdnsmabdmnsadjhasgdjkhwjkehwqkjehkqwjehkwqjhekjh"
            }
            time="오후 2:02"
          />
          <OthersChat
            text={
              "dskjfhsdkjfhksdjfhkjdshfkjhdsnmkasndmnasmdnasbdasbdnsmabdmnsadjhasgdjkhwjkehwqkjehkqwjehkwqjhekjh"
            }
            time="오후 2:02"
          />
          <OthersChat
            text={
              "dskjfhsdkjfhksdjfhkjdshfkjhdsnmkasndmnasmdnasbdasbdnsmabdmnsadjhasgdjkhwjkehwqkjehkqwjehkwqjhekjh"
            }
            time="오후 2:02"
          />
          <MeChat text={"asdsad"} time="오후 2:04" />
          <MeChat text={"asdsad"} time="오후 2:04" />
          <MeChat text={"asdsad"} time="오후 2:04" />
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
