import './Inputs.css';
import {ReactElement} from 'react';

export const NumberInput = (props: {
    id: string;
    label: string;
    value: number | undefined;
    onChange: (value: number) => unknown;
    required?: boolean
    min?: number
    max?: number
}): ReactElement =>
    <label>
        {props.label}
        <input id={props.id}
               type="number"
               placeholder={props.label}
               defaultValue={props.value}
               required={props.required}
               min={props.min}
               max={props.max}
               onChange={e => {
                   const value = parseInt(e.target.value);

                   if (!isNaN(value)) {
                       props.onChange(value);
                   }
               }}
        />
    </label>;

export const TextInput = (props: {
    id: string;
    label: string;
    value: string | undefined;
    onChange: (value: string) => unknown;
    required?: boolean
}): ReactElement =>
    <label>
        {props.label}
        <input id={props.id}
               type="text"
               placeholder={props.label}
               value={props.value}
               required={props.required}
               onChange={e => props.onChange(e.target.value)}
        />
    </label>;

export const Checkbox = (props: {
    id: string;
    label: string;
    checked: boolean;
    onChange: (value: boolean) => unknown;
}): ReactElement =>
    <label>
        <input id={props.id}
               type="checkbox"
               checked={props.checked}
               onChange={e => props.onChange(e.target.checked)}
        />
        {props.label}
    </label>;

type SelectProps = {
    id: string
    label: string
    value: string | undefined
    onChange: (value: string) => unknown
    required?: boolean
    options: string[]
    isDisabled?: (optionValue: string) => boolean
};

export const Select = (props: SelectProps): ReactElement => {
    const isDisabled = props.isDisabled ?? (() => false);
    const optionElements = props.options.map(option =>
        <option key={option} value={option} disabled={isDisabled(option)}>
            {option}
        </option>
    );

    return <label>
        {props.label}
        <select
            id={props.id}
            value={props.value}
            required={props.required}
            onChange={e => props.onChange(e.target.value)}
        >

            <option value="">Please choose and option</option>
            {optionElements}
        </select>
    </label>;
};
