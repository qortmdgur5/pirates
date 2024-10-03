import styles from "./styles/profileBox.module.scss";

interface ProfileBoxProps {
  name: string;
  imgSrc: string;
  userId: string;
}

function ProfileBox({ name, imgSrc, userId }: ProfileBoxProps) {
  return (
    <div className={styles.house_manage_profile_box}>
      <p className={styles.houes_manage_profile_text_1}>
        {name}
        <br />
        <span>반갑습니다 :)</span>
      </p>
      <div className={styles.house_manage_profile_img_box}>
        <img src={imgSrc} alt="profile_img" />
      </div>
      <p className={styles.house_manage_profile_id}>{userId}</p>
    </div>
  );
}

export default ProfileBox;
