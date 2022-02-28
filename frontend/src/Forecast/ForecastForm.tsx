import {FormEvent, ReactElement, useEffect, useState} from 'react';
import {forecastState} from './ForecastState';
import {useDispatch, useSelector} from 'react-redux';
import {forecastApi} from './ForecastApi';
import {result} from '../Http/Result';
import {teamsApi} from '../Teams/TeamsApi';
import {Fixture, fixtureState} from '../Teams/FixtureState';
import TeamPicker from '../Teams/TeamSelector';
import {AppState} from '../App/StateStore';
import {teamsState} from '../Teams/TeamsState';

const ForecastForm = (): ReactElement => {
    const dispatch = useDispatch();

    const fixture = useSelector((app: AppState) => app.fixture);

    useEffect(() => {
        dispatch(teamsState.startLoading);
        teamsApi.fetch()
            .then(teams => dispatch(teamsState.finishedLoading(result.ok(teams))))
            .catch(message => dispatch(teamsState.finishedLoading(result.err(message))));
    }, []);


    const submit = (e: FormEvent) => {
        e.preventDefault();
        if (!fixture.home || !fixture.away) return;
        dispatch(forecastState.startLoading);

        forecastApi.fetchFor(fixture as Fixture)
            .then(forecast => {
                dispatch(fixtureState.clear);
                dispatch(forecastState.finishedLoading(result.ok(forecast)));
            })
            .catch(message => dispatch(forecastState.finishedLoading(result.err(message))));
    };

    return <article>
        <form onSubmit={submit}>
            <TeamPicker side="home"/>
            <TeamPicker side="away"/>

            <button type="submit">Submit</button>
        </form>
    </article>;
};

export default ForecastForm;
