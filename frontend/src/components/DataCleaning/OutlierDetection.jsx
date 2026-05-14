import React, { useState } from 'react';
import { detectOutliers } from '../../services/api';

const METHODS = [
    { value: 'iqr', label: 'IQR', desc: 'Interquartile Range (1.5 × IQR rule)' },
    { value: 'zscore', label: 'Z-Score', desc: 'Values with |z| > 3' },
];

const OutlierDetection = () => {
    const [method, setMethod] = useState('iqr');
    const [results, setResults] = useState(null);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);

    const datasetId = localStorage.getItem('dataset_id');

    const handleDetect = async () => {
        if (!datasetId) {
            setError('No dataset loaded. Please upload a file first.');
            return;
        }
        setLoading(true);
        setError(null);
        setResults(null);
        try {
            const data = await detectOutliers(datasetId, method);
            setResults(data);
        } catch (err) {
            setError(err.response?.data?.detail || 'Error detecting outliers.');
        } finally {
            setLoading(false);
        }
    };

    const totalOutliers = results?.results?.reduce((sum, r) => sum + r.outlier_count, 0) ?? 0;

    return (
        <div style={s.wrap}>
            <h2>Outlier Detection</h2>
            <p style={s.muted}>Detect anomalous values in each numeric column of your dataset.</p>

            {!datasetId && <div style={s.warn}>No dataset loaded — please upload a file first.</div>}

            <div style={s.field}>
                <label style={s.label}>Detection Method</label>
                <div style={{ display: 'flex', gap: '16px' }}>
                    {METHODS.map(({ value, label, desc }) => (
                        <label key={value} style={s.radio}>
                            <input
                                type="radio"
                                value={value}
                                checked={method === value}
                                onChange={() => setMethod(value)}
                            />
                            <span><strong>{label}</strong> — {desc}</span>
                        </label>
                    ))}
                </div>
            </div>

            <button
                onClick={handleDetect}
                disabled={loading || !datasetId}
                style={{
                    ...s.btn,
                    backgroundColor: loading || !datasetId ? '#d9d9d9' : '#1890ff',
                    cursor: loading || !datasetId ? 'not-allowed' : 'pointer',
                }}
            >
                {loading ? 'Detecting…' : 'Detect Outliers'}
            </button>

            {error && <div style={s.errorBox}><p style={{ color: '#cf1322', margin: 0 }}>{error}</p></div>}

            {results && (
                <div style={{ marginTop: '24px' }}>
                    <div style={s.summary}>
                        <span style={s.badge}>{totalOutliers} total outlier{totalOutliers !== 1 ? 's' : ''} found</span>
                        <span style={{ color: '#999', fontSize: '13px' }}>Method: {results.method.toUpperCase()}</span>
                    </div>

                    <div style={s.tableWrap}>
                        <table style={s.table}>
                            <thead>
                                <tr>
                                    <th style={s.th}>Column</th>
                                    <th style={{ ...s.th, ...s.num }}>Outliers</th>
                                    <th style={{ ...s.th, ...s.num }}>Total</th>
                                    <th style={{ ...s.th, ...s.num }}>%</th>
                                    <th style={{ ...s.th, ...s.num }}>Lower Bound</th>
                                    <th style={{ ...s.th, ...s.num }}>Upper Bound</th>
                                    <th style={s.th}>Outlier Values</th>
                                </tr>
                            </thead>
                            <tbody>
                                {results.results.map((row, i) => (
                                    <tr key={row.column} style={i % 2 === 0 ? s.rowEven : s.rowOdd}>
                                        <td style={s.td}>{row.column}</td>
                                        <td style={{ ...s.td, ...s.num, color: row.outlier_count > 0 ? '#cf1322' : '#52c41a', fontWeight: 600 }}>
                                            {row.outlier_count}
                                        </td>
                                        <td style={{ ...s.td, ...s.num }}>{row.total_count}</td>
                                        <td style={{ ...s.td, ...s.num }}>
                                            {row.total_count > 0 ? ((row.outlier_count / row.total_count) * 100).toFixed(1) : 0}%
                                        </td>
                                        <td style={{ ...s.td, ...s.num }}>{row.lower_bound}</td>
                                        <td style={{ ...s.td, ...s.num }}>{row.upper_bound}</td>
                                        <td style={{ ...s.td, color: '#666', fontSize: '12px' }}>
                                            {row.outlier_values.length > 0
                                                ? row.outlier_values.join(', ')
                                                : <span style={{ color: '#bbb' }}>none</span>}
                                        </td>
                                    </tr>
                                ))}
                            </tbody>
                        </table>
                    </div>
                </div>
            )}
        </div>
    );
};

const s = {
    wrap: { padding: '20px' },
    muted: { color: '#666', marginBottom: '20px' },
    warn: { marginBottom: '16px', padding: '12px 16px', backgroundColor: '#fffbe6', border: '1px solid #ffe58f', borderRadius: '4px', color: '#ad6800' },
    field: { marginBottom: '20px' },
    label: { display: 'block', marginBottom: '8px', fontWeight: 600, fontSize: '14px' },
    radio: { display: 'flex', alignItems: 'center', gap: '8px', cursor: 'pointer', fontSize: '14px' },
    btn: { padding: '10px 24px', color: 'white', border: 'none', borderRadius: '4px', fontSize: '15px' },
    errorBox: { marginTop: '16px', padding: '12px 16px', backgroundColor: '#fff2f0', border: '1px solid #ffccc7', borderRadius: '4px' },
    summary: { display: 'flex', alignItems: 'center', gap: '16px', marginBottom: '12px' },
    badge: { padding: '4px 12px', backgroundColor: '#fff1f0', border: '1px solid #ffa39e', borderRadius: '4px', fontSize: '13px', color: '#cf1322', fontWeight: 600 },
    tableWrap: { overflowX: 'auto' },
    table: { width: '100%', borderCollapse: 'collapse', fontSize: '13px' },
    th: { padding: '8px 12px', backgroundColor: '#fafafa', border: '1px solid #e8e8e8', fontWeight: 600, textAlign: 'left', whiteSpace: 'nowrap' },
    td: { padding: '7px 12px', border: '1px solid #e8e8e8', whiteSpace: 'nowrap' },
    num: { textAlign: 'right' },
    rowEven: { backgroundColor: '#fff' },
    rowOdd: { backgroundColor: '#fafafa' },
};

export default OutlierDetection;
