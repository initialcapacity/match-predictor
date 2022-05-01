import * as schemawax from 'schemawax';
import {http} from '../Http/Http';
import {Model} from './ModelsState';

const modelsDecoder: schemawax.Decoder<Model[]> =
    schemawax.object({
        required: {
            models: schemawax.array(schemawax.string)
        }
    }).andThen(json => json.models.map(name => ({name})));

const fetch = (): Promise<Model[]> => {
    return http.sendRequest('/api/models', modelsDecoder);
};

export const modelsApi = {
    fetch,
};
