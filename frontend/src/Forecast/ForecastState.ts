import {Action, Reducer} from 'redux';
import {match} from 'ts-pattern';
import {remoteData, RemoteData} from '../Http/RemoteData';
import {Result} from '../Http/Result';
import {Fixture} from '../Teams/FixtureState';

export type Outcome = 'home' | 'away' | 'draw'

export type Forecast = {
    fixture: Fixture,
    outcome: Outcome,
    confidence?: number,
};

export type ForecastState = {
    data: RemoteData<Forecast, string>
};

const initialState: ForecastState = {
    data: remoteData.notLoaded()
};

type ForecastAction =
    | { type: 'forecast/start loading' }
    | { type: 'forecast/finished loading', value: Result<Forecast, string> }

const isForecastAction = (variable: unknown): variable is ForecastAction =>
    (variable as ForecastAction).type.startsWith('forecast/');

const startLoading: ForecastAction =
    {type: 'forecast/start loading'};

const finishedLoading = (value: Result<Forecast, string>): ForecastAction =>
    ({type: 'forecast/finished loading', value});

const reducer: Reducer<ForecastState, Action> = (state = initialState, action: Action): ForecastState => {
    if (!isForecastAction(action)) return state;

    return match(action)
        .with({type: 'forecast/start loading'}, (): ForecastState => ({
            data: remoteData.loading()
        }))
        .with({type: 'forecast/finished loading'}, ({value}): ForecastState => {
            if (value.isOk) {
                return {data: remoteData.loaded(value.data)};
            } else {
                return {data: remoteData.failure(value.reason)};
            }
        })
        .exhaustive();
};

export const forecastState = {
    startLoading,
    finishedLoading,
    reducer,
};
