import { ReactNode } from 'react';
import Home from '../pages/HomePage';
import Meals from '../pages/MealsPage';
import Profile from '../pages/ProfilePage';
import HomeIcon from '@mui/icons-material/Home';
import LocalDining from '@mui/icons-material/LocalDining';
import FavoriteIcon from '@mui/icons-material/Favorite';

//#region Typing
export type Location = "/" | "/profile" | "/meals";
export interface BaseLocationConfig 
{
    displayNav: boolean;
    requireAuth: boolean;
    element: () => JSX.Element;
}

export interface WithBottomNavigation extends BaseLocationConfig
{
    displayNav: true;
    inNav: true;
    icon: ReactNode;
    name: string;
}

export interface WithoutBottomNavigation extends BaseLocationConfig
{
    inNav?: false;
}

export type LocationConfig = WithBottomNavigation | WithoutBottomNavigation;

//#endregion

//#region Declaration
export const Locations: {[k in Location]: LocationConfig} = 
{
    "/": 
    { 
        name: "Home",
        displayNav: true,
        requireAuth: false,
        element: Home,
        inNav: true,
        icon: <HomeIcon/>
    },
    "/meals":
    {
        name: "Meals",
        displayNav: true,
        requireAuth: true,
        element: Meals,
        inNav: true,
        icon: <LocalDining/>
    },
    "/profile":
    { 
        name: "Profile",
        displayNav: true,
        requireAuth: false,
        element: Profile,
        inNav: true,
        icon: <FavoriteIcon/>
    },
};

//#endregion