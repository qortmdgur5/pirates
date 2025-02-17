import { useEffect, useState } from "react";
import axios from "axios";
import Header from "../../../components/common/header/Header";
import MenuBox from "../../../components/common/menuBox/MenuBox";
import ProfileBox from "../../../components/common/profileBox/ProfileBox";
import HouseInfoBox from "./components/HouseInfoBox";
import styles from "./styles/manageHouse.module.scss";
import { useRecoilState, useRecoilValue } from "recoil";
import { accomoAtoms, authAtoms } from "../../../atoms/authAtoms";

interface Accommodation {
  id: number | null;
  name: string;
  address: string;
  number?: string;
  introduction: string;
  score?: number | null;
  loveCount?: number | null;
}

function ManageHouse() {
  const [houseInfo, setHouseInfo] = useState<Accommodation | null>(null);
  const [loading, setLoading] = useState(true); // 로딩 상태 추가
  const [accomoAtom, setAccomoAtom] = useRecoilState(accomoAtoms); // 숙소 정보 상태
  const user = useRecoilValue(authAtoms);
  const ownerId = user.userId; // 로그인된 사장님 id 값
  const accomodationId = accomoAtom.accomodation_id; // 수정할 숙소 id 값
  const token = user.token; // 로그인 정보 token

  const managerMenuTabs = [
    {
      text: "게스트 하우스 관리",
      isActive: true,
      path: "/owner/manageHouse",
    },
    {
      text: "매니저 등록 관리",
      isActive: false,
      path: "/owner/managerApprove",
    },
    { text: "파티방 관리", isActive: false, path: "/manager/manageParty" },
  ];

  const fetchAccommodation = async (id: number) => {
    try {
      const response = await axios.get<{ data: Accommodation[] }>(
        `/api/owner/accomodation/${id}`,
        {
          params: { skip: 0, limit: 10, token: token },
          headers: { accept: "application/json" },
        }
      );

      const houseData = response.data.data[0];
      if (houseData) {
        setHouseInfo(response.data.data[0]);
        setAccomoAtom((prevState) => ({
          ...prevState,
          accomodation_name: houseData.name,
          accomodation_id: houseData.id,
        }));
      }
    } catch (error) {
      console.error("데이터를 불러오지 못했습니다.", error);
    } finally {
      setLoading(false); // 로딩 상태 해제
    }
  };

  useEffect(() => {
    if (ownerId) fetchAccommodation(ownerId);
  }, []);

  const saveAccommodation = async (newData: Accommodation) => {
    try {
      await axios.post(
        "/api/owner/accomodation",
        {
          ...newData,
          id: ownerId,
        },
        {
          params: { token }, // token을 쿼리 파라미터로 추가
        }
      );
      if (ownerId) fetchAccommodation(ownerId);
    } catch (error) {
      console.error("데이터 저장에 실패했습니다.", error);
    }
  };

  const updateAccommodation = async (updatedData: Accommodation) => {
    try {
      await axios.put(
        `/api/owner/accomodation/${accomodationId}`,
        {
          ...updatedData,
        },
        {
          params: { token }, // token을 쿼리 파라미터로 추가
        }
      );
      if (ownerId) fetchAccommodation(ownerId);
    } catch (error) {
      console.error("데이터 수정에 실패했습니다.", error);
    }
  };

  return (
    <>
      <Header />
      <div className={styles.container}>
        <div className={styles.house_manage_left_box}>
          <ProfileBox />
          <MenuBox menuTabs={managerMenuTabs} />
        </div>
        <div className={styles.manage_right_box}>
          <div className={styles.manage_container}>
            <p className={styles.manage_title}>게스트하우스 관리</p>
            {loading ? (
              <p>로딩 중...</p>
            ) : (
              <HouseInfoBox
                houseInfo={houseInfo}
                onSave={saveAccommodation}
                onUpdate={updateAccommodation}
                accomodationId={accomodationId}
                token={token}
              />
            )}
          </div>
        </div>
      </div>
    </>
  );
}

export default ManageHouse;
