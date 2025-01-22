import ReactDOM from "react-dom/client";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import Predictions from "./pages/Predictions";
import Navbar from "./components/Navbar"


export default function App() {

  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Predictions />} />
      </Routes>
    </BrowserRouter>
  );
}

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(<App />);