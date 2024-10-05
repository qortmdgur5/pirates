import { useState } from "react";

// 컴포넌트
import Header from "../../../components/common/header/Header";
import MenuBox from "../../../components/common/menuBox/MenuBox";
import ProfileBox from "../../../components/common/profileBox/ProfileBox";
import RadioButton from "../../../components/common/radio/RadioButton";
import styles from "./styles/manageParty.module.scss";
import NameSearch from "../../../components/common/search/NameSearch";
import ManagePartyTable from "./components/ManagePartyTable";

function ManageParty() {
  // 메뉴 탭 데이터
  const managerMenuTabs = [
    { text: "게스트 하우스 등록", isActive: false },
    { text: "매니저 등록 관리", isActive: false },
    { text: "파티방 관리", isActive: true },
    { text: "마이페이지", isActive: false },
  ];

  const [selectedOption, setSelectedOption] = useState("recentlyRegistered");

  return (
    <>
      <Header />
      <div className={styles.container}>
        <div className={styles.house_manage_left_box}>
          <ProfileBox
            name="매니저님"
            imgSrc="/src/assets/image/woman_icon_img.png"
            userId="sky1004"
          />
          <MenuBox menuTabs={managerMenuTabs} />
        </div>
        <div className={styles.house_manage_right_box}>
          <div className={styles.manage_container}>
            <p className={styles.manage_title}>파티방 관리</p>
            <div className={styles.manage_box}>
              <div className={styles.search_box}>
                <div className={styles.radio_box}>
                  <RadioButton
                    label="최근 등록 순"
                    name="recentlyRegistered"
                    value="recentlyRegistered"
                    checked={selectedOption === "recentlyRegistered"}
                    onChange={setSelectedOption}
                  />
                  <RadioButton
                    label="오래된 순"
                    name="oldRegistered"
                    value="oldRegistered"
                    checked={selectedOption === "oldRegistered"}
                    onChange={setSelectedOption}
                  />
                </div>
                <NameSearch />
              </div>
              <ManagePartyTable />
              <button className={styles.blue_button}>파티방 개설하기</button>
            </div>
          </div>
        </div>
      </div>
    </>
  );
}

export default ManageParty;
