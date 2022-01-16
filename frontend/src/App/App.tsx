import './App.css';
import logo from '../logo.svg';

const App = () => <>
    <header>
        <div className="container">
            <div className="title">
                <img src={logo} alt="soccer ball logo" className="logo"/>
                <h1>Match Predictor</h1>
            </div>
        </div>
    </header>
</>;

export default App;
