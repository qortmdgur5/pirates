import BackButton from "../../../components/common/backButton/BackButton";
import HomeButton from "../../../components/common/homeButton/HomeButton";
import HouseNameAndDate from "../../../components/common/houseNameAndDate/HouseNameAndDate";
import TeamDropDown from "../../../components/common/teamDropDown/TeamDropDown";
import styles from "./styles/partyUserList.module.scss";

function PartyUserList() {
  return (
    <div className={styles.container}>
      <div className={styles.container_contents}>
        <HouseNameAndDate guestHouseName={"솔 게스트 하우스"} />
        <div className={styles.home_and_back_box}>
          <HomeButton />
          <BackButton />
        </div>
        <div className={styles.search_and_participant_box}>
          <div className={styles.search_box}>
            <input
              className={styles.name_input}
              type="text"
              placeholder="검색"
            />
            <img src="/src/assets/image/glasses.png" alt="search_icon_img" />
          </div>
          <div className={styles.participant_box}>
            <p className={styles.participant_text}>참여자수</p>
            <p className={styles.participant_status}>98/100</p>
          </div>
        </div>
        <TeamDropDown team={"1조"} />
      </div>
    </div>
  );
}

export default PartyUserList;
