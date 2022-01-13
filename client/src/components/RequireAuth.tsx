import { useEffect } from 'react';
import { Navigate } from 'react-router';
import { Location } from '../config/Locations';
import { useSharedState } from '../core/Store';

const isAuthenticated = false;
const authPath = "/";

export default function RequireAuth({children}: any) {
    const [, setState] = useSharedState();
    const setValue = (location: Location) => setState((value) => ({...value, location}));

    useEffect(() => {
        if (!isAuthenticated) setValue(authPath);
    });
    
    return isAuthenticated? children : <Navigate to={authPath} />
}