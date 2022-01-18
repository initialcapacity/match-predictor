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
