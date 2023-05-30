import {ReactElement, useEffect, useState} from 'react';
import {UpcomingGamesApi, upcomingGamesApi} from './UpcomingGamesApi';
import {remoteData, RemoteData} from '../Http/RemoteData';
import {match} from 'ts-pattern';
import {Http} from '../Http/Http';

const UpcomingGameRow = ({game}: { game: UpcomingGamesApi.UpcomingGame }): ReactElement =>
    <li>
        <dl>
            <dt>League</dt>
            <dd>{game.league}</dd>
            <dt>Home</dt>
            <dd>{game.home}</dd>
            <dt>Away</dt>
            <dd>{game.away}</dd>
        </dl>
    </li>;

type GamesState =
    RemoteData<UpcomingGamesApi.UpcomingGame[], Http.Error>

type GameListProps = {
    games: UpcomingGamesApi.UpcomingGame[]
    doRefresh: () => void
}

const GameList = ({games, doRefresh}: GameListProps): ReactElement =>
    <>
        <button onClick={doRefresh}>Refresh</button>
        <ul>
            {games.map((game, index) => <UpcomingGameRow key={index} game={game}/>)}
        </ul>
    </>;

export const UpcomingGameList = (props: { currentDate?: Date }): ReactElement => {

    const currentDate = props.currentDate ?? new Date();
    const dateFrom = currentDate.toISOString().slice(0, 10);

    const [gamesState, setGamesState] = useState<GamesState>(remoteData.notLoaded());

    const loadGames = () => {
        setGamesState(remoteData.startLoading(gamesState.value));

        upcomingGamesApi
            .fetch(dateFrom)
            .then(result => setGamesState(remoteData.ofResult(result)));
    };

    useEffect(() => {
        loadGames();
    }, []);

    return match(gamesState)
        .with({type: 'not loaded'}, () =>
            <article/>
        )
        .with({type: 'loading'}, () =>
            <article>Loading data...</article>
        )
        .with({type: 'loaded'}, ({value}) =>
            <article><GameList games={value} doRefresh={loadGames}/></article>
        )
        .with({type: 'refreshing'}, ({value}) =>
            <article>
                Refreshing data...
                <GameList games={value} doRefresh={loadGames}/>
            </article>
        )
        .with({type: 'failure'}, () =>
            <article>There was an error, please try again later.</article>
        )
        .exhaustive();
};
