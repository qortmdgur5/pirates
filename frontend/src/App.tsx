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
import UserLoginPage from "./pages/user/login/Login"
import UserPartyPage from "./pages/user/party/Party"
import UserChatPage from "./pages/user/chat/Chat"
import UserChatRoomsPage from "./pages/user/chatRoom/ChatRoom"
import UserPartyUserListPage from "./pages/user/partyUserList/PartyUserList"

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/admin/houseManage" element={<AdminHouseManagePage />}></Route>
        <Route path="/admin/houseApprove" element={<AdminHouseApprovePage />}></Route>
        <Route path="/owner/manageHouse" element={<ManageHousePage />}></Route>
        <Route path="/owner/managerApprove" element={<ManagerApprovePage />}></Route>
        <Route path="/manager/login" element={<ManagerLoginPage />}></Route>
        <Route path="/manager/manageParty" element={<ManagePartyPage />}></Route>
        <Route path="/manager/managePartyDetail/:id" element={<ManagePartyDetailPage />}></Route>
        <Route path="/manager/signup" element={<ManagerSignupPage />}></Route>
        <Route index path="/" element={<UserLoginPage />}></Route>
        <Route path="/user/party" element={<UserPartyPage />} />
        <Route path="/user/chat" element={<UserChatPage />} />
        <Route path="/user/chatRooms" element={<UserChatRoomsPage />} />
        <Route path="/user/party/userList" element={<UserPartyUserListPage />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
