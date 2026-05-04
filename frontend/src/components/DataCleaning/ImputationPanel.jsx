import React, { useState } from 'react';
import { cleanData } from '../../services/api';

const ImputationPanel = () => {
    const [method, setMethod] = useState('mean');
    const [loading, setLoading] = useState(false);
    const [result, setResult] = useState(null);
    const [error, setError] = useState(null);

    const handleImpute = async () => {
        setLoading(true);
        setError(null);
        setResult(null);

        try {
            const response = await cleanData(null, {
                imputation_method: method,
                handle_missing: true
            });
            setResult(response);
        } catch (err) {
            setError('Failed to apply imputation. Please make sure data is loaded.');
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="imputation-panel" style={{ padding: '20px' }}>
            <h2>Data Imputation</h2>
            <p style={{ marginBottom: '20px', color: '#666' }}>
                Handle missing values in your dataset by selecting an imputation method below.
            </p>

            <div style={{ marginBottom: '20px' }}>
                <h3 style={{ marginBottom: '15px' }}>Select Imputation Method:</h3>
                <div style={{ display: 'flex', flexDirection: 'column', gap: '10px' }}>
                    <label style={{ display: 'flex', alignItems: 'center', gap: '10px', cursor: 'pointer' }}>
                        <input
                            type="radio"
                            value="mean"
                            checked={method === 'mean'}
                            onChange={() => setMethod('mean')}
                        />
                        <span><strong>Mean Imputation</strong> - Replace missing values with column mean</span>
                    </label>
                    <label style={{ display: 'flex', alignItems: 'center', gap: '10px', cursor: 'pointer' }}>
                        <input
                            type="radio"
                            value="median"
                            checked={method === 'median'}
                            onChange={() => setMethod('median')}
                        />
                        <span><strong>Median Imputation</strong> - Replace missing values with column median</span>
                    </label>
                    <label style={{ display: 'flex', alignItems: 'center', gap: '10px', cursor: 'pointer' }}>
                        <input
                            type="radio"
                            value="mice"
                            checked={method === 'mice'}
                            onChange={() => setMethod('mice')}
                        />
                        <span><strong>MICE Imputation</strong> - Multiple Imputation by Chained Equations</span>
                    </label>
                    <label style={{ display: 'flex', alignItems: 'center', gap: '10px', cursor: 'pointer' }}>
                        <input
                            type="radio"
                            value="knn"
                            checked={method === 'knn'}
                            onChange={() => setMethod('knn')}
                        />
                        <span><strong>KNN Imputation</strong> - K-Nearest Neighbors imputation</span>
                    </label>
                </div>
            </div>

            <button
                onClick={handleImpute}
                disabled={loading}
                style={{
                    padding: '12px 24px',
                    backgroundColor: '#1890ff',
                    color: 'white',
                    border: 'none',
                    borderRadius: '4px',
                    fontSize: '16px',
                    cursor: loading ? 'not-allowed' : 'pointer',
                    opacity: loading ? 0.7 : 1
                }}
            >
                {loading ? 'Applying...' : 'Apply Imputation'}
            </button>

            {error && (
                <div style={{ marginTop: '20px', padding: '15px', backgroundColor: '#fff2f0', border: '1px solid #ffccc7', borderRadius: '4px' }}>
                    <p style={{ color: '#cf1322', margin: 0 }}>{error}</p>
                </div>
            )}

            {result && (
                <div style={{ marginTop: '20px', padding: '15px', backgroundColor: '#f6ffed', border: '1px solid #b7eb8f', borderRadius: '4px' }}>
                    <p style={{ color: '#52c41a', margin: 0 }}>Imputation applied successfully!</p>
                </div>
            )}
        </div>
    );
};

export default ImputationPanel;