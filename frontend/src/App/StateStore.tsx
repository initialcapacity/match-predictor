import {Action, combineReducers, createStore, Reducer, Store} from 'redux';
import {forecastState, ForecastState} from '../Forecast/ForecastState';
import {ForecastRequestState, forecastRequestState} from '../Teams/ForecastRequestState';
import {teamsState, TeamsState} from '../Teams/TeamsState';
import {modelsState, ModelsState} from '../Model/ModelsState';

export type AppState = {
    forecast: ForecastState
    forecastRequest: ForecastRequestState
    teams: TeamsState
    models: ModelsState
};

const appReducer: Reducer<AppState, Action> =
    combineReducers({
        forecast: forecastState.reducer,
        forecastRequest: forecastRequestState.reducer,
        teams: teamsState.reducer,
        models: modelsState.reducer,
    });

const create = (): Store<AppState> =>
    createStore(appReducer);

export const stateStore = {
    create,
};
