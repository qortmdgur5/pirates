import React, { useEffect } from "react";
import { useRecoilState } from "recoil";
import { userAtom } from "../../atoms/userAtoms";

function useSessionUser() {
  const [user, setUser] = useRecoilState(userAtom);

  useEffect(() => {
    const sessionUser = sessionStorage.getItem("user");
    if (sessionUser) {
      const parsedUser = JSON.parse(sessionUser);
      setUser(parsedUser); // Recoil 상태 업데이트
    }
  }, [setUser]);

  return user; // 유저 상태 반환
}

export default useSessionUser;
