import {render} from '@testing-library/react';
import {TestAppContext} from '../../testSupport/TestAppContext';
import ForecastForm from '../ForecastForm';
import {Store} from 'redux';
import {AppState, stateStore} from '../../App/StateStore';
import {forecastApi} from '../ForecastApi';
import {Forecast} from '../ForecastState';
import {mocked} from 'jest-mock';
import {waitForPromise} from '../../testSupport/PromiseHelpers';
import {teamsApi} from '../../Teams/TeamsApi';
import {Team} from '../../Teams/TeamsState';
import {fixtureState} from '../../Teams/FixtureState';

jest.mock('../ForecastApi');
jest.mock('../../Teams/TeamsApi');

describe('ForecastForm', () => {
    let store: Store<AppState>;
    const chelsea = {name: 'Chelsea', leagues: ['england']};
    const burnley = {name: 'Burnley', leagues: ['england']};

    const teams: Team[] = [
        chelsea,
        burnley,
        {name: 'Rangers', leagues: ['scotland']},
    ];
    const mockTeamsResponse = Promise.resolve(teams);

    beforeEach(() => {
        store = stateStore.create();
        store.dispatch(fixtureState.setHome(chelsea));
        store.dispatch(fixtureState.setAway(burnley));

        mocked(teamsApi).fetch.mockImplementation(() => mockTeamsResponse);
    });

    test('loads teams', async () => {
        render(<TestAppContext store={store}>
            <ForecastForm/>
        </TestAppContext>);

        await waitForPromise(mockTeamsResponse);

        const teamList = store.getState().teams.data;
        expect(teamList.type).toEqual('loaded');
        if (teamList.type === 'loaded') {
            expect(teamList.value).toEqual({
                leagues: ['england', 'scotland'],
                teams
            });
        }
    });

    test('loads teams error', async () => {
        mocked(teamsApi).fetch.mockImplementation(() => Promise.reject('something happened'));

        render(<TestAppContext store={store}>
            <ForecastForm/>
        </TestAppContext>);

        await waitForPromise(mockTeamsResponse);

        const teamList = store.getState().teams.data;
        expect(teamList.type).toEqual('failure');
        if (teamList.type === 'failure') {
            expect(teamList.error).toEqual('something happened');
        }
    });

    test('submit', async () => {
        store.dispatch(fixtureState.setHome(chelsea));
        store.dispatch(fixtureState.setAway(burnley));

        const forecast: Forecast = {
            fixture: {home: chelsea, away: burnley, league: 'england'},
            outcome: 'home'
        };

        const mockForecastResponse = Promise.resolve(forecast);
        mocked(forecastApi).fetchFor.mockImplementation(() => mockForecastResponse);

        const page = render(<TestAppContext store={store}>
            <ForecastForm/>
        </TestAppContext>);

        page.getByText('Submit').click();

        expect(mocked(forecastApi).fetchFor.mock.calls.length).toEqual(1);
        expect(mocked(forecastApi).fetchFor.mock.calls[0][0]).toEqual({
            away: burnley,
            home: chelsea,
        });

        await waitForPromise(mockForecastResponse);

        expect(store.getState().forecast.data.type).toEqual('loaded');
    });

    test('submit error', async () => {
        const mockResponse = Promise.reject('A problem occurred');
        mocked(forecastApi).fetchFor.mockImplementation(() => mockResponse);

        const page = render(<TestAppContext store={store}>
            <ForecastForm/>
        </TestAppContext>);

        page.getByText('Submit').click();

        await waitForPromise(mockResponse);

        expect(store.getState().forecast.data.type).toEqual('failure');
    });
});
