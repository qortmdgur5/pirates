import styles from "./styles/nameSearch.module.scss";

function NameSearch() {
  return (
    <div className={styles.input_wrapper}>
      <input className={styles.name_input} type="text" placeholder="검색" />
      <img src="/src/assets/image/glasses.png" alt="search_icon_img" />
    </div>
  );
}

export default NameSearch;
