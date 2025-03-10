import { useEffect, useState } from "react";
import styles from "./styles/houseInfoBox.module.scss";
import axios from "axios";
import qr_img from "../../../../assets/image/qrcode.jpg";
import kakaoPay_img from "../../../../assets/image/kakao_pay_button.png";
const SECRET_KEY = import.meta.env.VITE_KAKAO_SECRET_KEY;
const CID = import.meta.env.VITE_KAKAO_CID;

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
  accomodationId: number | null;
  token: string | null;
}

function HouseInfoBox({
  houseInfo,
  onSave,
  onUpdate,
  accomodationId,
  token,
}: HouseInfoBoxProps) {
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

  // QR 코드 다운로드 API
  const downloadQRCode = async () => {
    try {
      // API 호출하여 QR 코드 이미지 파일을 가져옵니다
      const response = await axios.get(
        `/api/manager/accomodation/qr/${accomodationId}`,
        {
          params: { token },
          responseType: "blob", // 응답을 blob으로 처리
        }
      );

      // Blob 객체를 사용하여 다운로드 가능한 URL 생성
      const url = window.URL.createObjectURL(response.data);

      // 다운로드 링크를 생성하여 클릭 이벤트를 트리거합니다
      const a = document.createElement("a");
      a.href = url;
      a.download = "qr_code.png"; // 다운로드될 파일 이름을 설정합니다
      a.click();

      // 메모리 해제
      window.URL.revokeObjectURL(url);
    } catch (error) {
      console.error("파일 다운로드 중 오류 발생:", error);
    }
  };

  // Kakao pay API
  const handlePayment = async () => {
    try {
      const response = await axios.post(
        "/kakao-pay",
        {
          cid: CID,
          partner_order_id: "partner_order_id",
          partner_user_id: "partner_user_id",
          item_name: "해적 1달 구독권",
          quantity: 1,
          total_amount: 19000,
          tax_free_amount: 0,
          approval_url: "http://localhost:5173/owner/manageHouse",
          fail_url: "http://localhost:5173/owner/manageHouse",
          cancel_url: "http://localhost:5173/owner/manageHouse",
        },
        {
          headers: {
            Authorization: `SECRET_KEY ${SECRET_KEY}`,
            "Content-Type": "application/json",
          },
        }
      );

      // 결제 페이지로 리다이렉트
      if (response.data.next_redirect_pc_url) {
        window.location.href = response.data.next_redirect_pc_url;
      } else {
        alert("결제 페이지를 불러올 수 없습니다.");
      }
    } catch (error) {
      console.error("결제 요청 실패:", error);
      alert("결제 요청 중 오류가 발생했습니다.");
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
              <button
                className={styles.kakao_pay_button}
                type="button"
                onClick={handlePayment}
              >
                <img src={kakaoPay_img} alt="kakaoPay_img" />
              </button>
              <p className={styles.house_name}>{houseInfo?.name}</p>
              <button
                className={styles.qr_box}
                type="button"
                onClick={downloadQRCode}
              >
                <img src={qr_img} alt="qrcode_img" />
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
