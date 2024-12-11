import { atom } from "recoil";

// userAtom에 포함될 유저 정보 타입을 정의
export interface UserInfo {
  name: string;
  phone: string;
  gender: boolean; // true: 남자, false: 여자
  job: string | null;
  age: number | null;
  mbti: string | null;
  region: string | null;
}

export interface User {
  id: number;
  party_id: number | null;
  userInfo: UserInfo | null;
}

// Recoil atom 정의
export const userAtom = atom<User | null>({
  key: "userAtom",   // 유니크한 key 값
  default: null,     // 초기 상태는 null
});