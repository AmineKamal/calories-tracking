interface IEnvironementParams<T> 
{
    dev: T;
    staging?: T;
    test?: T;
    prod?: T;
}

interface IEnvironmentGetter<T> 
{
    get: () => T;
}

function getEnv(): keyof IEnvironementParams<any> 
{
    if (!process.env.NODE_ENV || process.env.NODE_ENV === "development") return "dev";
    if (process.env.NODE_ENV === "production") return "prod";
    if (process.env.NODE_ENV === "test") return "test";
    if (process.env.NODE_ENV === "staging") return "staging";

    return "dev";
}

export function Env<T>(params: IEnvironementParams<T>): IEnvironmentGetter<T>
{
    return {
        get: () => params[getEnv()] ?? params.dev
    }
}