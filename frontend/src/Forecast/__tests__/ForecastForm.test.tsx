import {render} from '@testing-library/react';
import {TestAppContext} from '../../testSupport/TestAppContext';
import ForecastForm from '../ForecastForm';
import {Store} from 'redux';
import {AppState, stateStore} from '../../App/StateStore';
import userEvent from '@testing-library/user-event';
import {forecastApi} from '../ForecastApi';
import {Forecast} from '../ForecastState';
import {mocked} from 'jest-mock';
import {waitForPromise} from '../../testSupport/PromiseHelpers';

jest.mock('../ForecastApi');

describe('ForecastForm', () => {
    let store: Store<AppState>;

    beforeEach(() => {
        store = stateStore.create();
    });

    test('submit', async () => {
        const forecast: Forecast = {
            fixture: {
                home: 'Chelsea',
                away: 'Manchester City',
                season: 2022,
                league: 'england',
            },
            outcome: 'home'
        };

        const mockResponse = Promise.resolve(forecast);
        mocked(forecastApi).fetchFor.mockImplementation(() => mockResponse);

        const page = render(<TestAppContext store={store}>
            <ForecastForm/>
        </TestAppContext>);

        userEvent.type(page.getByLabelText('Home'), 'Chelsea');
        userEvent.type(page.getByLabelText('Away'), 'Manchester City');
        userEvent.type(page.getByLabelText('League'), 'england');
        userEvent.clear(page.getByLabelText('Season'));
        userEvent.type(page.getByLabelText('Season'), '2022');

        page.getByText('Submit').click();

        expect(mocked(forecastApi).fetchFor.mock.calls.length).toEqual(1);
        expect(mocked(forecastApi).fetchFor.mock.calls[0][0]).toEqual({
            away: 'Manchester City',
            home: 'Chelsea',
            league: 'england',
            season: 2022
        });

        await waitForPromise(mockResponse);

        expect(store.getState().forecast.data.type).toEqual('loaded');
    });

    test('error', async () => {
        const mockResponse = Promise.reject('A problem occurred');
        mocked(forecastApi).fetchFor.mockImplementation(() => mockResponse);

        const page = render(<TestAppContext store={store}>
            <ForecastForm/>
        </TestAppContext>);

        userEvent.type(page.getByLabelText('Home'), 'Chelsea');
        userEvent.type(page.getByLabelText('Away'), 'Manchester City');
        userEvent.type(page.getByLabelText('League'), 'england');
        userEvent.clear(page.getByLabelText('Season'));
        userEvent.type(page.getByLabelText('Season'), '2022');

        page.getByText('Submit').click();

        await waitForPromise(mockResponse);

        expect(store.getState().forecast.data.type).toEqual('failure');
    });
});
