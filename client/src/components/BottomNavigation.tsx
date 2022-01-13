import BottomNavigation from '@mui/material/BottomNavigation';
import BottomNavigationAction from '@mui/material/BottomNavigationAction';
import { Paper } from '@mui/material';
import { Link } from "react-router-dom";
import { useSharedState } from "../core/Store";
import { LocationConfig, Locations, WithBottomNavigation, Location } from '../config/Locations';

function FilterLocation(value: [string, LocationConfig]): value is [string, WithBottomNavigation]
{
    return value[1].inNav === true;
}

function NavigationActionMapper([loc, {name, icon}]: [string, WithBottomNavigation], index: number) 
{
    return <BottomNavigationAction key={index} label={name} value={loc} icon={icon} component={Link} to={loc}/>
}

export default function BottomNav() {
    const [state, setState] = useSharedState();
    const setValue = (location: Location) => setState((value) => ({...value, location}));
  
    return (
        Locations[state.location].displayNav ?
            <Paper sx={{ position: 'fixed', bottom: 0, left: 0, right: 0 }} elevation={3}>
                <BottomNavigation showLabels value={state.location} onChange={(_, newValue) => { setValue(newValue); }}>
                    { Object.entries(Locations).filter(FilterLocation).map(NavigationActionMapper)}
                </BottomNavigation>
            </Paper>
            : null
    );
  }