import * as schemawax from 'schemawax';
import {http} from '../Http/Http';
import {Model} from './ModelsState';
import {result} from '../Http/Result';

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

const noModels: Model[] = [];

const fetch = async (): Promise<Model[]> =>
    http.sendRequest('/api/models', modelsDecoder)
        .then(result.orElse(noModels));

export const modelsApi = {
    fetch,
};
