import styles from "./styles/houseManage.module.scss";
import { useState } from "react";

// 컴포넌트
import Header from "../../../components/common/header/Header";
import ProfileBox from "../../../components/common/profileBox/ProfileBox";
import MenuBox from "../../../components/common/menuBox/MenuBox";
import RadioButton from "../../../components/common/radio/RadioButton";
import GuestHouseTable from "./components/GuestHoustTable";

function HouseManage() {
  // 메뉴 탭 데이터
  const adminMenuTabs = [
    { text: "게스트 하우스 관리", isActive: true },
    { text: "게스트 승인 관리", isActive: false },
    { text: "마이페이지", isActive: false },
  ];

  const [selectedOption, setSelectedOption] = useState("manyReviews");

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
          {/* MenuBox에 menuTabs 배열을 props로 전달 */}
          <MenuBox menuTabs={adminMenuTabs} />
        </div>
        <div className={styles.house_manage_right_box}>
          <div className={styles.manage_container}>
            <p className={styles.manage_title}>게스트 하우스 관리</p>
            <div className={styles.manage_box}>
              <div className={styles.search_box}>
                <div className={styles.radio_box}>
                  <RadioButton
                    label="많은 리뷰 순"
                    name="reviewOrder"
                    value="manyReviews"
                    checked={selectedOption === "manyReviews"}
                    onChange={setSelectedOption}
                  />
                  <RadioButton
                    label="최근 등록 순"
                    name="reviewOrder"
                    value="recentlyRegistered"
                    checked={selectedOption === "recentlyRegistered"}
                    onChange={setSelectedOption} // onChange 함수로 상태 변경
                  />
                </div>
              </div>
              <GuestHouseTable />
            </div>
          </div>
        </div>
      </div>
    </>
  );
}

export default HouseManage;
