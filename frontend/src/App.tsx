import { BrowserRouter, Routes, Route } from "react-router-dom";

// 페이지 컴포넌트
import ManagerLoginPage from "./pages/manager/login/Login"
import AdminHouseManagePage from "./pages/admin/houseManage/HouseManage"
import AdminHouseApprovePage from "./pages/admin/houseApprove/HouseApprove"
import ManageHousePage from "./pages/owner/manageHouse/ManageHouse"
import ManagerApprovePage from "./pages/owner/managerApprove/ManagerApprove";
import ManagePartyPage from "./pages/manager/manageParty/ManageParty"
import ManagePartyDetailPage from "./pages/manager/managePartyDetail/ManagePartyDetail"
import ManagerSignupPage from "./pages/manager/signup/Signup"

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route index path="/" element={<ManagerLoginPage />}></Route>
        <Route path="/admin/houseManage" element={<AdminHouseManagePage />}></Route>
        <Route path="/admin/houseApprove" element={<AdminHouseApprovePage />}></Route>
        <Route path="/owner/manageHouse" element={<ManageHousePage />}></Route>
        <Route path="/owner/managerApprove" element={<ManagerApprovePage />}></Route>
        <Route path="/manager/manageParty" element={<ManagePartyPage />}></Route>
        <Route path="/manager/managePartyDetail/:id" element={<ManagePartyDetailPage />}></Route>
        <Route path="/manager/signup" element={<ManagerSignupPage />}></Route>
      </Routes>
    </BrowserRouter>
  );
}

export default App;
