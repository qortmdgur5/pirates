import Header from "../../../components/common/header/Header";
import MenuBox from "../../../components/common/menuBox/MenuBox";
import ProfileBox from "../../../components/common/profileBox/ProfileBox";
import ParticipantTable from "./components/ParticipantTable";
import ReservationStatusTable from "./components/ReservationStatusTable";
import styles from "./styles/managePartyDetail.module.scss";

function ManagePartyDetail() {
  // 메뉴 탭 데이터
  const managerMenuTabs = [
    { text: "게스트 하우스 등록", isActive: false },
    { text: "매니저 등록 관리", isActive: false },
    { text: "파티방 관리", isActive: false },
    { text: "마이페이지", isActive: true },
  ];
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
            <p className={styles.manage_title}>예약 현황</p>
            <div className={styles.manage_box}>
              <ReservationStatusTable />
            </div>
            <p className={styles.manage_title}>참석자 명단</p>
            <div className={styles.manage_box}>
              <button className={styles.blue_button}>등록</button>
              <ParticipantTable />
            </div>
          </div>
        </div>
      </div>
    </>
  );
}

export default ManagePartyDetail;
