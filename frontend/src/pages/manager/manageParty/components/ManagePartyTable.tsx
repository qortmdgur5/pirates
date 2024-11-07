import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom"; // 추가
import styles from "./styles/managePartyTable.module.scss";
import axios from "axios";

interface Party {
  id: number;
  partyDate: string;
  number: number;
  partyOpen: boolean;
  partyTime: string;
  participant: number;
}

interface PartyAPIResponse {
  data: Party[];
  totalCount: number;
}

interface ManagePartyTableProps {
  isOldestOrders: boolean;
  page: number;
  pageSize: number;
}

const ManagePartyTable: React.FC<ManagePartyTableProps> = ({
  isOldestOrders,
  page,
}) => {
  const [data, setData] = useState<Party[]>([]);
  const [totalCount, setTotalCount] = useState<number>(0);
  const accomodationId = 1; // 임시 숙소 id
  const navigate = useNavigate(); // navigate 추가

  // 매니저 리스트 가져오기 API
  useEffect(() => {
    const fetchData = async (id: number) => {
      try {
        const response = await axios.get<PartyAPIResponse>(
          `/api/manager/parties/${id}`,
          {
            params: { isOldestOrders, skip: 0, limit: 10 },
            headers: { accept: "application/json" },
          }
        );
        setData(response.data.data);
        setTotalCount(response.data.totalCount);
      } catch (error) {
        console.error("데이터를 불러오는데 실패했습니다.", error);
      }
    };

    fetchData(accomodationId);
  }, [isOldestOrders, page]);

  // 행 클릭 시 상세 페이지로 이동
  const handleRowClick = (item: Party) => {
    navigate(`/manager/managePartyDetail/${item.id}`, { state: item });
  };

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
            <tr
              key={index}
              onClick={() => handleRowClick(item)}
              style={{ cursor: "pointer" }}
            >
              <td className={styles.td_left_black}></td>
              <td className={styles.text_center}>{index + 1}</td>
              <td className={styles.text_center}>{item.partyDate}</td>
              <td className={styles.text_center}>
                {item.participant}/{item.number}
              </td>{" "}
              {/* 예약인원 데이터 추가 */}
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
