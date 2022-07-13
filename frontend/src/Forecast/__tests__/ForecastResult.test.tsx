import {TestAppContext} from '../../TestSupport/TestAppContext';
import {Store} from 'redux';
import {AppState, stateStore} from '../../App/StateStore';
import {forecastState} from '../ForecastState';
import ForecastResult from '../ForecastResult';
import {render} from '@testing-library/react';
import {result} from '../../Http/Result';
import {forecastTestBuilders} from '../ForecastTestBuilders';
import {http} from '../../Http/Http';

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
        store.dispatch(forecastState.finishedLoading(result.ok(
            forecastTestBuilders.forecast({
                fixture: forecastTestBuilders.fixture({
                    home: forecastTestBuilders.team({name: 'Chelsea'}),
                    away: forecastTestBuilders.team({name: 'Burnley'}),
                }),
                outcome: 'draw'
            })
        )));

        const page = render(<TestAppContext store={store}>
            <ForecastResult/>
        </TestAppContext>);

        expect(await page.findByText('Chelsea v. Burnley')).toBeTruthy();
        expect(page.container.textContent).toContain('DRAW');
    });

    test('loaded with confidence', async () => {
        store.dispatch(forecastState.finishedLoading(result.ok(
            forecastTestBuilders.forecast({
                confidence: .53345,
            })
        )));

        const page = render(<TestAppContext store={store}>
            <ForecastResult/>
        </TestAppContext>);

        expect(await page.findByText('Confidence: 53%')).toBeTruthy();
    });

    test('loaded with confidence round up', async () => {
        store.dispatch(forecastState.finishedLoading(result.ok(
            forecastTestBuilders.forecast({
                confidence: .537,
            })
        )));

        const page = render(<TestAppContext store={store}>
            <ForecastResult/>
        </TestAppContext>);

        expect(await page.findByText('Confidence: 54%')).toBeTruthy();
    });

    test('error', async () => {
        store.dispatch(forecastState.finishedLoading(result.err(http.connectionError)));

        const page = render(<TestAppContext store={store}>
            <ForecastResult/>
        </TestAppContext>);

        expect(await page.findByText('There was a problem')).toBeTruthy();
    });
});
