import { atom } from "recoil";

interface AuthState {
  role: string | null; // "ADMIN", "OWNER", "MANAGER", "USER"
  token: string | null;
  userId: number | null;
}

export const authAtoms = atom<AuthState>({
  key: "authAtoms",
  default: {
    role: null,
    token: null,
    userId: null,
  },
});

interface AccomoState {
  accomodation_id: number | null;
}

export const accomoAtoms = atom<AccomoState>({
  key: "accomoAtoms",
  default: {
    accomodation_id: null,
  },
});
