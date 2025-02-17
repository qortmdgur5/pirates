import styles from "./styles/managerApprove.module.scss";
import { useState } from "react";

// 컴포넌트
import Header from "../../../components/common/header/Header";
import ProfileBox from "../../../components/common/profileBox/ProfileBox";
import MenuBox from "../../../components/common/menuBox/MenuBox";
import RadioButton from "../../../components/common/radio/RadioButton";
import ManagerApproveTable from "./components/ManagerApproveTable";
import NameSearch from "../../../components/common/search/NameSearch";

function ManagerApprove() {
  // 메뉴 탭 데이터
  const managerMenuTabs = [
    {
      text: "게스트 하우스 관리",
      isActive: false,
      path: "/owner/manageHouse",
    },
    {
      text: "매니저 등록 관리",
      isActive: true,
      path: "/owner/managerApprove",
    },
    { text: "파티방 관리", isActive: false, path: "/manager/manageParty" },
  ];

  // 최신 순 오래된 순 상태
  const [selectedOption, setSelectedOption] = useState<boolean>(false);
  const [name, setName] = useState<string>(""); // 매니저 이름 검색 조건

  // 라디오 버튼 함수
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
          <MenuBox menuTabs={managerMenuTabs} />
        </div>
        <div className={styles.house_manage_right_box}>
          <div className={styles.manage_container}>
            <p className={styles.manage_title}>매니저 등록 관리</p>
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
              <ManagerApproveTable
                isOldestOrders={selectedOption}
                name={name}
              />
            </div>
          </div>
        </div>
      </div>
    </>
  );
}

export default ManagerApprove;
