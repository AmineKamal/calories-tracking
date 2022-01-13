import { useState } from 'react';
import { createContainer } from 'react-tracked';
import { Location } from "../config/Locations"

//#region Typing

//#region User Types
export interface WeightKg 
{
  value: number;
  kind: "kg";
}

export interface WeightLb
{
  value: number;
  kind: "lb";
}

export interface HeightCm 
{
  value: number;
  kind: "cm";
}

export interface HeightFtIn
{
  valueFt: number;
  valueIn: number;
  kind: "ft_in";
}

export interface IMacros 
{
  calories: number;
  carbs: number;
  protein: number;
  fat: number;
}

export interface IMeal 
{
  name: string;
  calories: number;
  protein: number;
  fat: number;
  carbs: number;
}

export interface IWeightDateGoal 
{
  date: string;
  weight: WeightKg | WeightLb;
}

export interface IMacroSplit 
{
  carbs: number;
  protein: number;
  fat: number;
}

export interface IFollowOptions 
{
  subscribeToMeals: boolean
}

export interface IUser 
{
  id: string;
  username: string;
  password: string;
  name: string;
  weight: WeightKg | WeightLb;
  goal: 'loss'| 'gain' | 'maintain';
  activityLevel: 'sedentary' | 'lightly_active' | 'moderately_active' | 'very_active' | 'extra_active';
  weightDateGoal?: IWeightDateGoal;
  age: number;
  gender: 'm' | 'f';
  height: HeightCm | HeightFtIn;
  targetMacros: IMacros;
  currentMacros: IMacros;
  macroSplit?: IMacroSplit;
  meals: { [key: string]: IMeal };
  following: { [key: string]: IFollowOptions };
  followers: { [key: string]: IFollowOptions };
}

//#endregion

interface INotification 
{
  isOpen: boolean;
  severity: "error" | "warning" | "info" | "success";
  message: string;
}

interface IState 
{
  location: Location;
  notification: INotification;
  user?: IUser;
}

//#endregion

//#region Declaration
const initialState: IState = {
  location: window.location.pathname as Location,
  notification: {isOpen: false, severity: "info", message: ""}
};

const useMyState = () => useState(initialState);

export const { Provider: SharedStateProvider, useTracked: useSharedState } = createContainer(useMyState);

//#endregion