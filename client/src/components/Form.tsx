import {capitalize} from "lodash";
import { FormControl, FormControlLabel, FormLabel, RadioGroup, TextField, Radio, InputLabel, MenuItem, Select, Checkbox, ListItemText, Switch } from "@mui/material";

type ElementProps<P, T> = { element: (props: P) => JSX.Element, state: [T, React.Dispatch<React.SetStateAction<T>>] } & P;
function FormElement<P, T>(props: ElementProps<P, T>) 
{
    const [state, setState] = props.state;
    const handleChange = (e: any) => setState(e.target.value);

    const E = props.element;
    return <E {...props} sx={{ m: 1 }} value={state} onChange={handleChange}></E>
}

type TextElementProps = { name: string, state: [string, React.Dispatch<React.SetStateAction<string>>] };
export function TextElement({name, state}: TextElementProps) 
{
    return <FormElement element={TextField} state={state} label={name} variant="outlined" />
}

type PasswordElementProps = { name: string, state: [string, React.Dispatch<React.SetStateAction<string>>] };
export function PasswordElement({name, state}: PasswordElementProps) 
{
    return <FormElement element={TextField} state={state} label={name} variant="outlined" type="password" autoComplete="on" />
}

type NumberElementProps = { name: string, state: [number, React.Dispatch<React.SetStateAction<number>>] };
export function NumberElement({name, state}: NumberElementProps) 
{
    return <FormElement element={TextField} state={state} label={name} variant="outlined" type="number" />
}

type CheckboxElementProps = { name: string, state: [boolean, React.Dispatch<React.SetStateAction<boolean>>] };
export function CheckboxElement({name, state}: CheckboxElementProps) 
{
    const [value, setState] = state;
    const handleChange = (event: React.ChangeEvent<HTMLInputElement>) => setState(event.target.checked);
      
    return <FormControlLabel sx={{ m: 1 }} control={<Checkbox checked={value} onChange={handleChange} />} label={capitalize(name)} />
}

type SwitchElementProps = { name: string, state: [boolean, React.Dispatch<React.SetStateAction<boolean>>] };
export function SwitchElement({name, state}: SwitchElementProps) 
{
    const [value, setState] = state;
    const handleChange = (event: React.ChangeEvent<HTMLInputElement>) => setState(event.target.checked);
      
    return <FormControlLabel sx={{ m: 1 }} control={<Switch checked={value} onChange={handleChange} />} label={capitalize(name)} />
}

type Option = string | number;

function cap(option?: Option): Option { return typeof option === "number" ? option : capitalize(option); }

type RadioElementProps<Options extends readonly Option[]> = { name: string, state: [Options[number], React.Dispatch<React.SetStateAction<Options[number]>>], options: Options };
export function RadioElement<Options extends readonly Option[]>({name, state, options}: RadioElementProps<Options>) 
{
    const [value, setState] = state;
    const handleChange = (e: any) => setState(e.target.value);
    const optionMapper = (option: Option, i: number) => <FormControlLabel key={i} value={option} control={<Radio />} label={cap(option)} />;

    return (
        <FormControl sx={{ m: 1 }} component="fieldset">
            <FormLabel component="legend">{capitalize(name)}</FormLabel>
                <RadioGroup aria-label={name} value={value} onChange={handleChange}>
                    {options.map(optionMapper)}
                </RadioGroup>
        </FormControl>
    )
}

type SelectElementProps<Options extends readonly Option[]> = { name: string, state: [Options[number], React.Dispatch<React.SetStateAction<Options[number]>>], options: Options };
export function SelectElement<Options extends readonly Option[]>({name, state, options}: SelectElementProps<Options>) 
{
    const [value, setState] = state;
    const handleChange = (e: any) => setState(e.target.value);
    const optionMapper = (option: Option, i: number) => <MenuItem key={i} value={option}>{cap(option)}</MenuItem>;

    return (
        <FormControl sx={{ m: 1 }}>
            <InputLabel>{capitalize(name)}</InputLabel>
            <Select value={value} label={capitalize(name)} onChange={handleChange}>
                {options.map(optionMapper)}
            </Select>
        </FormControl>
    )
}

type MultipleSelectElementProps<Options extends readonly Option[]> = { name: string, state: [Partial<Options>, React.Dispatch<React.SetStateAction<Partial<Options>>>], options: Options };
export function MultipleSelectElement<Options extends readonly Option[]>({name, state, options}: MultipleSelectElementProps<Options>) 
{
    const [value, setState] = state;
    const handleChange = (e: any) => setState(typeof e.target.value === 'string' ? e.target.value.split(',') : e.target.value);
    const optionMapper = (option: Option, i: number) => (
        <MenuItem key={i} value={option}>
            <Checkbox checked={value.indexOf(option) > -1} />
            <ListItemText primary={cap(option)} />
        </MenuItem>
    );

    return (
        <FormControl sx={{ m: 1 }}>
            <InputLabel>{capitalize(name)}</InputLabel>
            <Select value={value} label={capitalize(name)} onChange={handleChange} multiple renderValue={(s) => s.map(cap).join(', ')}>
                {options.map(optionMapper)}
            </Select>
        </FormControl>
    )
}

interface IBaseFormElement 
{
    name: string;
}

interface ITextElement extends IBaseFormElement
{
    kind: "Text";
}

interface IPasswordElement extends IBaseFormElement
{
    kind: "Password";
}

interface INumberElement extends IBaseFormElement
{
    kind: "Number";
}

interface IRadioElement<Options extends Option[]> extends IBaseFormElement
{
    kind: "Radio";
    options: Options;
}

interface ISelectElement<Options extends Option[]> extends IBaseFormElement
{
    kind: "Select";
    options: Options;
}

interface IMultipleSelectElement<Options extends Option[]> extends IBaseFormElement
{
    kind: "MultipleSelect";
    options: Options;
}

interface ICheckboxElement extends IBaseFormElement
{
    kind: "Checkbox";
}

interface ISwitchElement extends IBaseFormElement
{
    kind: "Switch";
}

type IFormElement<O extends Option[] = []> = ITextElement | IPasswordElement | INumberElement | IRadioElement<O> | ISelectElement<O> | IMultipleSelectElement<O> | ICheckboxElement | ISwitchElement;

type IFormElementMap<E extends IFormElement<any>> = 
    E extends ITextElement ? string :
    E extends IPasswordElement ? string:
    E extends INumberElement ? number :
    E extends IRadioElement<infer O> ? O[number] :
    E extends ISelectElement<infer O> ? O[number] :
    E extends IMultipleSelectElement<infer O> ? Partial<O> :
    E extends ICheckboxElement ? boolean :
    E extends ISwitchElement ? boolean :
    never;