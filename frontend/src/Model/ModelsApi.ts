import * as schemawax from 'schemawax';
import {http} from '../Http/Http';
import {Model} from './ModelsState';

const modelsDecoder: schemawax.Decoder<Model[]> =
    schemawax.object({
        required: {
            models: schemawax.array(schemawax.object({
                required: {
                    name: schemawax.string,
                    predicts_in_progress: schemawax.boolean
                }
            }))
        }
    }).andThen(json => json.models);

const fetch = (): Promise<Model[]> => {
    return http.sendRequest('/api/models', modelsDecoder);
};

export const modelsApi = {
    fetch,
};
