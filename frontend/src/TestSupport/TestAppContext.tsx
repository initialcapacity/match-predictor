import {AppState, stateStore} from '../App/StateStore';
import {ReactElement, ReactNode} from 'react';
import {Store} from 'redux';
import {Provider} from 'react-redux';
import {AppConfig, AppConfigContext} from '../App/AppConfig';

type TestAppContextProps = {
    store?: Store<AppState>,
    appConfig?: AppConfig,
    children: ReactNode,
}

export const TestAppContext = (props: TestAppContextProps): ReactElement => {
    const defaultAppConfig: AppConfig = {
        enableUpcomingGames: true
    };

    return <Provider store={props.store ?? stateStore.create()}>
        <AppConfigContext.Provider value={props.appConfig ?? defaultAppConfig}>
            {props.children}
        </AppConfigContext.Provider>
    </Provider>;
};
