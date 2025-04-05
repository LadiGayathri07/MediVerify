import { Routes, Route } from 'react-router-dom';
import Home from './pages/Home';
import Result from './pages/Result';
import Learn from './pages/Learn';
import Navbar from './components/Navbar';

const App = () => {
    return (
        <div 
            className="px-4 sm:px-8 md:px-12 lg:px-20 xl:px-28 min-h-screen h-auto bg-transparent"
            style={{ backgroundImage: "url('/bg-image.jpeg')", backgroundSize: "cover", backgroundPosition: "center", backgroundRepeat: "no-repeat", backgroundAttachment: "fixed" }}
        >
            <Navbar />
            <Routes>
                <Route path="/" element={<Home />} />
                
                <Route path="/result" element={<Result />} />
                <Route path="/learn" element={<Learn />} />
            </Routes>
        </div>
    );
};

export default App;
