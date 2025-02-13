import { atom } from "recoil";
import { recoilPersist } from "recoil-persist";

// recoilPersist를 초기화
const { persistAtom } = recoilPersist({
  key: "localStorage",
  storage: localStorage,
});

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
  token: string | null;
  id: number | null;
  role: string | null;
  party_id: number | null;
  userInfo: UserInfo | null;
}

// Recoil atom 정의
export const userAtom = atom<User | null>({
  key: "userAtom", // 유니크한 key 값
  default: null, // 초기 상태는 null
  effects_UNSTABLE: [persistAtom], // recoilPersist로 설정된 persistAtom 사용
});
