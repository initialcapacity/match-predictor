import {ReactElement} from 'react';
import ForecastForm from './ForecastForm';
import ForecastResult from './ForecastResult';

const Forecaster = (): ReactElement => <>
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

export default Forecaster;
