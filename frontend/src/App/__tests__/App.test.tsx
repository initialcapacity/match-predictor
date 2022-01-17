import App from '../App';
import {render} from '@testing-library/react';

describe('App', () => {
    test('App', async () => {
        const page = render(<App/>);

        expect(await page.findByText('Match Predictor')).toBeTruthy();
    });
});
