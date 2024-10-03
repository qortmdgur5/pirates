import React from "react";
import styles from "./styles/menuBox.module.scss";

// MenuBox의 타입 정의
interface MenuBoxProps {
  menuTabs: { text: string; isActive: boolean }[]; // 각 탭의 텍스트와 활성화 여부를 배열로 전달받음
}

const MenuBox: React.FC<MenuBoxProps> = ({ menuTabs }) => {
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

          {/* tab.isActive에 따라 background-color와 스타일 조정 */}
          <button
            className={`${styles.menu_card} ${
              tab.isActive ? styles.active_card : ""
            }`}
          >
            {tab.text}
          </button>
        </div>
      ))}
    </div>
  );
};

export default MenuBox;
