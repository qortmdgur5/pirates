import { atom } from "recoil";
import { recoilPersist } from "recoil-persist";

// recoilPersist를 초기화
const { persistAtom } = recoilPersist({
  key: "localStorage",
  storage: localStorage,
});

interface AuthState {
  role: string | null; // "ADMIN", "OWNER", "MANAGER", "USER"
  token: string | null;
  userId: number | null;
  username: string | null;
}

export const authAtoms = atom<AuthState>({
  key: "authAtoms",
  default: {
    role: null,
    token: null,
    userId: null,
    username: null,
  },
  effects_UNSTABLE: [persistAtom], // recoilPersist로 설정된 persistAtom 사용
});

interface AccomoState {
  accomodation_id: number | null;
  accomodation_name: string | null;
}

export const accomoAtoms = atom<AccomoState>({
  key: "accomoAtoms",
  default: {
    accomodation_id: null,
    accomodation_name: null,
  },
  effects_UNSTABLE: [persistAtom], // recoilPersist로 설정된 persistAtom 사용
});
