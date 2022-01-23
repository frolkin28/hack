import React, {useState} from "react";

export const MainContext = React.createContext(null);

export const ContextProvider = ({children}) => {
    const [inputEmail, setInputEmail] = useState('');
    const [inputName, setInputName] = useState('');

    const data = {
        email: [inputEmail, setInputEmail],
        name: [inputName, setInputName],
    }

    return (
        <MainContext.Provider value={data}>
            {children}
        </MainContext.Provider>
    );
};
