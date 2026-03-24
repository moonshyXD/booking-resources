import {BrowserRouter, Routes, Route} from "react-router-dom";
import './App.css'
import ChooseOrganization from "./pages/choose-organization/choose-organization";
import Login from "./pages/login/login";
import ForgotPassword from "./pages/forgot-password/forgot-password";
import ForgotPasswordSuccess from "./pages/forgot-password-success/forgot-password-success";
import Catalog from "./pages/catalog/catalog";

function App() {
  return(
      <BrowserRouter>
          <Routes>
              <Route path="/"    element={<ChooseOrganization />} />
              <Route path="/login" element={<Login/>} />
              <Route path="/forgot-password" element={<ForgotPassword />} />
              <Route path="/forgot-password/success" element={<ForgotPasswordSuccess />} />
              <Route path="/catalog" element={<Catalog />} />
          </Routes>
      </BrowserRouter>
  )

}

export default App
