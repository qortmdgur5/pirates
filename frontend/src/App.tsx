import { BrowserRouter, Routes, Route } from "react-router-dom";

// 페이지 컴포넌트
import LoginPage from "./pages/common/login/login"
import AdminHouseManagePage from "./pages/admin/houseManage/HouseManage"
import AdminHouseApprovePage from "./pages/admin/houseApprove/HouseApprove"
import ManagerHouseRegisterPage from "./pages/manager/houseRegister/HouseRegister"
import ManagerApprovePage from "./pages/manager/managerApprove/ManagerApprove";

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route index path="/" element={<LoginPage />}></Route>
        <Route path="/admin/houseManage" element={<AdminHouseManagePage />}></Route>
        <Route path="/admin/houseApprove" element={<AdminHouseApprovePage />}></Route>
        <Route path="/manager/houseRegister" element={<ManagerHouseRegisterPage />}></Route>
        <Route path="/manager/managerApprove" element={<ManagerApprovePage />}></Route>
      </Routes>
    </BrowserRouter>
  );
}

export default App;
