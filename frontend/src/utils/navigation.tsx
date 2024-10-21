// 네비게이션 공통 유틸 함수

import { useNavigate } from "react-router-dom";

export const useNavigation = () => {
  const navigate = useNavigate();
  
  return (url: string) => {
    navigate(url);
  };
};
