import React from 'react';
import {env} from './Env';

export type AppConfig = {
    enableUpcomingGames: boolean
}

const emptyAppConfig: AppConfig = {
    enableUpcomingGames: false
};

const fromEnv = (): AppConfig => ({
    enableUpcomingGames: env.get('enableUpcomingGames') === 'true',
});

export const AppConfigContext = React.createContext(emptyAppConfig);

export const appConfig = {
    fromEnv,
};
