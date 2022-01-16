import App from '../App';
import {render} from '@testing-library/react';

describe('App', () => {
    test('App', async () => {
        const content = render(<App/>);

        expect(await content.findByText('Match Predictor')).toBeTruthy();
    });
});
