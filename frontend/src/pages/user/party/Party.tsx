import HomeButton from "../../../components/common/homeButton/HomeButton";
import HouseNameAndDate from "../../../components/common/houseNameAndDate/HouseNameAndDate";
import styles from "./styles/party.module.scss";

function Party() {
  return (
    <div className={styles.container}>
      <div className={styles.container_contents}>
        <HouseNameAndDate guestHouseName={"솔 게스트 하우스"} />
        <HomeButton />
        <div className={styles.house_info_box}>
          <div className={styles.house_info_lane}>
            <div className={styles.house_info_left}>소개</div>
            <div className={styles.house_info_right}>
              즐거운 분위기의 게스트 하우스
            </div>
          </div>
          <div className={styles.house_info_lane}>
            <div className={styles.house_info_left}>주소</div>
            <div className={styles.house_info_right}>
              경기도 부천시 토브빈 베이커리
            </div>
          </div>
          <div className={styles.house_info_lane}>
            <div className={styles.house_info_left}>전화번호</div>
            <div className={styles.house_info_right}>
              010-2222-3333
            </div>
          </div>
          <div className={styles.house_info_lane}>
            <div className={styles.house_info_left}>평점</div>
            <div className={styles.house_info_right}>
              ⭐ 4.56
            </div>
          </div>
          <div className={styles.house_info_lane}>
            <div className={styles.house_info_left}>짝 매칭 카운트</div>
            <div className={styles.house_info_right}>
              ❤️ 100
            </div>
          </div>
        </div>
        <div className={styles.button_box}>
          <button className={styles.house_party_button} type="button">파티방</button>
          <button className={styles.personal_chat_button} type="button">개인 채팅방</button>
          <button className={styles.love_button} type="button">짝 매칭</button>
        </div>
      </div>
    </div>
  );
}

export default Party;
