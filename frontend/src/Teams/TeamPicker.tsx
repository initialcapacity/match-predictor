import {useDispatch, useSelector} from 'react-redux';
import {AppState} from '../App/StateStore';
import {match} from 'ts-pattern';
import {ReactElement, useEffect, useMemo, useState} from 'react';
import {Team, TeamList} from './TeamsState';
import {Select} from '../Forms/Inputs';
import {forecastRequestState} from './ForecastRequestState';

type Side = 'home' | 'away'

const TeamSelector = (props: { teamList: TeamList, side: Side }): ReactElement => {
    const dispatch = useDispatch();
    const otherSide = props.side === 'home' ? 'away' : 'home';
    const selectedTeam = useSelector((app: AppState) => app.forecastRequest[props.side]);
    const otherSelectedTeam = useSelector((app: AppState) => app.forecastRequest[otherSide]);

    const [league, setLeague] = useState<string>('');

    const teamsForCurrentLeague = useMemo<Team[]>(
        () => props.teamList.teams.filter(t => t.leagues.includes(league)),
        [league]
    );

    useEffect(() => {
        if (!selectedTeam) {
            setLeague('');
        }
    }, [selectedTeam]);

    const setTeam = (teamName: string) => {
        const team = teamsForCurrentLeague.filter(t => t.name === teamName).pop();

        if (team) {
            match(props.side)
                .with('home', () => dispatch(forecastRequestState.setHome(team)))
                .with('away', () => dispatch(forecastRequestState.setAway(team)))
                .exhaustive();
        }
    };

    return <>
        <fieldset>
            <legend>{props.side}</legend>
            <Select
                id={props.side + '-league'}
                label={'league'}
                value={league}
                onChange={league => setLeague(league)}
                options={props.teamList.leagues}
            />
            <Select
                id={props.side + '-team'}
                label="name"
                value={selectedTeam?.name}
                required
                options={teamsForCurrentLeague.map(t => t.name)}
                onChange={teamName => setTeam(teamName)}
                isDisabled={teamName => teamName == otherSelectedTeam?.name}
            />
        </fieldset>
    </>;
};

const TeamPicker = (props: { side: Side }): ReactElement => {
    const teams = useSelector((app: AppState) => app.teams.data);

    return match(teams)
        .with({type: 'not loaded'}, () => <></>)
        .with({type: 'loading'}, () => <>Loading</>)
        .with({type: 'loaded'}, ({value}) => <TeamSelector teamList={value} side={props.side}/>)
        .with({type: 'refreshing'}, ({value}) => <TeamSelector teamList={value} side={props.side}/>)
        .with({type: 'failure'}, data => <>{data.error}</>)
        .exhaustive();
};

export default TeamPicker;
