import {Action, Reducer} from 'redux';
import {match} from 'ts-pattern';
import {remoteData, RemoteData} from '../Http/RemoteData';
import {Result} from '../Http/Result';


export interface Model {
    name: string;
    predicts_in_progress: boolean;
}

export interface ModelList {
    models: Model[];
}

export type ModelsState = {
    data: RemoteData<ModelList, string>
};

const initialState: ModelsState = {
    data: remoteData.notLoaded()
};

type ModelsAction =
    | { type: 'models/start loading' }
    | { type: 'models/finished loading', value: Result<Model[], string> }

const isModelsAction = (variable: unknown): variable is ModelsAction =>
    (variable as ModelsAction).type.startsWith('models/');

const startLoading: ModelsAction =
    {type: 'models/start loading'};

const finishedLoading = (value: Result<Model[], string>): ModelsAction =>
    ({type: 'models/finished loading', value});

const reducer: Reducer<ModelsState, Action> = (state = initialState, action: Action): ModelsState => {
    if (!isModelsAction(action)) return state;

    return match(action)
        .with({type: 'models/start loading'}, (): ModelsState => ({
            data: remoteData.loading()
        }))
        .with({type: 'models/finished loading'}, ({value}): ModelsState => {
            if (value.isOk) {
                return {
                    data: remoteData.loaded({
                        models: value.data,
                    })
                };
            } else {
                return {data: remoteData.failure(value.reason)};
            }
        })
        .exhaustive();
};

export const modelsState = {
    startLoading,
    finishedLoading,
    reducer,
};
