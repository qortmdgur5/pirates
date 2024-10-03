import { BrowserRouter, Routes, Route } from "react-router-dom";

// 페이지 컴포넌트
import LoginPage from "./pages/common/login/login"
import AdminHouseManagePage from "./pages/admin/houseManage/HouseManage"

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route index path="/" element={<LoginPage />}></Route>
        <Route path="/admin/houseManage" element={<AdminHouseManagePage />}></Route>
      </Routes>
    </BrowserRouter>
  );
}

export default App;
