import {Action, Reducer} from 'redux';
import {match} from 'ts-pattern';
import {remoteData, RemoteData} from '../Http/RemoteData';
import {Result} from '../Http/Result';
import {Fixture} from '../Teams/ForecastRequestState';
import {Http} from '../Http/Http';

export type Outcome = 'home' | 'away' | 'draw'

export type Forecast = {
    fixture: Fixture,
    outcome: Outcome,
    model_name: string
    confidence?: number,
};

export type ForecastState = {
    data: RemoteData<Forecast, Http.Error>
};

const initialState: ForecastState = {
    data: remoteData.notLoaded()
};

type ForecastAction =
    | { type: 'forecast/start loading' }
    | { type: 'forecast/finished loading', value: Result<Forecast, Http.Error> }

const isForecastAction = (variable: unknown): variable is ForecastAction =>
    (variable as ForecastAction).type.startsWith('forecast/');

const startLoading: ForecastAction =
    {type: 'forecast/start loading'};

const finishedLoading = (value: Result<Forecast, Http.Error>): ForecastAction =>
    ({type: 'forecast/finished loading', value});

const reducer: Reducer<ForecastState, Action> =
    (state = initialState, action: Action): ForecastState => {
        if (!isForecastAction(action)) return state;

        return match<ForecastAction, ForecastState>(action)
            .with({type: 'forecast/start loading'}, () => ({data: remoteData.loading()}))
            .with({type: 'forecast/finished loading'}, ({value}) => ({data: remoteData.ofResult(value)}))
            .exhaustive();
    };

export const forecastState = {
    startLoading,
    finishedLoading,
    reducer,
};
