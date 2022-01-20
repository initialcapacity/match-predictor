import './Inputs.css';
import {ReactElement} from 'react';

export const TextInput = (props: {
    label: string;
    value: string | undefined;
    onChange: (value: string) => unknown;
    required?: boolean
}): ReactElement =>
    <label>
        <span>{props.label}</span>
        <input type="text"
               placeholder={props.label}
               value={props.value}
               required={props.required}
               onChange={e => props.onChange(e.target.value)}
        />
    </label>;

export const Select = (props: {
    id: string
    label: string
    value: string | undefined
    onChange: (value: string) => unknown
    required?: boolean
    options: string[]
}): ReactElement => {
    const optionElements = props.options.map(option => <option key={option} value={option}>{option}</option>);

    return <label>
        <span>{props.label}</span>
        <select
            id={props.id}
            value={props.value}
            required={props.required}
            onChange={e => props.onChange(e.target.value)}>

            <option value="">Please choose and option</option>
            {optionElements}
        </select>
    </label>;
};
