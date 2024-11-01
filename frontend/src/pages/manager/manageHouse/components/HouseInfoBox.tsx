import { useEffect, useState } from "react";
import styles from "./styles/houseInfoBox.module.scss";

// Props로 받을 타입 정의
interface HouseInfo {
  name: string;
  address: string;
  number: string;
  introduction: string;
  score: number | null;
  loveCount: number | null;
}

interface HouseInfoBoxProps {
  houseInfo: HouseInfo | null;
}

function HouseInfoBox({ houseInfo }: HouseInfoBoxProps) {
  const [isEditing, setIsEditing] = useState(false);
  const [editedInfo, setEditedInfo] = useState<HouseInfo>({
    name: "",
    address: "",
    number: "",
    introduction: "",
    score: null,
    loveCount: null,
  });

  // houseInfo가 변경될 때 editedInfo를 업데이트
  useEffect(() => {
    if (houseInfo) {
      setEditedInfo({
        name: houseInfo.name,
        address: houseInfo.address,
        number: houseInfo.number,
        introduction: houseInfo.introduction,
        score: houseInfo.score,
        loveCount: houseInfo.loveCount,
      });
      setIsEditing(false); // houseInfo가 있을 때는 수정 모드가 아닙니다.
    } else {
      setEditedInfo({
        name: "",
        address: "",
        number: "",
        introduction: "",
        score: null,
        loveCount: null,
      });
      setIsEditing(true); // houseInfo가 없을 때는 수정 모드로 설정합니다.
    }
  }, [houseInfo]);

  const handleInputChange = (field: keyof HouseInfo, value: string) => {
    setEditedInfo((prev) => ({ ...prev, [field]: value }));
  };

  const toggleEditMode = () => {
    setIsEditing((prev) => !prev);
  };

  return (
    <div className={styles.container}>
      <div className={styles.house_info_container}>
        {isEditing ? (
          <>
            <input
              type="text"
              value={editedInfo.name}
              onChange={(e) => handleInputChange("name", e.target.value)}
              className={styles.house_name_input}
              placeholder="게스트하우스 이름"
            />
            <div className={styles.house_info_box}>
              <div className={styles.house_info}>
                <p className={styles.house_info_left_text}>소개</p>
                <input
                  type="text"
                  value={editedInfo.introduction}
                  onChange={(e) =>
                    handleInputChange("introduction", e.target.value)
                  }
                  className={styles.house_right_input}
                  placeholder="소개"
                />
              </div>
              <div className={styles.house_info}>
                <p className={styles.house_info_left_text}>주소</p>
                <input
                  type="text"
                  value={editedInfo.address}
                  onChange={(e) => handleInputChange("address", e.target.value)}
                  className={styles.house_right_input}
                  placeholder="주소"
                />
              </div>
              <div className={styles.house_info}>
                <p className={styles.house_info_left_text}>전화번호</p>
                <input
                  type="text"
                  value={editedInfo.number}
                  onChange={(e) => handleInputChange("number", e.target.value)}
                  className={styles.house_right_input}
                  placeholder="게스트하우스 전화번호"
                />
              </div>
            </div>
            <div className={styles.button_container}>
              <button onClick={toggleEditMode} className={styles.save_button}>
                저장
              </button>
              <button
                onClick={() => setIsEditing(false)}
                className={styles.cancel_button}
              >
                취소
              </button>
            </div>
          </>
        ) : (
          <>
            <p className={styles.house_name}>{houseInfo?.name}</p>
            <div className={styles.house_info_box}>
              <div className={styles.house_info}>
                <p className={styles.house_info_left_text}>소개</p>
                <p className={styles.house_info_right_text}>
                  {houseInfo?.introduction}
                </p>
              </div>
              <div className={styles.house_info}>
                <p className={styles.house_info_left_text}>주소</p>
                <p className={styles.house_info_right_text}>
                  {houseInfo?.address}
                </p>
              </div>
              <div className={styles.house_info}>
                <p className={styles.house_info_left_text}>전화번호</p>
                <p className={styles.house_info_right_text}>
                  {houseInfo?.number}
                </p>
              </div>
              <div className={styles.house_info}>
                <p className={styles.house_info_left_text}>평점</p>
                <p className={styles.house_info_right_text}>
                  {houseInfo?.score ? `⭐${houseInfo.score}` : "평가 없음"}
                </p>
              </div>
              <div className={styles.house_info}>
                <p className={styles.house_info_left_text}>짝 매칭 카운트</p>
                <p className={styles.house_info_right_text}>
                  ❤️{houseInfo?.loveCount ?? 0}
                </p>
              </div>
            </div>
            <div className={styles.button_container}>
              <button className={styles.modify_button} onClick={toggleEditMode}>
                수정
              </button>
            </div>
          </>
        )}
      </div>
    </div>
  );
}

export default HouseInfoBox;
