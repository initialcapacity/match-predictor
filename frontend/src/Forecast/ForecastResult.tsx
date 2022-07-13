import {useSelector} from 'react-redux';
import {AppState} from '../App/StateStore';
import {match, __} from 'ts-pattern';
import {ReactElement} from 'react';
import {Forecast} from './ForecastState';

const SingleForecast = (props: { forecast: Forecast }): ReactElement => {
    const fixture = props.forecast.fixture;

    const teams = match(props.forecast.outcome)
        .with('home', () => <><strong>{fixture.home.name}</strong> v. {fixture.away.name}</>)
        .with('away', () => <>{fixture.home.name} v. <strong>{fixture.away.name}</strong></>)
        .with('draw', () => <em>{fixture.home.name} v. {fixture.away.name}</em>)
        .exhaustive();

    const confidenceHtml = match(props.forecast.confidence)
        .with(undefined, () => <></>)
        .with(__.number, (confidence) => {
            const roundedConfidence = Math.round(confidence * 100);
            return <div>Confidence: {roundedConfidence}%</div>;
        })
        .exhaustive();

    return <>
        <div>{teams} ({props.forecast.outcome.toUpperCase()})</div>
        {confidenceHtml}
    </>;
};

const ForecastResult = (): ReactElement => {
    const forecast = useSelector((app: AppState) => app.forecast.data);

    const result = match(forecast)
        .with({type: 'loading'}, () => <>Loading</>)
        .with({type: 'not loaded'}, () => <>Submit a fixture to see results</>)
        .with({type: 'refreshing'}, ({value}) => <SingleForecast forecast={value}/>)
        .with({type: 'loaded'}, ({value}) => <SingleForecast forecast={value}/>)
        .with({type: 'failure'}, () => <>There was a problem</>)
        .exhaustive();

    return <article>{result}</article>;
};

export default ForecastResult;
