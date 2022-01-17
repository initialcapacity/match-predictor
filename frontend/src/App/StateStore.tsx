import {Action, combineReducers, createStore, Reducer, Store} from 'redux';
import {forecastState, ForecastState} from '../Forecast/ForecastState';

export type AppState = {
    forecast: ForecastState
};

const appReducer: Reducer<AppState, Action> =
    combineReducers({
        forecast: forecastState.reducer
    });

const create = (): Store<AppState> =>
    createStore(appReducer);

export const stateStore = {
    create,
};
