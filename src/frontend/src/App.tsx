import { BrowserRouter, Routes, Route, Navigate, useLocation } from "react-router-dom";
import { useEffect } from 'react'
import type { ReactElement } from 'react'
import { useDispatch, useSelector } from 'react-redux'
import './App.css'
import ChooseOrganization from "./pages/choose-organization/choose-organization";
import Login from "./pages/login/login";
import ForgotPassword from "./pages/forgot-password/forgot-password";
import ForgotPasswordSuccess from "./pages/forgot-password-success/forgot-password-success";
import Catalog from "./pages/catalog/catalog";
import type { AppDispatch, RootState } from './store/store'
import { fetchMe } from './store/authSlice'

const RequireAuth = ({ children }: { children: ReactElement }) => {
  const location = useLocation()
  const isAuthenticated = useSelector((state: RootState) => state.auth.isAuthenticated)

  if (!isAuthenticated) {
    return <Navigate to="/login" replace state={{ from: location.pathname }} />
  }

  return children
}

const RequireOrganization = ({ children }: { children: ReactElement }) => {
  const location = useLocation()
  const selectedOrgId = useSelector((state: RootState) => state.organization.selectedOrgId)

  if (!selectedOrgId) {
    return <Navigate to="/" replace state={{ from: location.pathname }} />
  }

  return children
}

function App() {
  const dispatch = useDispatch<AppDispatch>()
  const meEndpoint = import.meta.env.VITE_ME_ENDPOINT

  useEffect(() => {
    if (meEndpoint) {
      void dispatch(fetchMe())
    }
  }, [dispatch, meEndpoint])

  return (
    <BrowserRouter basename="/frontend">
      <Routes>
        <Route path="/" element={<ChooseOrganization />} />
        <Route path="/login" element={<Login />} />
        <Route path="/forgot-password" element={<ForgotPassword />} />
        <Route path="/forgot-password/success" element={<ForgotPasswordSuccess />} />
        <Route
          path="/catalog"
          element={
            <RequireAuth>
              <RequireOrganization>
                <Catalog />
              </RequireOrganization>
            </RequireAuth>
          }
        />
      </Routes>
    </BrowserRouter>
  )
}

export default App
