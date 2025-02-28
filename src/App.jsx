import ReactDOM from "react-dom/client";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import Predictions from "./pages/Predictions";
import Compare from "./pages/Compare";
import Navbar from "./components/Navbar"
import League from "./pages/League";
import Home from "./pages/Home";


export default function App() {

  return (
    <BrowserRouter>
      <Navbar />
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/stats" element={<Predictions />} />
        <Route path="/compare" element={<Compare />} />
        <Route path="/league" element={<League />} />
      </Routes>
    </BrowserRouter>
  );
}

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(<App />);