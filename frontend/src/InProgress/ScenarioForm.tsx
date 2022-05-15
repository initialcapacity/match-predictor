import {ReactElement} from 'react';
import {useDispatch, useSelector} from 'react-redux';
import {AppState} from '../App/StateStore';
import {NumberInput} from '../Forms/Inputs';
import {forecastRequestState} from '../Teams/ForecastRequestState';

const ScenarioForm = (): ReactElement => {
    const dispatch = useDispatch();
    const matchStatus = useSelector((app: AppState) => app.forecastRequest.matchStatus);

    if (matchStatus.type == 'not started') {
        return <></>;
    }

    const scenario = {
        minutesElapsed: matchStatus.minutesElapsed,
        homeGoals: matchStatus.homeGoals,
        awayGoals: matchStatus.awayGoals,
    };

    return <fieldset>
        <NumberInput
            id="home-goals"
            label="home goals"
            value={scenario.homeGoals}
            min={0}
            onChange={(homeGoals) => dispatch(forecastRequestState.setInProgress({...scenario, homeGoals}))}
            required={true}
        />
        <NumberInput
            id="away-goals"
            label="away goals"
            value={scenario.awayGoals}
            min={0}
            onChange={(awayGoals) => dispatch(forecastRequestState.setInProgress({...scenario, awayGoals}))}
            required={true}
        />
        <NumberInput
            id="minutes-elapsed"
            label="minutes elapsed"
            value={scenario.minutesElapsed}
            min={0}
            max={90}
            onChange={(minutesElapsed) => dispatch(forecastRequestState.setInProgress({...scenario, minutesElapsed}))}
            required={true}
        />
    </fieldset>;
};

export default ScenarioForm;
