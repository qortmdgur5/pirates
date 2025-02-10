import { useEffect } from "react";
import { useRecoilState } from "recoil";
import { authAtoms } from "../atoms/authAtoms";

function useSessionUser() {
  const [user, setUser] = useRecoilState(authAtoms);

  // 초기화: sessionStorage 값을 Recoil 상태로 로드
  useEffect(() => {
    const sessionUser = sessionStorage.getItem("user");
    if (sessionUser) {
      const parsedUser = JSON.parse(sessionUser);
      if (!user || JSON.stringify(user) !== JSON.stringify(parsedUser)) {
        setUser(parsedUser);
      }
    }
  }, [setUser, user]);

  // Recoil 상태 변경 시 sessionStorage 업데이트
  useEffect(() => {
    if (user) {
      sessionStorage.setItem("user", JSON.stringify(user));
    }
  }, [user]);

  return user;
}

export default useSessionUser;
