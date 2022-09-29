import './App.css';
import logo from '../logo.svg';
import Forecaster from '../Forecast/Forecaster';

const Header = () => <header>
    <div className="container">
        <div className="title">
            <img src={logo} alt="soccer ball logo" className="logo"/>
            <h1>Match Predictor</h1>
        </div>
    </div>
</header>;

const App = () => <>
    <Header/>
    <Forecaster/>
</>;

export default App;
