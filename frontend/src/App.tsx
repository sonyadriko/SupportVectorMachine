import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Dashboard from "./pages/Dashboard";
import Topbar from "./components/Topbar";
import DataTraining from "./pages/DataTraining";
import Evaluate from "./pages/Evaluate";

function App() {
  return (
    <Router>
      <div className="min-h-screen bg-gray-100 dark:bg-gray-900 text-black dark:text-white">
        <Topbar />
        <div className="p-6">
          <Routes>
            <Route path="/" element={<Dashboard />} />
            <Route path="/datatraining" element={<DataTraining />} />
            {/*<Route path="/preprocessing" element={<Preprocessing />} />
            <Route path="/tfidf" element={<Tfidf />} />
            <Route path="/svm" element={<SVM />} />*/}
            <Route path="/evaluate" element={<Evaluate />} /> 
          </Routes>
        </div>
      </div>
    </Router>
  );
}

export default App;
