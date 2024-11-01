import { useEffect, useState } from "react";
import Header from "../../../components/common/header/Header";
import MenuBox from "../../../components/common/menuBox/MenuBox";
import ProfileBox from "../../../components/common/profileBox/ProfileBox";
import HouseInfoBox from "./components/HouseInfoBox";
import styles from "./styles/houseRegister.module.scss";
import axios from "axios";

interface Accommodation {
  id: number;
  name: string;
  address: string;
  number: string;
  introduction: string;
  score: number | null;
  loveCount: number | null;
}

function ManageHouse() {
  const [houseInfo, setHouseInfo] = useState<Accommodation | null>(null); // 게스트 하우스 정보 상태
  const ownerId = 1; // 추후 아톰으로 관리하여 로그인한 사장님의 id 값 저장해서 사용

  // 메뉴 탭 데이터
  const managerMenuTabs = [
    {
      text: "게스트 하우스 관리",
      isActive: true,
      path: "/manager/manageHouse",
    },
    {
      text: "매니저 등록 관리",
      isActive: false,
      path: "/manager/managerApprove",
    },
    { text: "파티방 관리", isActive: false, path: "/manager/manageParty" },
    { text: "마이페이지", isActive: false, path: "#" },
  ];

  // 사장님 & 매니저 게스트 하우스 정보 가져오기 API 호출
  useEffect(() => {
    const fetchAccommodation = async (id: number) => {
      try {
        const response = await axios.get<Accommodation[]>(
          `/api/owner/accomodation/${id}`,
          {
            params: { skip: 0, limit: 10 },
            headers: { accept: "application/json" },
          }
        );
        setHouseInfo(response.data[0]); // 첫 번째 항목만 저장, 배열이지만 현재는 한명의 사장에게 하나의 게스트하우스라고 가정
      } catch (error) {
        console.error("데이터를 불러오지 못했습니다.", error);
      }
    };

    fetchAccommodation(ownerId);
  }, []);

  return (
    <>
      <Header />
      <div className={styles.container}>
        <div className={styles.house_manage_left_box}>
          <ProfileBox
            name="매니저님"
            imgSrc="/src/assets/image/man_icon_img.png"
            userId="sky1004"
          />
          <MenuBox menuTabs={managerMenuTabs} />
        </div>
        <div className={styles.manage_right_box}>
          <div className={styles.manage_container}>
            <p className={styles.manage_title}>게스트하우스 관리</p>
            {houseInfo && <HouseInfoBox houseInfo={houseInfo} />}
          </div>
        </div>
      </div>
    </>
  );
}

export default ManageHouse;
