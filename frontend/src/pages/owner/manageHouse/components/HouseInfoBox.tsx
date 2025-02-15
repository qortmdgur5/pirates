import { useEffect, useState } from "react";
import styles from "./styles/houseInfoBox.module.scss";

interface HouseInfo {
  id: number | null;
  name: string;
  address: string;
  number?: string; // 전화번호는 선택사항으로 처리
  introduction: string;
  score?: number | null;
  loveCount?: number | null;
}

interface HouseInfoBoxProps {
  houseInfo: HouseInfo | null;
  onSave: (newData: HouseInfo) => Promise<void>;
  onUpdate: (updatedData: HouseInfo) => Promise<void>;
}

function HouseInfoBox({ houseInfo, onSave, onUpdate }: HouseInfoBoxProps) {
  const [isEditing, setIsEditing] = useState(false);
  const [isEnrolling, setIsEnrolling] = useState(false);
  const [editedInfo, setEditedInfo] = useState<HouseInfo>({
    id: null,
    name: "",
    address: "",
    number: "",
    introduction: "",
    score: null,
    loveCount: null,
  });

  useEffect(() => {
    if (houseInfo) {
      setEditedInfo(houseInfo);
      setIsEditing(false);
      setIsEnrolling(false);
    } else {
      // 게스트하우스 정보가 없는 사장님이 등록하러 들어왔을때
      setIsEditing(true);
      setIsEnrolling(true);
    }
  }, [houseInfo]);

  const handleInputChange = (field: keyof HouseInfo, value: string) => {
    setEditedInfo((prev) => ({ ...prev, [field]: value }));
  };

  const handleSave = async () => {
    if (!editedInfo.name || !editedInfo.address || !editedInfo.introduction) {
      alert("필수 입력창을 입력하세요.");
      return;
    }
    await onSave(editedInfo);
    setIsEditing(false);
    setIsEnrolling(false);
  };

  const handleUpdate = async () => {
    if (!editedInfo.name || !editedInfo.address || !editedInfo.introduction) {
      alert("필수 입력창을 입력하세요.");
      return;
    }
    await onUpdate(editedInfo);
    setIsEditing(false);
  };

  const toggleEditMode = () => {
    if (isEnrolling) {
      alert("게스트 하우스 등록을 해주세요.");
    } else {
      setIsEditing((prev) => !prev);
    }
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
              placeholder="게스트하우스 이름 (필수)"
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
                  placeholder="소개 (필수)"
                />
              </div>
              <div className={styles.house_info}>
                <p className={styles.house_info_left_text}>주소</p>
                <input
                  type="text"
                  value={editedInfo.address}
                  onChange={(e) => handleInputChange("address", e.target.value)}
                  className={styles.house_right_input}
                  placeholder="주소 (필수)"
                />
              </div>
              <div className={styles.house_info}>
                <p className={styles.house_info_left_text}>전화번호</p>
                <input
                  type="text"
                  value={editedInfo.number || ""}
                  onChange={(e) => handleInputChange("number", e.target.value)}
                  className={styles.house_right_input}
                  placeholder="전화번호 (선택사항)"
                />
              </div>
            </div>
            <div className={styles.button_container}>
              <button
                onClick={isEnrolling ? handleSave : handleUpdate}
                className={styles.save_button}
              >
                저장
              </button>
              <button onClick={toggleEditMode} className={styles.cancel_button}>
                취소
              </button>
            </div>
          </>
        ) : (
          <>
            <div className={styles.house_name_qr_box}>
              <p className={styles.house_name}>{houseInfo?.name}</p>
              <button className={styles.qr_box} type="button">
                <img src="/src/assets/image/qrcode.jpg" alt="qrcode_img" />
              </button>
            </div>
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
                  {houseInfo?.number || "없음"}
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
              <button onClick={toggleEditMode} className={styles.modify_button}>
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
