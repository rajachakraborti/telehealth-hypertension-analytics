import React, { useState } from 'react';
import { detectOutliers } from '../../services/api';

const OutlierDetection = () => {
    const [data, setData] = useState([]);
    const [outliers, setOutliers] = useState([]);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);

    const handleDetectOutliers = async () => {
        setLoading(true);
        setError(null);
        try {
            const response = await detectOutliers(data);
            setOutliers(response.data);
        } catch (err) {
            setError('Error detecting outliers. Please try again.');
        } finally {
            setLoading(false);
        }
    };

    return (
        <div>
            <h2>Outlier Detection</h2>
            <button onClick={handleDetectOutliers} disabled={loading}>
                {loading ? 'Detecting...' : 'Detect Outliers'}
            </button>
            {error && <p className="error">{error}</p>}
            {outliers.length > 0 && (
                <div>
                    <h3>Detected Outliers</h3>
                    <ul>
                        {outliers.map((outlier, index) => (
                            <li key={index}>{JSON.stringify(outlier)}</li>
                        ))}
                    </ul>
                </div>
            )}
        </div>
    );
};

export default OutlierDetection;