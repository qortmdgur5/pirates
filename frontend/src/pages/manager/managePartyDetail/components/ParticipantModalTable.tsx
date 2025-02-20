import React, { useState } from "react";
import axios from "axios";
import styles from "./styles/participantModalTable.module.scss";

interface ParticipantData {
  id: number;
  name: string;
  phone: string;
  age: number | null; // 빈 값 허용
  gender: boolean; // 남성: true, 여성: false, 필수 값
  mbti: string | null; // 빈 값 허용
  region: string | null; // 빈 값 허용
}

interface ParticipantModalTableProps {
  partyId: number;
  onRegister: () => void;
  participant: number;
  setParticipantCount: React.Dispatch<React.SetStateAction<number>>;
  token: string | null;
}

function ParticipantModalTable({
  partyId,
  onRegister,
  setParticipantCount,
  token,
}: ParticipantModalTableProps) {
  const initialParticipantData: ParticipantData = {
    id: partyId,
    name: "",
    phone: "",
    age: null,
    gender: true,
    mbti: null,
    region: null,
  };

  // 참석인원 상태관리
  const [participantData, setParticipantData] = useState<ParticipantData>(
    initialParticipantData
  );

  // 입력값이 변경될 때 상태 업데이트 함수
  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setParticipantData((prevData) => ({
      ...prevData,
      [name]: name === "age" ? (value ? Number(value) : null) : value || null, // age는 숫자, 나머지는 빈 문자열을 null로
    }));
  };

  // 성별 선택을 위한 드롭다운 변경 함수
  const handleGenderChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
    setParticipantData((prevData) => ({
      ...prevData,
      gender: e.target.value === "true", // true는 남성, false는 여성
    }));
  };

  // 등록하기 버튼 클릭 시 데이터 전송
  const handleSubmit = async () => {
    try {
      const response = await axios.post(
        "/api/manager/participant",
        participantData,
        {
          params: { token },
          headers: { "Content-Type": "application/json" },
        }
      );
      console.log("참가자가 성공적으로 등록되었습니다:", response.data);

      // 등록 후 초기값으로 리셋
      setParticipantData(initialParticipantData);
      setParticipantCount((prev) => prev + 1); // 참가자 수 증가
      onRegister();
    } catch (error) {
      console.error("참가자 등록 실패:", error);
    }
  };

  return (
    <div className={styles.table_container}>
      <table className={styles.participant_modal_table}>
        <thead>
          <tr>
            <th className={styles.th_left_blank}></th>
            <th className={styles.text_center}>이름</th>
            <th className={styles.text_center}>연락처</th>
            <th className={styles.text_center}>나이</th>
            <th className={styles.text_center}>성별</th>
            <th className={styles.text_center}>MBTI</th>
            <th className={styles.text_center}>지역</th>
            <th className={styles.th_right_blank}></th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td className={styles.td_left_black}></td>
            <td className={styles.modal_input}>
              <input
                type="text"
                name="name"
                placeholder="이름"
                value={participantData.name}
                onChange={handleInputChange}
              />
            </td>
            <td className={styles.modal_input}>
              <input
                type="text"
                name="phone"
                placeholder="연락처"
                value={participantData.phone}
                onChange={handleInputChange}
              />
            </td>
            <td className={styles.modal_input}>
              <input
                type="number"
                name="age"
                placeholder="나이"
                value={participantData.age ?? ""}
                onChange={handleInputChange}
              />
            </td>
            <td className={styles.modal_input}>
              <select
                name="gender"
                value={participantData.gender.toString()}
                onChange={handleGenderChange}
              >
                <option value="true">남성</option>
                <option value="false">여성</option>
              </select>
            </td>
            <td className={styles.modal_input}>
              <input
                type="text"
                name="mbti"
                placeholder="MBTI"
                value={participantData.mbti ?? ""}
                onChange={handleInputChange}
              />
            </td>
            <td className={styles.modal_input}>
              <input
                type="text"
                name="region"
                placeholder="지역"
                value={participantData.region ?? ""}
                onChange={handleInputChange}
              />
            </td>
            <td className={styles.td_right_black}></td>
          </tr>
        </tbody>
      </table>
      <div className={styles.modal_blue_button_box}>
        <button className={styles.blue_button} onClick={handleSubmit}>
          등록하기
        </button>
      </div>
    </div>
  );
}

export default ParticipantModalTable;
