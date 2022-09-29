import React from 'react';
import ReactDOM from 'react-dom';
import './reset.css';
import './theme.css';
import './index.css';
import App from './App/App';
import {appConfig, AppConfigContext} from './App/AppConfig';
import {stateStore} from './App/StateStore';
import {Provider} from 'react-redux';

ReactDOM.render(
    <React.StrictMode>
        <AppConfigContext.Provider value={appConfig.fromEnv()}>
            <Provider store={stateStore.create()}>
                <App/>
            </Provider>
        </AppConfigContext.Provider>
    </React.StrictMode>,
    document.getElementById('root')
);
