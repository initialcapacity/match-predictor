import {FormEvent, ReactElement, useState} from 'react';
import {Select} from '../Forms/Inputs';
import {Fixture, forecastState} from './ForecastState';
import {useDispatch} from 'react-redux';
import {forecastApi} from './ForecastApi';
import {result} from '../Http/Result';

const emptyFixture = {
    home: '',
    away: '',
};

const ForecastForm = (): ReactElement => {
    const [fields, setFields] = useState<Fixture>(emptyFixture);
    const dispatch = useDispatch();

    const submit = (e: FormEvent) => {
        e.preventDefault();
        dispatch(forecastState.startLoading);
        const fixture = {
            home: fields.home,
            away: fields.away,
        };

        forecastApi.fetchFor(fixture)
            .then(forecast => {
                setFields(emptyFixture);
                dispatch(forecastState.finishedLoading(result.ok(forecast)));
            })
            .catch(message => dispatch(forecastState.finishedLoading(result.err(message))));
    };

    const teams = [
        'Chelsea',
        'Tottenham Hotspur',
        'Arsenal',
        'Juventus',
        'Southampton',
    ];

    return <article>
        <form onSubmit={submit}>
            <fieldset>
                <Select
                    id="home-team"
                    label="Home"
                    value={fields.home}
                    required
                    options={teams}
                    onChange={home => setFields({...fields, home})}
                />
                <span className="versus">vs.</span>
                <Select
                    id="away-team"
                    label="Away"
                    value={fields.away}
                    required
                    options={teams}
                    onChange={away => setFields({...fields, away})}
                />
            </fieldset>
            <button type="submit">Submit</button>
        </form>
    </article>;
};

export default ForecastForm;
