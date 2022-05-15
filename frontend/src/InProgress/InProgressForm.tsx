import {ReactElement, useEffect} from 'react';
import {useDispatch, useSelector} from 'react-redux';
import {AppState} from '../App/StateStore';
import {match} from 'ts-pattern';
import {Checkbox} from '../Forms/Inputs';
import {forecastRequestState} from '../Teams/ForecastRequestState';
import ScenarioForm from './ScenarioForm';
import './InProgressForm.css';

const InProgressPicker = (): ReactElement => {
    const dispatch = useDispatch();
    const matchStatus = useSelector((app: AppState) => app.forecastRequest.matchStatus);
    const inProgress = matchStatus.type == 'in progress';

    const checkbox = <Checkbox
        id="in-progress"
        label="In progress"
        checked={inProgress}
        onChange={(checked) => {
            if (checked) {
                dispatch(forecastRequestState.setInProgress({
                    awayGoals: 0,
                    homeGoals: 0,
                    minutesElapsed: 0,
                }));
            } else {
                dispatch(forecastRequestState.setNotStarted);
            }
        }}
    />;

    return <fieldset className="column">
        {checkbox}
        <ScenarioForm/>
    </fieldset>;
};

const InProgressForm = (): ReactElement => {
    const dispatch = useDispatch();
    const model = useSelector((app: AppState) => app.forecastRequest.model);

    useEffect(() => {
        if (!model?.predicts_in_progress) {
            dispatch(forecastRequestState.setNotStarted);
        }
    }, [model]);

    return match(model)
        .with(undefined, () => <></>)
        .with({predicts_in_progress: false}, () => <></>)
        .with({predicts_in_progress: true}, () => <InProgressPicker/>)
        .exhaustive();
};

export default InProgressForm;
