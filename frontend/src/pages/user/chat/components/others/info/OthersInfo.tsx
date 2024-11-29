import styles from "./othersInfo.module.scss";

// Props 타입 정의
interface OthersInfoProps {
  id: number; // 유저의 primary key
  name: string; // 유저 이름
  time: string; // 채팅 시간
}

function OthersInfo({ id, name, time }: OthersInfoProps) {
  return (
    <div className={styles.info_box}>
      <button className={styles.info_image} aria-label={`User ID: ${id}`} type="button"></button>
      <p className={styles.info_name}>{name}</p>
      <p className={styles.info_time}>{time}</p>
    </div>
    
  );
}

export default OthersInfo;
