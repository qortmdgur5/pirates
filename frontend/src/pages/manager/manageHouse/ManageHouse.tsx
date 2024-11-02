import { useEffect, useState } from "react";
import axios from "axios";
import Header from "../../../components/common/header/Header";
import MenuBox from "../../../components/common/menuBox/MenuBox";
import ProfileBox from "../../../components/common/profileBox/ProfileBox";
import HouseInfoBox from "./components/HouseInfoBox";
import styles from "./styles/houseRegister.module.scss";

interface Accommodation {
  name: string;
  address: string;
  number?: string;
  introduction: string;
  score?: number | null;
  loveCount?: number | null;
}

function ManageHouse() {
  const [houseInfo, setHouseInfo] = useState<Accommodation | null>(null);
  const ownerId = 14; // 로그인된 사장님 id 값
  const accomodationId = 38; // 수정할 숙소 id 값 

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

  const fetchAccommodation = async (id: number) => {
    try {
      const response = await axios.get<Accommodation[]>(
        `/api/owner/accomodation/${id}`,
        {
          params: { skip: 0, limit: 10 },
          headers: { accept: "application/json" },
        }
      );
      setHouseInfo(response.data[0]);
    } catch (error) {
      console.error("데이터를 불러오지 못했습니다.", error);
    }
  };

  useEffect(() => {
    fetchAccommodation(ownerId);
  }, []);

  const saveAccommodation = async (newData: Accommodation) => {
    try {
      await axios.post("/api/owner/accomodation", { ...newData, id: ownerId });
      fetchAccommodation(ownerId);
    } catch (error) {
      console.error("데이터 저장에 실패했습니다.", error);
    }
  };

  const updateAccommodation = async (updatedData: Accommodation) => {
    try {
      await axios.put(`/api/owner/accomodation/${accomodationId}`, updatedData);
      fetchAccommodation(ownerId);
    } catch (error) {
      console.error("데이터 수정에 실패했습니다.", error);
    }
  };

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
            <HouseInfoBox
              houseInfo={houseInfo}
              onSave={saveAccommodation}
              onUpdate={updateAccommodation}
            />
          </div>
        </div>
      </div>
    </>
  );
}

export default ManageHouse;
