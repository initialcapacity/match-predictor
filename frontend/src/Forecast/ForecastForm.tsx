import {FormEvent, ReactElement, useEffect} from 'react';
import {forecastState} from './ForecastState';
import {useDispatch, useSelector} from 'react-redux';
import {forecastApi} from './ForecastApi';
import {result} from '../Http/Result';
import {teamsApi} from '../Teams/TeamsApi';
import {ForecastRequest} from '../Teams/ForecastRequestState';
import TeamPicker from '../Teams/TeamPicker';
import {AppState} from '../App/StateStore';
import {teamsState} from '../Teams/TeamsState';
import {modelsApi} from '../Model/ModelsApi';
import {modelsState} from '../Model/ModelsState';
import ModelPicker from '../Model/ModelPicker';
import InProgressForm from '../InProgress/InProgressForm';

export const ForecastForm = (): ReactElement => {
    const dispatch = useDispatch();

    const forecastRequest = useSelector((app: AppState) => app.forecastRequest);

    useEffect(() => {
        dispatch(teamsState.startLoading);
        dispatch(modelsState.startLoading);
        teamsApi.fetch()
            .then(teams => dispatch(teamsState.finishedLoading(result.ok(teams))))
            .catch(message => dispatch(teamsState.finishedLoading(result.err(message))));
        modelsApi.fetch()
            .then(models => dispatch(modelsState.finishedLoading(result.ok(models))))
            .catch(message => dispatch(teamsState.finishedLoading(result.err(message))));
    }, []);


    const submit = (e: FormEvent) => {
        e.preventDefault();
        if (!forecastRequest.home || !forecastRequest.away || !forecastRequest.model) return;
        dispatch(forecastState.startLoading);

        forecastApi.fetchFor(forecastRequest as ForecastRequest)
            .then(forecast => {
                dispatch(forecastState.finishedLoading(forecast));
            });
    };

    return <article>
        <form onSubmit={submit}>
            <TeamPicker side="home"/>
            <TeamPicker side="away"/>
            <fieldset>
                <ModelPicker/>
            </fieldset>
            <InProgressForm/>

            <button type="submit">Submit</button>
        </form>
    </article>;
};

export default ForecastForm;
