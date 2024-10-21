import Header from "../../../components/common/header/Header";
import MenuBox from "../../../components/common/menuBox/MenuBox";
import ProfileBox from "../../../components/common/profileBox/ProfileBox";
import HouseInfoBox from "./components/HouseInfoBox";
import styles from "./styles/houseRegister.module.scss";

function HouseRegister() {
  // 메뉴 탭 데이터
  const managerMenuTabs = [
    { text: "게스트 하우스 등록", isActive: true },
    { text: "매니저 등록 관리", isActive: false },
    { text: "파티방 관리", isActive: false },
    { text: "마이페이지", isActive: false },
  ];
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
            <HouseInfoBox />
          </div>
        </div>
      </div>
    </>
  );
}

export default HouseRegister;
