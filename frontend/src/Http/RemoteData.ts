import {Result} from './Result';

export type RemoteData<T, E> =
    | { type: 'not loaded', value: undefined, error: undefined }
    | { type: 'loading', value: undefined, error: undefined }
    | { type: 'loaded', value: T, error: undefined }
    | { type: 'refreshing', value: T, error: undefined }
    | { type: 'failure', value: undefined, error: E }

const notLoaded = <V, E>(): RemoteData<V, E> => ({
    type: 'not loaded',
    value: undefined,
    error: undefined,
});

const loading = <V, E>(): RemoteData<V, E> => ({
    type: 'loading',
    value: undefined,
    error: undefined,
});

const loaded = <V, E>(value: V): RemoteData<V, E> => ({
    type: 'loaded',
    value,
    error: undefined,
});

const refreshing = <V, E>(value: V): RemoteData<V, E> => ({
    type: 'refreshing',
    value,
    error: undefined,
});

const failure = <V, E>(error: E): RemoteData<V, E> => ({
    type: 'failure',
    value: undefined,
    error,
});

const ofResult = <T, E>(result: Result<T, E>): RemoteData<T, E> =>
    result.isOk
        ? loaded(result.data)
        : failure(result.reason);

const startLoading = <T, E>(oldData?: T): RemoteData<T, E> =>
    oldData === undefined
        ? loading()
        : refreshing(oldData);

export const remoteData = {
    notLoaded,
    loading,
    loaded,
    refreshing,
    failure,
    ofResult,
    startLoading,
};
