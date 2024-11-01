import { BrowserRouter, Routes, Route } from "react-router-dom";

// 페이지 컴포넌트
import LoginPage from "./pages/common/login/login"
import AdminHouseManagePage from "./pages/admin/houseManage/HouseManage"
import AdminHouseApprovePage from "./pages/admin/houseApprove/HouseApprove"
import ManageHousePage from "./pages/manager/manageHouse/ManageHouse"
import ManagerApprovePage from "./pages/manager/managerApprove/ManagerApprove";
import ManagePartyPage from "./pages/manager/manageParty/ManageParty"
import ManagePartyDetailPage from "./pages/manager/managePartyDetail/ManagePartyDetail"
import OwnerSignupPage from "./pages/owner/signup/Signup"

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route index path="/" element={<LoginPage />}></Route>
        <Route path="/admin/houseManage" element={<AdminHouseManagePage />}></Route>
        <Route path="/admin/houseApprove" element={<AdminHouseApprovePage />}></Route>
        <Route path="/manager/manageHouse" element={<ManageHousePage />}></Route>
        <Route path="/manager/managerApprove" element={<ManagerApprovePage />}></Route>
        <Route path="/manager/manageParty" element={<ManagePartyPage />}></Route>
        <Route path="/manager/managePartyDetail" element={<ManagePartyDetailPage />}></Route>
        <Route path="/owner/signup" element={<OwnerSignupPage />}></Route>
      </Routes>
    </BrowserRouter>
  );
}

export default App;
