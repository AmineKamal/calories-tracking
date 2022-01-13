import { Action, Endpoint, IRequestInput, IRequestOutput, IRequests, Requests } from "../config/Api";
import axios, { AxiosRequestHeaders } from "axios";
import { useSharedState } from "./Store";
import { useEffect, useState } from "react";

function camelToSnake(s: string): string
{
    return s.replace(/[A-Z]/g, letter => `_${letter.toLowerCase()}`);
}

function snakeToCamel(s: string): string 
{
    return s.toLowerCase().replace(/([-_][a-z])/g, group =>
        group
        .toUpperCase()
        .replace('-', '')
        .replace('_', '')
    );
}

function transformKeys(body: any, transformer: (k: string) => string, recurse = true): object
{
    const keys = Object.keys(body);
    const obj: any = {};

    for (const key of keys) 
    {
        const transformedKey = transformer(key);
        
        if (body[key] && typeof body[key] === "object" && body[key]["__collection__"]) 
        {
            delete body[key]["__collection__"];
            obj[transformedKey] = body[key];
            continue;
        }

        obj[transformedKey] = body[key] && typeof body[key] === "object" && recurse ? transformKeys(body[key], transformer, recurse) : body[key];
    }

    return obj;
}

async function performAction<A extends Action>(action: A, input: IRequestInput<IRequests[A]>): Promise<IRequestOutput<IRequests[A]>>
{
    const request = Requests[action];
    const token = localStorage.getItem("token");
    
    if (!token && request.includeAuthToken) 
    {
        // Todo throw error
    }
    
    const data = JSON.stringify(transformKeys(input, camelToSnake));
    const url = Endpoint.get() + request.url;
    const method = request.method;
    const headers: AxiosRequestHeaders = { "content-type": "application/json" };
    
    if (token && request.includeAuthToken) headers["Authorization"] = `Bearer ${token}`;
    
    const response = await axios.request<IRequestOutput<IRequests[A]>>({url, method, data, headers});

    return transformKeys(response.data, snakeToCamel) as IRequestOutput<IRequests[A]>;
}

export function useAction<A extends Action>(action: A)
{
    const [, setState] = useSharedState();
    const notify = (severity: "error" | "warning" | "info" | "success", message: string) => setState((value) => ({...value, notification: {isOpen: true, severity, message}}));
    const [loading, setLoading] = useState(true);
    const [response, setResponse] = useState<IRequestOutput<IRequests[A]> | null>(null);
    const [error, setError] = useState<boolean>(false);

    async function dispatch(input: IRequestInput<IRequests[A]>) 
    {
        try 
        {
            const response = await performAction(action, input);
            console.log(response);
            setResponse(response);
            notify("success", "Operation was successful");
        }
        catch(e: any) 
        {
            if (axios.isAxiosError(e)) 
            {
                console.log(e.response);
                setError(true);
                notify("error", e.response?.data);
            }
        }

        setLoading(false);
    }

    return {loading, response, error, dispatch};
}