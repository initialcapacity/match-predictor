import * as Redux from 'redux';
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

const appReducer: Redux.Reducer<AppState, Redux.Action> =
    Redux.combineReducers({
        forecast: forecastState.reducer,
        forecastRequest: forecastRequestState.reducer,
        teams: teamsState.reducer,
        models: modelsState.reducer,
    });

const create = (): Redux.Store<AppState> =>
    Redux.createStore(appReducer);

export const stateStore = {
    create,
};
