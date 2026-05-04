import React, { useState, useEffect } from 'react';

const PreprocessingHistory = () => {
    const [history, setHistory] = useState([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        // Simulate loading history from localStorage or API
        const savedHistory = localStorage.getItem('preprocessingHistory');
        if (savedHistory) {
            try {
                setHistory(JSON.parse(savedHistory));
            } catch (e) {
                setHistory([]);
            }
        }
        setLoading(false);
    }, []);

    const clearHistory = () => {
        localStorage.removeItem('preprocessingHistory');
        setHistory([]);
    };

    if (loading) {
        return <div style={{ padding: '20px' }}>Loading...</div>;
    }

    return (
        <div className="preprocessing-history" style={{ padding: '20px' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '20px' }}>
                <h2>Preprocessing History</h2>
                {history.length > 0 && (
                    <button
                        onClick={clearHistory}
                        style={{
                            padding: '8px 16px',
                            backgroundColor: '#ff4d4f',
                            color: 'white',
                            border: 'none',
                            borderRadius: '4px',
                            cursor: 'pointer'
                        }}
                    >
                        Clear History
                    </button>
                )}
            </div>

            <p style={{ marginBottom: '20px', color: '#666' }}>
                View the history of all preprocessing steps applied to your data.
            </p>

            <table style={{ width: '100%', borderCollapse: 'collapse', backgroundColor: 'white', boxShadow: '0 2px 8px rgba(0,0,0,0.1)' }}>
                <thead>
                    <tr style={{ backgroundColor: '#fafafa' }}>
                        <th style={{ padding: '12px', textAlign: 'left', borderBottom: '1px solid #e8e8e8' }}>Step</th>
                        <th style={{ padding: '12px', textAlign: 'left', borderBottom: '1px solid #e8e8e8' }}>Description</th>
                        <th style={{ padding: '12px', textAlign: 'left', borderBottom: '1px solid #e8e8e8' }}>Timestamp</th>
                    </tr>
                </thead>
                <tbody>
                    {history.length > 0 ? (
                        history.map((step, index) => (
                            <tr key={index}>
                                <td style={{ padding: '12px', borderBottom: '1px solid #e8e8e8' }}>{step.step}</td>
                                <td style={{ padding: '12px', borderBottom: '1px solid #e8e8e8' }}>{step.description}</td>
                                <td style={{ padding: '12px', borderBottom: '1px solid #e8e8e8' }}>{new Date(step.timestamp).toLocaleString()}</td>
                            </tr>
                        ))
                    ) : (
                        <tr>
                            <td colSpan="3" style={{ padding: '40px', textAlign: 'center', color: '#999' }}>
                                No preprocessing steps applied yet. Apply imputation or outlier detection to see history.
                            </td>
                        </tr>
                    )}
                </tbody>
            </table>
        </div>
    );
};

export default PreprocessingHistory;