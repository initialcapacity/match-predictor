import React from 'react';
import ForecastForm from './ForecastForm';
import ForecastResult from './ForecastResult';
import {UpcomingGameList} from './UpcomingGameList';
import {AppConfigContext} from '../App/AppConfig';

const Forecaster = (): React.ReactElement => {
    const appConfig = React.useContext(AppConfigContext);
    const enableUpcomingGames = appConfig.enableUpcomingGames;

    return <>
        {enableUpcomingGames &&
            <section>
                <div className="container">
                    <h2>Upcoming Games</h2>
                    <UpcomingGameList/>
                </div>
            </section>
        }
        <section>
            <div className="container">
                <h2>Fixture</h2>
                <ForecastForm/>
            </div>
        </section>
        <section>
            <div className="container">
                <h2>Result</h2>
                <ForecastResult/>
            </div>
        </section>
    </>;
};

export default Forecaster;
