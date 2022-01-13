import { HeightCm, HeightFtIn, IMacroSplit, IUser, IWeightDateGoal, WeightKg, WeightLb } from "../core/Store";
import { Env } from "../core/Environment";

//#region Typing
export type Action = "createUser" | "login";

export interface IRequest<_Input, _Output>
{
    url: string;
    method: "GET" | "POST" | "PUT" | "DELETE";
    includeAuthToken: boolean;
}

//#region Api Messages
export interface ILoginInput 
{
    username: string;
    password: string;
}

export interface ILoginOutput
{
    user: IUser;
    token: string;
}

export type IUpdateUserInput = Partial<
{
    name: string;
    weight: WeightKg | WeightLb
    goal: 'loss' | 'gain' | 'maintain';
    activityLevel: 'sedentary' | 'lightly_active' | 'moderately_active' | 'very_active' | 'extra_active';
    age: number;
    gender: 'm' | 'f'
    height: HeightCm | HeightFtIn
    macroSplit: IMacroSplit
    weightDateGoal: IWeightDateGoal
}>;

export interface IUpdateUserOutput extends IUser {}

export interface ICreateUserInput extends IUpdateUserInput, ILoginInput {}

export interface ICreateUserOutput extends IUser {}

//#endregion

export interface IRequests 
{
    createUser: IRequest<ICreateUserInput, ICreateUserOutput>;
    login: IRequest<ILoginInput, ILoginOutput>;
}

export type IRequestInput<R> = R extends IRequest<infer I, any> ? I : never;
export type IRequestOutput<R> = R extends IRequest<any, infer O> ? O : never;

//#endregion

//#region Declaration
export const Endpoint = Env({ dev: "http://localhost:5000" });
export const Requests: {[K in Action]: IRequests[K]} = 
{
    createUser: 
    {
        url: "/users",
        method: "POST",
        includeAuthToken: false
    },
    login:
    {
        url: "/user/login",
        method: "POST",
        includeAuthToken: false
    }
} as const;

//#endregion