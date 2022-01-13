import Box from '@mui/material/Box';
import { BrowserRouter as Router, Routes, Route} from "react-router-dom";
import { LocationConfig, Locations } from '../config/Locations';
import BottomNavigation from "../components/BottomNavigation";
import RequireAuth from '../components/RequireAuth';
import Notification from '../components/Notification';

function RouterMapper([loc, {requireAuth, element}]: [string, LocationConfig], index: number) 
{
    return <Route key={index} path={loc} element={requireAuth ? <RequireAuth>element()</RequireAuth> : element()}></Route>;
}

export default function RouterComponent() {
    return (
        <Router>
            <Box sx={{ pb: 7 }}>
                <Routes>{Object.entries(Locations).map(RouterMapper)}</Routes>
                <BottomNavigation></BottomNavigation>
                <Notification/>
            </Box>
        </Router>
  )
}