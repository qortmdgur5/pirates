import styles from "./styles/houseManage.module.scss";

// 컴포넌트
import Header from "../../../components/common/header/Header";
import ProfileBox from "../../../components/common/profileBox/ProfileBox";
import MenuBox from "../../../components/common/menuBox/MenuBox";

function HouseManage() {
  // 메뉴 탭 데이터
  const menuTabs = [
    { text: "게스트 하우스 관리", isActive: true },
    { text: "예약 관리", isActive: false },
    { text: "숙소 관리", isActive: false },
  ];

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
          <div className={styles.house_manage_menu_box}>
            {/* MenuBox에 menuTabs 배열을 props로 전달 */}
            <MenuBox menuTabs={menuTabs} />
          </div>
        </div>
        <div className={styles.house_manage_right_box}></div>
      </div>
    </>
  );
}

export default HouseManage;
