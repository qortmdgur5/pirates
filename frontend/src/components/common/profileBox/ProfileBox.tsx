import { useRecoilValue } from "recoil";
import styles from "./styles/profileBox.module.scss";
import { authAtoms } from "../../../atoms/authAtoms";

function ProfileBox() {
  const { username, role } = useRecoilValue(authAtoms);

  // role에 따라 이름 설정
  const name = (() => {
    switch (role) {
      case "SUPER_ADMIN":
        return "관리자님";
      case "ROLE_AUTH_MANAGER":
      case "ROLE_NOTAUTH_MANAGER":
        return "매니저님";
      case "ROLE_AUTH_OWNER":
      case "ROLE_NOTAUTH_OWNER":
        return "사장님";
      default:
        return "사용자님";
    }
  })();

  return (
    <div className={styles.house_manage_profile_box}>
      <p className={styles.houes_manage_profile_text_1}>
        {name}
        <br />
        <span>반갑습니다 :)</span>
      </p>
      <div className={styles.house_manage_profile_img_box}>
        <img src="/src/assets/image/man_icon_img.png" alt="profile_img" />
      </div>
      <p className={styles.house_manage_profile_id}>{username}</p>
    </div>
  );
}

export default ProfileBox;
