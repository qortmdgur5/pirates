import styles from "./styles/houseApprove.module.scss"
import { useState } from "react";

// 컴포넌트
import Header from "../../../components/common/header/Header";
import RadioButton from "../../../components/common/radio/RadioButton";
import ProfileBox from "../../../components/common/profileBox/ProfileBox";
import MenuBox from "../../../components/common/menuBox/MenuBox";
import HouseApproveTable from "./components/HouseApproveTable";

function HouseApprove() {
  // 메뉴 탭 데이터
  const adminMenuTabs = [
    { text: "게스트 하우스 관리", isActive: false },
    { text: "게스트 승인 관리", isActive: true },
    { text: "마이페이지", isActive: false },
  ];

  const [selectedOption, setSelectedOption] = useState("asdOrders");

  return (
    <>
      <Header />
      <div className={styles.container}>
        <div className={styles.house_manage_left_box}>
          <ProfileBox
            name="관리자님"
            imgSrc="/src/assets/image/woman_icon_img.png"
            userId="Pirates"
          />
          <MenuBox menuTabs={adminMenuTabs} />
        </div>
        <div className={styles.house_manage_right_box}>
          <div className={styles.manage_container}>
            <p className={styles.manage_title}>게스트 승인 관리</p>
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
              </div>
              <HouseApproveTable />
            </div>
          </div>
        </div>
      </div>
    </>
  );
}

export default HouseApprove;
