import styles from "./styles/managerApprove.module.scss"
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
    { text: "게스트 하우스 관리", isActive: false, path: "/manager/houseRegister" },
    { text: "매니저 등록 관리", isActive: true, path: "/manager/managerApprove" },
    { text: "파티방 관리", isActive: false, path: "/manager/manageParty" },
    { text: "마이페이지", isActive: false, path: "#" },
  ];

  const [selectedOption, setSelectedOption] = useState("asdOrders");

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
            <p className={styles.manage_title}>매니저 등록 관리</p>
            <div className={styles.manage_box}>
              <div className={styles.search_box}>
                <div className={styles.radio_box}>
                  <RadioButton
                    label="가나다 순"
                    name="asdOrder"
                    value="asdOrders"
                    checked={selectedOption === "asdOrders"}
                    onChange={setSelectedOption}
                  />
                  <RadioButton
                    label="최근 등록 순"
                    name="recentlyRegistered"
                    value="recentlyRegistered"
                    checked={selectedOption === "recentlyRegistered"}
                    onChange={setSelectedOption}
                  />
                </div>
                <NameSearch />
              </div>
              <ManagerApproveTable />
            </div>
          </div>
        </div>
      </div>
    </>
  );
}

export default ManagerApprove;
