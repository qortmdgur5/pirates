import BackButton from "../../../components/common/backButton/BackButton";
import HomeButton from "../../../components/common/homeButton/HomeButton";
import HouseNameAndDate from "../../../components/common/houseNameAndDate/HouseNameAndDate";
import UserListCard from "./components/UserListCard";
import styles from "./styles/loveSelect.module.scss";

function LoveSelect() {
  return (
    <div className={styles.container}>
      <div className={styles.container_contents}>
        <HouseNameAndDate guestHouseName={"솔 게스트 하우스 짝매칭"} />
        <div className={styles.home_and_back_box}>
          <HomeButton />
          <BackButton navigateTo="/user/party"/>
        </div>
        <div className={styles.team_and_time_box}>
          <p className={styles.team_text}>1조 짝 매칭</p>
          <p className={styles.time_box}>05:00</p>
        </div>
        <div className={styles.love_select_container}>
          <div className={styles.info_intro_box}>
            <p className={styles.img_intro}>이미지</p>
            <p className={styles.name_and_gender_intro}>이름 및 성별</p>
            <p className={styles.check_intro}>체크</p>
            <p className={styles.rank_intro}>순위</p>
          </div>
          <div className={styles.user_list_box}>
            <UserListCard />
            <UserListCard />
          </div>
        </div>
        <div className={styles.love_match_container}></div>
      </div>
    </div>
  );
}

export default LoveSelect;
