import './App.css';
import logo from '../logo.svg';
import {stateStore} from './StateStore';
import {Provider} from 'react-redux';
import Forecaster from '../Forecast/Forecaster';
import {appConfig, AppConfigContext} from './AppConfig';

const Header = () => <header>
    <div className="container">
        <div className="title">
            <img src={logo} alt="soccer ball logo" className="logo"/>
            <h1>Match Predictor</h1>
        </div>
    </div>
</header>;

const App = () => <>
    <AppConfigContext.Provider value={appConfig.fromEnv()}>
        <Provider store={stateStore.create()}>
            <Header/>
            <Forecaster/>
        </Provider>
    </AppConfigContext.Provider>
</>;

export default App;
