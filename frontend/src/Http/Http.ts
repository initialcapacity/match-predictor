import * as schemawax from 'schemawax';
import {result, Result} from './Result';

export declare namespace Http {
    type Error =
        | { name: 'connection error' }
        | { name: 'server error', message?: string }
        | { name: 'deserialization error', json?: string }
}

const connectionError: Http.Error =
    {name: 'connection error'};

const serverError = (message?: string): Http.Error =>
    ({name: 'server error', message});

const deserializationError = (json?: string): Http.Error =>
    ({name: 'deserialization error', json});

const sendRequest = async <T>(request: RequestInfo, decoder: schemawax.Decoder<T>): Promise<Result<T, Http.Error>> => {
    const response = await fetch(request).catch(() => undefined);
    if (response === undefined) {
        return result.err(connectionError);
    }

    if (!response.ok) {
        return response.text()
            .then(message => result.err<T, Http.Error>(serverError(message)))
            .catch(() => result.err(serverError()));
    }

    const json = await response.json().catch(() => undefined);
    if (json === undefined) {
        return result.err(deserializationError());
    }

    const decodedJson = decoder.decode(json);
    if (decodedJson === null) {
        const actualJson = JSON.stringify(json);
        return result.err(deserializationError(actualJson));
    }

    return result.ok(decodedJson);
};

export const http = {
    connectionError,
    serverError,
    deserializationError,
    sendRequest
};
