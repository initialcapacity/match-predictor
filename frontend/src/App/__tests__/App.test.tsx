import App from '../App';
import {render} from '@testing-library/react';
import {TestAppContext} from '../../TestSupport/TestAppContext';

describe('App', () => {

    test('App', async () => {
        const page = render(<TestAppContext><App/></TestAppContext>);

        expect(await page.findByText('Match Predictor')).toBeTruthy();
    });
});
