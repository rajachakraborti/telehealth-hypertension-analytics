import React, { useState, useEffect } from 'react';
import { fetchHyperparameterOptions, tuneHyperparameters } from '../../services/api';

const HyperparameterTuning = () => {
    const [model, setModel] = useState('');
    const [hyperparameters, setHyperparameters] = useState({});
    const [tuningResults, setTuningResults] = useState(null);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);

    useEffect(() => {
        if (model) {
            fetchHyperparameterOptions(model)
                .then(options => setHyperparameters(options))
                .catch(err => setError(err.message));
        }
    }, [model]);

    const handleModelChange = (event) => {
        setModel(event.target.value);
    };

    const handleTuning = () => {
        setLoading(true);
        tuneHyperparameters(model, hyperparameters)
            .then(results => {
                setTuningResults(results);
                setLoading(false);
            })
            .catch(err => {
                setError(err.message);
                setLoading(false);
            });
    };

    return (
        <div>
            <h2>Hyperparameter Tuning</h2>
            <div>
                <label>Select Model:</label>
                <select value={model} onChange={handleModelChange}>
                    <option value="">Select a model</option>
                    <option value="logistic_regression">Logistic Regression</option>
                    <option value="random_forest">Random Forest</option>
                    <option value="xgboost">XGBoost</option>
                </select>
            </div>
            {model && (
                <div>
                    <h3>Hyperparameters</h3>
                    {/* Render hyperparameter inputs based on the selected model */}
                    {Object.keys(hyperparameters).map(param => (
                        <div key={param}>
                            <label>{param}:</label>
                            <input
                                type="text"
                                value={hyperparameters[param]}
                                onChange={(e) => setHyperparameters({ ...hyperparameters, [param]: e.target.value })}
                            />
                        </div>
                    ))}
                    <button onClick={handleTuning} disabled={loading}>
                        {loading ? 'Tuning...' : 'Tune Hyperparameters'}
                    </button>
                </div>
            )}
            {tuningResults && (
                <div>
                    <h3>Tuning Results</h3>
                    <pre>{JSON.stringify(tuningResults, null, 2)}</pre>
                </div>
            )}
            {error && <div style={{ color: 'red' }}>{error}</div>}
        </div>
    );
};

export default HyperparameterTuning;