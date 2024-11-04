import { useEffect, useState } from "react";
import styles from "./styles/managePartyTable.module.scss";
import axios from "axios";

interface Party {
  id: number;
  partyDate: string;
  number: number;
  partyOpen: boolean;
  partyTime: string;
}

interface ManagePartyTableProps {
  isOldestOrders: boolean;
}

const ManagePartyTable: React.FC<ManagePartyTableProps> = ({
  isOldestOrders,
}) => {
  const [data, setData] = useState<Party[]>([]);
  const accomodationId = 1; // 임시 숙소 id

  // 매니저 리스트 가져오기 API
  useEffect(() => {
    const fetchData = async (id: number) => {
      try {
        const response = await axios.get<Party[]>(
          `/api/manager/parties/${id}`,
          {
            params: { isOldestOrders, skip: 0, limit: 10 },
            headers: { accept: "application/json" },
          }
        );
        setData(response.data);
      } catch (error) {
        console.error("데이터를 불러오는데 실패했습니다.", error);
      }
    };

    fetchData(accomodationId);
  }, [isOldestOrders]); // isOldestOrders가 변경될 때마다 데이터 갱신
  return (
    <div className={styles.table_container}>
      <table className={styles.guest_house_table}>
        <thead>
          <tr>
            <th className={styles.th_left_blank}></th>
            <th className={styles.text_center}>NO.</th>
            <th className={styles.text_center}>파티 일자</th>
            <th className={styles.text_center}>참석 인원</th>
            <th className={styles.text_center}>파티여부</th>
            <th className={styles.text_center}>파티 시작 시간</th>
            <th className={styles.th_right_blank}></th>
          </tr>
        </thead>
        <tbody>
          {data.map((item, index) => (
            <tr key={index}>
              <td className={styles.td_left_black}></td>
              <td className={styles.text_center}>{index + 1}</td>
              <td className={styles.text_center}>{item.partyDate}</td>
              <td className={styles.text_center}>
                5/{item.number}
              </td>
              <td className={styles.text_center}>
                {item.partyOpen ? `O` : `X`}
              </td>
              <td className={styles.text_center}>{item.partyTime}</td>
              <td className={styles.td_right_black}></td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default ManagePartyTable;
