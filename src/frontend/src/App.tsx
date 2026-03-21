import {BrowserRouter, Routes, Route} from "react-router-dom";
import './App.css'
import ChooseOrganization from "./pages/choose-organization/choose-organization.tsx";

function App() {
  return(
      <BrowserRouter>
          <Routes>
              <Route path="/" element={<ChooseOrganization />} />
          </Routes>
      </BrowserRouter>
  )

}

export default App
