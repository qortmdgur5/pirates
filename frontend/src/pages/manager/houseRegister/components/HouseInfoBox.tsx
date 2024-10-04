import styles from "./styles/houseInfoBox.module.scss"

function HouseInfoBox() {
  return (
    <div className={styles.container}>
      <div className={styles.house_info_container}>
        <p className={styles.house_name}>부산 솔게스트 하우스</p>
        <div className={styles.house_info_box}>
          <div className={styles.house_info}>
            <p className={styles.houes_info_left_text}>소개</p>
            <p className={styles.houes_info_right_text}>즐거운 분위기의 게스트 하우스</p>
          </div>
          <div className={styles.house_info}>
            <p className={styles.houes_info_left_text}>주소</p>
            <p className={styles.houes_info_right_text}>경기도 부천시 토브빈 베이커리</p>
          </div>
          <div className={styles.house_info}>
            <p className={styles.houes_info_left_text}>전화번호</p>
            <p className={styles.houes_info_right_text}>010-0000-0000</p>
          </div>
          <div className={styles.house_info}>
            <p className={styles.houes_info_left_text}>평점</p>
            <p className={styles.houes_info_right_text}>⭐4.56</p>
          </div>
          <div className={styles.house_info}>
            <p className={styles.houes_info_left_text}>짝 매칭 카운트</p>
            <p className={styles.houes_info_right_text}>❤️100</p>
          </div>
        </div>
        <div className={styles.button_container}>
          <button className={styles.register_button}>등록</button>
          <button className={styles.modify_button}>수정</button>
        </div>
      </div>
    </div>
  )
}

export default HouseInfoBox