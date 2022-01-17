import {useSelector} from 'react-redux';
import {AppState} from '../App/StateStore';
import {match} from 'ts-pattern';
import {ReactElement} from 'react';
import {Forecast} from './ForecastState';

const SingleForecast = (props: { forecast: Forecast }): ReactElement => {
    const fixture = props.forecast.fixture;

    const teams = match(props.forecast.outcome)
        .with('home', () => <><strong>{fixture.home}</strong> v. {fixture.away}</>)
        .with('away', () => <>{fixture.home} v. <strong>{fixture.away}</strong></>)
        .with('draw', () => <em>{fixture.home} v. {fixture.away}</em>)
        .exhaustive();

    return <article>
        {teams} ({props.forecast.outcome.toUpperCase()})
    </article>;
};

const ForecastResult = (): ReactElement => {
    const forecast = useSelector((app: AppState) => app.forecast.data);

    return match(forecast)
        .with({type: 'loading'}, () => <article>Loading</article>)
        .with({type: 'not loaded'}, () => <article>Submit a fixture to see results</article>)
        .with({type: 'loaded'}, data => <SingleForecast forecast={data.value}/>)
        .with({type: 'failure'}, data => <article>{data.error}</article>)
        .exhaustive();
};

export default ForecastResult;
