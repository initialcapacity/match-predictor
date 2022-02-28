import {Action, combineReducers, createStore, Reducer, Store} from 'redux';
import {forecastState, ForecastState} from '../Forecast/ForecastState';
import {FixtureState, fixtureState} from '../Teams/FixtureState';
import {teamsState, TeamsState} from '../Teams/TeamsState';

export type AppState = {
    forecast: ForecastState
    fixture: FixtureState
    teams: TeamsState
};

const appReducer: Reducer<AppState, Action> =
    combineReducers({
        forecast: forecastState.reducer,
        fixture: fixtureState.reducer,
        teams: teamsState.reducer
    });

const create = (): Store<AppState> =>
    createStore(appReducer);

export const stateStore = {
    create,
};
