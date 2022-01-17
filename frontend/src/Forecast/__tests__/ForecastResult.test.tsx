import {TestAppContext} from '../../testSupport/TestAppContext';
import {Store} from 'redux';
import {AppState, stateStore} from '../../App/StateStore';
import {forecastState} from '../ForecastState';
import ForecastResult from '../ForecastResult';
import {render} from '@testing-library/react';
import {result} from '../../Http/Result';

describe('ForecastResult', () => {
    let store: Store<AppState>;

    beforeEach(() => {
        store = stateStore.create();
    });

    test('not loaded', async () => {
        const page = render(<TestAppContext store={store}>
            <ForecastResult/>
        </TestAppContext>);

        expect(await page.findByText('Submit a fixture to see results')).toBeTruthy();
    });

    test('loading', async () => {
        store.dispatch(forecastState.startLoading);

        const page = render(<TestAppContext store={store}>
            <ForecastResult/>
        </TestAppContext>);

        expect(await page.findByText('Loading')).toBeTruthy();
    });

    test('loaded', async () => {
        store.dispatch(forecastState.finishedLoading(result.ok({
            fixture: {
                home: 'Chelsea',
                away: 'Burnley',
                league: 'england',
                season: 2020
            },
            outcome: 'draw'
        })));

        const page = render(<TestAppContext store={store}>
            <ForecastResult/>
        </TestAppContext>);

        expect(await page.findByText('Chelsea v. Burnley')).toBeTruthy();
        expect(page.container.textContent).toContain('DRAW');
    });

    test('error', async () => {
        store.dispatch(forecastState.finishedLoading(result.err('There was a problem')));

        const page = render(<TestAppContext store={store}>
            <ForecastResult/>
        </TestAppContext>);

        expect(await page.findByText('There was a problem')).toBeTruthy();
    });
});
