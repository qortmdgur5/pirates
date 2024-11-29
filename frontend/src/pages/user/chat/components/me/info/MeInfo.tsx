import styles from "./meInfo.module.scss";

// Props 타입 정의
interface MeInfoProps {
  name: string; // 유저 이름
  time: string; // 채팅 시간
}

function MeInfo({ name, time }: MeInfoProps) {
  return (
    <div className={styles.info_box}>
      <p className={styles.info_name}>{name}</p>
      <p className={styles.info_time}>{time}</p>
      <button className={styles.info_image} type="button"></button>
    </div>
  );
}

export default MeInfo;
