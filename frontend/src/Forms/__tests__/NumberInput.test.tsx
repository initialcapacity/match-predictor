import {fireEvent, render} from '@testing-library/react';
import {NumberInput} from '../Inputs';

describe('NumberInput', () => {
    test('valid input', () => {
        const callback = jest.fn();

        const input = render(<NumberInput id="test" label="test" value={1} onChange={callback}/>)
            .getByLabelText('test');

        fireEvent.change(input, {target: {value: '3'}});

        expect(callback).toHaveBeenCalledWith(3);
    });

    test('invalid input', () => {
        const callback = jest.fn();

        const input = render(<NumberInput id="test" label="test" value={1} onChange={callback}/>)
            .getByLabelText('test');

        fireEvent.change(input, {target: {value: ''}});
        expect(callback).not.toHaveBeenCalled();

        fireEvent.change(input, {target: {value: undefined}});
        expect(callback).not.toHaveBeenCalled();

        fireEvent.change(input, {target: {value: 'pickles'}});
        expect(callback).not.toHaveBeenCalled();
    });
});
