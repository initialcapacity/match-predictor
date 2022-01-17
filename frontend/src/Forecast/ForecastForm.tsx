import {FormEvent, ReactElement, useState} from 'react';
import {NumberInput, Inputs} from '../Forms/Inputs';
import {Fixture, forecastState} from './ForecastState';
import {useDispatch} from 'react-redux';
import {forecastApi} from './ForecastApi';
import {result} from '../Http/Result';

const emptyFixture = {
    home: '',
    away: '',
    league: '',
    season: 2021
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
            league: fields.league,
            season: fields.season,
        };

        forecastApi.fetchFor(fixture)
            .then(forecast => {
                setFields(emptyFixture);
                dispatch(forecastState.finishedLoading(result.ok(forecast)));
            })
            .catch(message => {
                return dispatch(forecastState.finishedLoading(result.err(message)));
            });
    };

    return <form onSubmit={submit}>
        <Inputs
            label="Home"
            value={fields.home}
            onChange={home => setFields({...fields, home})}
        />
        <Inputs
            label="Away"
            value={fields.away}
            onChange={away => setFields({...fields, away})}
        />
        <Inputs
            label="League"
            value={fields.league}
            onChange={league => setFields({...fields, league})}
        />
        <NumberInput
            label="Season"
            value={fields.season || ''}
            onChange={season => setFields({...fields, season})}
        />
        <button type="submit">Submit</button>
    </form>;
};

export default ForecastForm;
