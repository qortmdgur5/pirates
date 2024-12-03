import styles from "./styles/houseNameAndDate.module.scss";

interface Props {
  guestHouseName: string;
}

function HouseNameAndDate({ guestHouseName }: Props) {
  const now = new Date();
  const currentHour = now.getHours();

  // 날짜 형식 변환 함수
  const formatDay = (date: Date) => {
    const dayOfWeek = ["일", "월", "화", "수", "목", "금", "토"];
    return `${date.getMonth() + 1}.${date.getDate()} (${
      dayOfWeek[date.getDay()]
    })`;
  };

  // 표시할 날짜 결정
  const displayDate = (() => {
    if (currentHour >= 12) {
      // 오늘 정오 이후는 오늘 날짜 표시
      return formatDay(now);
    } else {
      // 정오 이전이라면 전날 정오 이후
      const yesterday = new Date(now);
      yesterday.setDate(now.getDate() - 1);
      return formatDay(yesterday);
    }
  })();

  return (
    <p className={styles.party_text_1}>
      {guestHouseName} - {displayDate}
    </p>
  );
}

export default HouseNameAndDate;
