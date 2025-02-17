import styles from "./styles/houseManage.module.scss";
import { useState } from "react";

// 컴포넌트
import Header from "../../../components/common/header/Header";
import ProfileBox from "../../../components/common/profileBox/ProfileBox";
import MenuBox from "../../../components/common/menuBox/MenuBox";
import RadioButton from "../../../components/common/radio/RadioButton";
import GuestHouseTable from "./components/GuestHoustTable";
import NameSearch from "../../../components/common/search/NameSearch";

function HouseManage() {
  // 메뉴 탭 데이터
  const adminMenuTabs = [
    { text: "게스트 하우스 관리", isActive: true, path: "/admin/houseManage" },
    { text: "게스트 승인 관리", isActive: false, path: "/admin/houseApprove" },
    { text: "마이페이지", isActive: false, path: "#" },
  ];

  // 최신등록 순서 상태 - 리뷰많은 순도 기획하였으나 현재는 리뷰가 미구현
  const [selectedOption, setSelectedOption] = useState<boolean>(false);
  // 이름 검색 조건 상태
  const [name, setName] = useState<string>("");

  // 라디오 버튼 상태 함수
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
            <p className={styles.manage_title}>게스트 하우스 관리</p>
            <div className={styles.manage_box}>
              <div className={styles.search_box}>
                <div className={styles.radio_box}>
                  <RadioButton
                    label="많은 리뷰 순"
                    name="reviewOrder"
                    value={true}
                    checked={selectedOption === true}
                    onChange={handleRadioChange}
                  />
                  <RadioButton
                    label="최근 등록 순"
                    name="reviewOrder"
                    value={false}
                    checked={selectedOption === false}
                    onChange={handleRadioChange}
                  />
                </div>
                <NameSearch onSearch={handleSearch} />
              </div>
              <GuestHouseTable isMostReviews={selectedOption} name={name} />
            </div>
          </div>
        </div>
      </div>
    </>
  );
}

export default HouseManage;
