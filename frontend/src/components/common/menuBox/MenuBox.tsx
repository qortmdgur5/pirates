import { useNavigation } from "../../../utils/navigation"; // 네비게이션 훅 임포트
import styles from "./styles/menuBox.module.scss";

// MenuBox의 타입 정의
interface MenuBoxProps {
  menuTabs: { text: string; isActive: boolean; path: string }[]; // 각 탭의 텍스트, 활성화 여부, 경로를 전달받음
}

function MenuBox({ menuTabs }: MenuBoxProps) {
  const navigateTo = useNavigation(); // 네비게이션 훅 호출

  return (
    <div className={styles.house_manage_menu_box}>
      {/* menuTabs 배열을 map으로 순회하면서 각 탭을 렌더링 */}
      {menuTabs.map((tab, index) => (
        <div className={styles.menu_tab} key={index}>
          {/* tab.isActive에 따라 sideBar visibility 조정 */}
          <div
            className={`${styles.menu_tab_sideBar} ${
              tab.isActive ? styles.visible : ""
            }`}
          ></div>

          {/* tab.isActive에 따라 스타일 조정 및 네비게이션 적용 */}
          <button
            className={`${styles.menu_card} ${
              tab.isActive ? styles.active_card : ""
            }`}
            onClick={() => navigateTo(tab.path)} // 클릭 시 해당 경로로 이동
          >
            {tab.text}
          </button>
        </div>
      ))}
    </div>
  );
}

export default MenuBox;
