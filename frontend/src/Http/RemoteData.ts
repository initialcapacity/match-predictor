export type RemoteData<T, E> =
    | { type: 'not loaded' }
    | { type: 'loading' }
    | { type: 'loaded', value: T }
    | { type: 'failure', error: E }

const notLoaded = <V, E>(): RemoteData<V, E> => ({
    type: 'not loaded',
});

const loading = <V, E>(): RemoteData<V, E> => ({
    type: 'loading',
});

const loaded = <V, E>(value: V): RemoteData<V, E> => ({
    type: 'loaded',
    value,
});

const failure = <V, E>(error: E): RemoteData<V, E> => ({
    type: 'failure',
    error,
});

export const remoteData = {
    notLoaded,
    loading,
    loaded,
    failure,
};
