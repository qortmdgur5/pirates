import { atom } from "recoil";

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
});

interface AccomoState {
  accomodation_id: number | null;
  // accomodation_name: string | null;
}

export const accomoAtoms = atom<AccomoState>({
  key: "accomoAtoms",
  default: {
    accomodation_id: null,
    // accomodation_name: null,
  },
});
