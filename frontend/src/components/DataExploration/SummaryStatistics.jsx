import React from 'react';
import { useEffect, useState } from 'react';
import { fetchSummaryStatistics } from '../../services/api';

const SummaryStatistics = ({ datasetId }) => {
    const [statistics, setStatistics] = useState(null);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);

    useEffect(() => {
        if (!datasetId) return;

        const getStatistics = async () => {
            setLoading(true);
            setError(null);
            try {
                const data = await fetchSummaryStatistics(datasetId);
                setStatistics(data);
            } catch (err) {
                setError(err.message || 'Failed to fetch statistics');
            } finally {
                setLoading(false);
            }
        };

        getStatistics();
    }, [datasetId]);

    if (!datasetId) {
        return (
            <div>
                <h2>Summary Statistics</h2>
                <p>Please select a dataset to view statistics.</p>
            </div>
        );
    }

    if (loading) {
        return <div>Loading...</div>;
    }

    if (error) {
        return <div>Error: {error}</div>;
    }

    if (!statistics) {
        return (
            <div>
                <h2>Summary Statistics</h2>
                <p>No statistics available.</p>
            </div>
        );
    }

    return (
        <div>
            <h2>Summary Statistics</h2>
            <table>
                <thead>
                    <tr>
                        <th>Statistic</th>
                        <th>Value</th>
                    </tr>
                </thead>
                <tbody>
                    {Object.entries(statistics).map(([statistic, value]) => (
                        <tr key={statistic}>
                            <td>{statistic}</td>
                            <td>{typeof value === 'object' ? JSON.stringify(value) : value}</td>
                        </tr>
                    ))}
                </tbody>
            </table>
        </div>
    );
};

export default SummaryStatistics;