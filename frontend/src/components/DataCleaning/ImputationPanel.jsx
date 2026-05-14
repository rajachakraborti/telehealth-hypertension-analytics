import React, { useState } from 'react';
import { imputeData } from '../../services/api';

const METHODS = [
    { value: 'mean', label: 'Mean', desc: 'Replace missing values with column mean' },
    { value: 'median', label: 'Median', desc: 'Replace missing values with column median' },
    { value: 'mice', label: 'MICE', desc: 'Multiple Imputation by Chained Equations' },
    { value: 'knn', label: 'KNN', desc: 'K-Nearest Neighbors imputation (k=5)' },
];

const ImputationPanel = () => {
    const [method, setMethod] = useState('mean');
    const [loading, setLoading] = useState(false);
    const [result, setResult] = useState(null);
    const [error, setError] = useState(null);

    const datasetId = localStorage.getItem('dataset_id');

    const handleImpute = async () => {
        if (!datasetId) {
            setError('No dataset loaded. Please upload a file first.');
            return;
        }
        setLoading(true);
        setError(null);
        setResult(null);
        try {
            const response = await imputeData(datasetId, method);
            setResult(response);
        } catch (err) {
            setError(err.response?.data?.detail || 'Failed to apply imputation.');
        } finally {
            setLoading(false);
        }
    };

    return (
        <div style={{ padding: '20px' }}>
            <h2>Data Imputation</h2>
            <p style={{ marginBottom: '20px', color: '#666' }}>
                Handle missing values in your dataset by selecting an imputation method below.
            </p>

            {!datasetId && (
                <div style={s.warn}>
                    No dataset loaded — please upload a file first.
                </div>
            )}

            <div style={{ marginBottom: '20px' }}>
                <h3 style={{ marginBottom: '15px' }}>Select Imputation Method:</h3>
                <div style={{ display: 'flex', flexDirection: 'column', gap: '10px' }}>
                    {METHODS.map(({ value, label, desc }) => (
                        <label key={value} style={{ display: 'flex', alignItems: 'center', gap: '10px', cursor: 'pointer' }}>
                            <input
                                type="radio"
                                value={value}
                                checked={method === value}
                                onChange={() => setMethod(value)}
                            />
                            <span><strong>{label} Imputation</strong> — {desc}</span>
                        </label>
                    ))}
                </div>
            </div>

            <button
                onClick={handleImpute}
                disabled={loading || !datasetId}
                style={{
                    padding: '12px 24px',
                    backgroundColor: loading || !datasetId ? '#d9d9d9' : '#1890ff',
                    color: 'white',
                    border: 'none',
                    borderRadius: '4px',
                    fontSize: '16px',
                    cursor: loading || !datasetId ? 'not-allowed' : 'pointer',
                }}
            >
                {loading ? 'Applying…' : 'Apply Imputation'}
            </button>

            {error && (
                <div style={s.errorBox}>
                    <p style={{ color: '#cf1322', margin: 0 }}>{error}</p>
                </div>
            )}

            {result && (
                <div style={s.successBox}>
                    <p style={{ color: '#52c41a', margin: '0 0 8px' }}>
                        {result.message}
                    </p>
                    <div style={s.stats}>
                        <div style={s.stat}><strong>{result.values_imputed}</strong><span>Values filled</span></div>
                        <div style={s.stat}><strong>{result.missing_before}</strong><span>Missing before</span></div>
                        <div style={s.stat}><strong>{result.missing_after}</strong><span>Missing after</span></div>
                    </div>
                </div>
            )}
        </div>
    );
};

const s = {
    warn: {
        marginBottom: '16px', padding: '12px 16px',
        backgroundColor: '#fffbe6', border: '1px solid #ffe58f',
        borderRadius: '4px', color: '#ad6800',
    },
    errorBox: {
        marginTop: '20px', padding: '15px',
        backgroundColor: '#fff2f0', border: '1px solid #ffccc7', borderRadius: '4px',
    },
    successBox: {
        marginTop: '20px', padding: '20px',
        backgroundColor: '#f6ffed', border: '1px solid #b7eb8f', borderRadius: '4px',
    },
    stats: { display: 'flex', gap: '24px', marginTop: '8px' },
    stat: {
        display: 'flex', flexDirection: 'column', alignItems: 'center',
        gap: '2px', fontSize: '13px', color: '#555',
    },
};

export default ImputationPanel;
