import React, {useState} from "react";
import useStateWithCallback from "../../hooks/useStateWithCallback";

export const MainContext = React.createContext(null);

export const ContextProvider = ({children}) => {
    const [inputEmail, setInputEmail] = useState('');
    const [inputName, setInputName] = useState('');
    const [isOrganizer, setIsOrganizer] = useState(false);
    const [clients, setClients] = useStateWithCallback([]);

    const data = {
        email: [inputEmail, setInputEmail],
        name: [inputName, setInputName],
        organizer: [isOrganizer, setIsOrganizer],
        clients: [clients, setClients]
    }

    return (
        <MainContext.Provider value={data}>
            {children}
        </MainContext.Provider>
    );
};
