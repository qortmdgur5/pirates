import { useState } from "react";
import styles from "./styles/nameSearch.module.scss";

interface NameSearchProps {
  onSearch: (name: string) => void;
}

function NameSearch({ onSearch }: NameSearchProps) {
  const [inputValue, setInputValue] = useState<string>("");

  const handleChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    setInputValue(event.target.value);
  };

  const handleKeyDown = (event: React.KeyboardEvent<HTMLInputElement>) => {
    if (event.key === "Enter") {
      onSearch(inputValue); // 엔터를 누르면 검색 실행
    }
  };

  return (
    <div className={styles.input_wrapper}>
      <input
        className={styles.name_input}
        type="text"
        placeholder="검색"
        value={inputValue}
        onChange={handleChange}
        onKeyDown={handleKeyDown} // 엔터 키 감지
      />
      <img src="/src/assets/image/glasses.png" alt="search_icon_img" />
    </div>
  );
}

export default NameSearch;
