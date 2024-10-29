import { useEffect, useState } from "react";
import axios from "axios";
import styles from "./styles/guestHouseTable.module.scss";

// API 응답 데이터 타입 정의
interface GuestHouseAPIResponse {
  id: number;
  name: string;
  address: string;
  number: string;
  date: string;
}

interface GuestHouseTableProps {
  isMostReviews: boolean;
}

function GuestHouseTable({ isMostReviews }: GuestHouseTableProps) {
  const [data, setData] = useState<GuestHouseAPIResponse[]>([]);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await axios.get<GuestHouseAPIResponse[]>(
          "/api/admin/accomodations",
          {
            params: { isMostReviews, skip: 0, limit: 10 },
            headers: { accept: "application/json" },
          }
        );

        console.log(response);

        setData(response.data);
      } catch (error) {
        console.error("데이터를 불러오는데 실패했습니다.", error);
      }
    };

    fetchData();
  }, [isMostReviews]); // isMostReviews가 변경될 때마다 데이터 갱신

  return (
    <div className={styles.table_container}>
      <table className={styles.guest_house_table}>
        <thead>
          <tr>
            <th className={styles.th_left_blank}></th>
            <th className={styles.text_left}>NO.</th>
            <th className={styles.text_left}>게스트 하우스 이름</th>
            <th className={styles.text_left}>주소</th>
            <th className={styles.text_left}>숙소 연락처</th>
            <th className={styles.text_left}>숙소 등록일</th>
            <th className={styles.th_right_blank}></th>
          </tr>
        </thead>
        <tbody>
          {data.map((item, index) => (
            <tr key={item.id}>
              <td className={styles.td_left_black}></td>
              <td className={styles.text_left}>
                {String(index + 1).padStart(2, "0")}
              </td>
              <td className={styles.text_left}>{item.name}</td>
              <td className={styles.text_left}>{item.address}</td>
              <td className={styles.text_left}>{item.number}</td>
              <td className={styles.text_left}>{item.date}</td>
              <td className={styles.td_right_black}></td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default GuestHouseTable;
