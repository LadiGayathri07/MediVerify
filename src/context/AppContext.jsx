import { createContext, useState, useEffect } from "react";
import axios from "axios";

export const AppContext = createContext();

const API_BASE_URL = "http://127.0.0.1:5000"; // Flask backend URL

const AppContextProvider = ({ children }) => {
    const [user, setUser] = useState(null);
    const [data, setData] = useState(null); // Example state for fetching data

    // Example: Fetch data from backend when component mounts
    useEffect(() => {
        axios.get(`${API_BASE_URL}/your-endpoint`)
            .then(response => setData(response.data))
            .catch(error => console.error("Error fetching data:", error));
    }, []);

    const value = {
        user,
        setUser,
        data, // Provide fetched data to the context
    };

    return (
        <AppContext.Provider value={value}>
            {children}
        </AppContext.Provider>
    );
};

export default AppContextProvider;
