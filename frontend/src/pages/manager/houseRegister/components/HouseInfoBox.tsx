// HouseInfoBox.tsx
import styles from "./styles/houseInfoBox.module.scss";

// Props로 받을 타입 정의
export interface HouseInfo {
  name: string;
  address: string;
  number: string;
  introduction: string;
  score: number | null;
  loveCount: number | null;
}

interface HouseInfoBoxProps {
  houseInfo: HouseInfo;
}

function HouseInfoBox({ houseInfo }: HouseInfoBoxProps) {
  return (
    <div className={styles.container}>
      <div className={styles.house_info_container}>
        <p className={styles.house_name}>{houseInfo.name}</p>
        <div className={styles.house_info_box}>
          <div className={styles.house_info}>
            <p className={styles.houes_info_left_text}>소개</p>
            <p className={styles.houes_info_right_text}>{houseInfo.introduction}</p>
          </div>
          <div className={styles.house_info}>
            <p className={styles.houes_info_left_text}>주소</p>
            <p className={styles.houes_info_right_text}>{houseInfo.address}</p>
          </div>
          <div className={styles.house_info}>
            <p className={styles.houes_info_left_text}>전화번호</p>
            <p className={styles.houes_info_right_text}>{houseInfo.number}</p>
          </div>
          <div className={styles.house_info}>
            <p className={styles.houes_info_left_text}>평점</p>
            <p className={styles.houes_info_right_text}>
              {houseInfo.score ? `⭐${houseInfo.score}` : "평가 없음"}
            </p>
          </div>
          <div className={styles.house_info}>
            <p className={styles.houes_info_left_text}>짝 매칭 카운트</p>
            <p className={styles.houes_info_right_text}>
              ❤️{houseInfo.loveCount ?? 0}
            </p>
          </div>
        </div>
        <div className={styles.button_container}>
          <button className={styles.register_button}>등록</button>
          <button className={styles.modify_button}>수정</button>
        </div>
      </div>
    </div>
  );
}

export default HouseInfoBox;
