import styles from "./styles/houseApprove.module.scss";
import { useState } from "react";

// 컴포넌트
import Header from "../../../components/common/header/Header";
import RadioButton from "../../../components/common/radio/RadioButton";
import ProfileBox from "../../../components/common/profileBox/ProfileBox";
import MenuBox from "../../../components/common/menuBox/MenuBox";
import HouseApproveTable from "./components/HouseApproveTable";
import NameSearch from "../../../components/common/search/NameSearch";

function HouseApprove() {
  // 메뉴 탭 데이터
  const adminMenuTabs = [
    { text: "게스트 하우스 관리", isActive: false, path: "/admin/houseManage" },
    { text: "게스트 승인 관리", isActive: true, path: "/admin/houseApprove" },
    { text: "마이페이지", isActive: false, path: "#" },
  ];

  const [selectedOption, setSelectedOption] = useState<boolean>(false); // 오래된 순 최신 순 상태
  const [name, setName] = useState<string>(""); // 이름 검색용 상태

  // 최근순 오래된 순 라디오 버튼 상태 함수
  const handleRadioChange = (value: boolean) => {
    setSelectedOption(value);
  };

  // 이름 검색 함수
  const handleSearch = (searchName: string) => {
    setName(searchName);
  };
  

  return (
    <>
      <Header />
      <div className={styles.container}>
        <div className={styles.house_manage_left_box}>
          <ProfileBox />
          <MenuBox menuTabs={adminMenuTabs} />
        </div>
        <div className={styles.house_manage_right_box}>
          <div className={styles.manage_container}>
            <p className={styles.manage_title}>게스트 승인 관리</p>
            <div className={styles.manage_box}>
              <div className={styles.search_box}>
                <div className={styles.radio_box}>
                  <RadioButton
                    label="최근 등록 순"
                    name="recentlyRegistered"
                    value={false}
                    checked={selectedOption === false}
                    onChange={handleRadioChange}
                  />
                  <RadioButton
                    label="오래된 순"
                    name="oldestOrders"
                    value={true}
                    checked={selectedOption === true}
                    onChange={handleRadioChange}
                  />
                </div>
                <NameSearch onSearch={handleSearch} />
              </div>
              <HouseApproveTable isOldestOrders={selectedOption} name={name} />
            </div>
          </div>
        </div>
      </div>
    </>
  );
}

export default HouseApprove;
