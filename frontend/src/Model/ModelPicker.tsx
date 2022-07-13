import {useDispatch, useSelector} from 'react-redux';
import {AppState} from '../App/StateStore';
import {match} from 'ts-pattern';
import {ReactElement} from 'react';
import {ModelList} from './ModelsState';
import {Select} from '../Forms/Inputs';
import {forecastRequestState} from '../Teams/ForecastRequestState';


const ModelSelector = (props: { modelList: ModelList }): ReactElement => {
    const dispatch = useDispatch();
    const selectedModel = useSelector((app: AppState) => app.forecastRequest.model);

    const models = props.modelList.models;

    const setModel = (modelName: string) => {
        const model = models.filter(t => t.name === modelName).pop();

        if (model) {
            dispatch(forecastRequestState.setModel(model));
        }
    };

    return <Select
        id="model-name"
        label="model"
        value={selectedModel?.name}
        required
        options={models.map(t => t.name)}
        onChange={modelName => setModel(modelName)}
    />;
};

const ModelPicker = (): ReactElement => {
    const models = useSelector((app: AppState) => app.models.data);

    return match(models)
        .with({type: 'loading'}, () => <>Loading</>)
        .with({type: 'not loaded'}, () => <>No models available</>)
        .with({type: 'loaded'}, ({value}) => <ModelSelector modelList={value}/>)
        .with({type: 'refreshing'}, ({value}) => <ModelSelector modelList={value}/>)
        .with({type: 'failure'}, data => <>{data.error}</>)
        .exhaustive();
};

export default ModelPicker;
