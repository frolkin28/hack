import {
    useState,
    useCallback,
    useRef,
    useEffect
} from 'react';

const useStateWithCallback = (initialState) => {
    const [state, setState] = useState(initialState);
    const callBackRef = useRef(null);

    const updateState = useCallback((newState, callBack) => {
        callBackRef.current = callBack;
        setState(prev => typeof newState === 'function' ? newState(prev) : newState);
    }, []);

    useEffect(() => {
        if (callBackRef.current) {
            callBackRef.current(state);
            callBackRef.current = null;
        }
    }, [state]);

    return [state, updateState];
}

export default useStateWithCallback;