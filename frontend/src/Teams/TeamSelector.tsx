import {useDispatch, useSelector} from 'react-redux';
import {AppState} from '../App/StateStore';
import {match} from 'ts-pattern';
import {ReactElement, useMemo, useState} from 'react';
import {Team, TeamList} from './TeamsState';
import {Select} from '../Forms/Inputs';
import {fixtureState} from './FixtureState';

type Side = 'home' | 'away'

const TeamSelector = (props: { teamList: TeamList, side: Side }): ReactElement => {
    const dispatch = useDispatch();
    const selectedTeam = useSelector((app: AppState) => app.fixture[props.side]);
    const [country, setCountry] = useState<string>('');

    const teams = useMemo<Team[]>(
        () => props.teamList.teams.filter(t => t.country === country),
        [country]
    );

    const setTeam = (teamName: string) => {
        const team = teams.filter(t => t.name === teamName).pop();

        if (team) {
            match(props.side)
                .with('home', () => dispatch(fixtureState.setHome(team)))
                .with('away', () => dispatch(fixtureState.setAway(team)))
                .exhaustive();
        }
    };

    return <>
        <fieldset>
            <legend>{props.side}</legend>
            <Select
                id={props.side + '-country'}
                label={'country'}
                value={country}
                onChange={country => setCountry(country)}
                options={props.teamList.countries}
            />
            <Select
                id={props.side + '-team'}
                label="name"
                value={selectedTeam?.name}
                required
                options={teams.map(t => t.name)}
                onChange={teamName => setTeam(teamName)}
            />
        </fieldset>
    </>;
};

const TeamPicker = (props: { side: Side }): ReactElement => {
    const teams = useSelector((app: AppState) => app.teams.data);

    return match(teams)
        .with({type: 'loading'}, () => <>Loading</>)
        .with({type: 'not loaded'}, () => <>No teams available</>)
        .with({type: 'loaded'}, data => <TeamSelector teamList={data.value} side={props.side}/>)
        .with({type: 'failure'}, data => <>{data.error}</>)
        .exhaustive();
};

export default TeamPicker;
