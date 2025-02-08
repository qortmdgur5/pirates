import axios from "axios";
import styles from "./styles/userListCard.module.scss";
import { useState } from "react";

interface MatchUserListCardProps {
  id: number; // 해당 유저 id 값
  userName: string; // 유저 이름
  gender: boolean; // true: 남자, false: 여자
  isChecked: boolean; // 체크 상태
  onSelect: () => void; // 선택 시 호출되는 함수
  userId: number | null; // 본인 id 값
  partyId: number | null; // 파티 id 값
  confirm: boolean; // 짝 확정지었는지 확인 state
  setConfirm: (vlaue: boolean) => void; // confirm state Set hook
}

function UserListCard({
  id,
  userName,
  gender,
  isChecked,
  onSelect,
  userId,
  partyId,
  confirm,
  setConfirm,
}: MatchUserListCardProps) {
  const [loading, setLoading] = useState(false);

  const handleSelect = async () => {
    if (loading) return; // 로딩 중이면 중복 호출 방지

    // 알림창을 통해 사용자에게 확인 요청
    const confirmSelection = window.confirm(
      `${userName} 님을 선택하시겠습니까?`
    );

    if (!confirmSelection) {
      return; // 사용자가 "취소"를 클릭하면 아무 동작도 하지 않음
    }

    setLoading(true);

    try {
      // API 호출: 짝 매칭 선택
      await axios.post("/api/user/match/select", {
        party_id: partyId,
        user_id_1: userId,
        user_id_2: id,
      });

      // 매칭 성공
      setConfirm(true); // 확정 confirm state 변경
      console.log("매칭 성공");
    } catch (err) {
      console.error("매칭 실패:", err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className={styles.container}>
      <div className={styles.img_box}>
        <div className={styles.img_info}>
          <img
            src={
              gender
                ? "/src/assets/image/man_icon_img.png"
                : "/src/assets/image/woman_icon_img.png"
            }
            alt="user_img_png"
          />
        </div>
      </div>
      <div className={styles.name_and_gender_box}>
        <div className={styles.name_and_gender_info}>
          <p className={styles.name_text}>{userName}</p>
          <div className={styles.gender_box}>
            <img
              src={
                gender
                  ? "/src/assets/image/gender_man.png"
                  : "/src/assets/image/gender_woman.png"
              }
              alt="gender_img_png"
            />
          </div>
        </div>
      </div>
      <button
        className={styles.check_box}
        onClick={onSelect}
        disabled={confirm}
      >
        <img
          src={
            isChecked
              ? "/src/assets/image/check.png"
              : "/src/assets/image/uncheck.png"
          }
          alt="check_img"
        />
      </button>

      <div className={styles.select_box}>
        {isChecked && !confirm && (
          <button
            className={styles.select_button}
            type="button"
            onClick={handleSelect}
          >
            선택
          </button>
        )}

        {isChecked && confirm && (
          <button className={styles.confirm_button} type="button" disabled>
            확정
          </button>
        )}
      </div>
    </div>
  );
}

export default UserListCard;
