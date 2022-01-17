import {ReactElement} from 'react';

export const Inputs = (props: {
    label: string;
    value: string | undefined;
    onChange: (value: string) => unknown;
}): ReactElement =>
    <label>
        <span>{props.label}</span>
        <input type="text"
               placeholder={props.label}
               value={props.value}
               onChange={e => props.onChange(e.target.value)}
        />
    </label>;

export const NumberInput = (props: {
    label: string;
    value: number | '';
    onChange: (value: number) => unknown;
}): ReactElement =>
    <label>
        <span>{props.label}</span>
        <input type="number"
               placeholder={props.label}
               value={props.value}
               onChange={e => props.onChange(parseInt(e.target.value))}
        />
    </label>;
