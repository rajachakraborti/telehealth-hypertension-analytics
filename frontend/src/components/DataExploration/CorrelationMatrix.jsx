import React, { useEffect, useState } from 'react';
import { fetchCorrelationMatrix } from '../../services/api';

const heatColor = (val) => {
    if (val == null) return '#f5f5f5';
    const v = Math.max(-1, Math.min(1, val));
    if (v >= 0) {
        const intensity = Math.round(v * 180);
        return `rgb(${255 - intensity}, ${255 - intensity}, 255)`;
    }
    const intensity = Math.round(-v * 180);
    return `rgb(255, ${255 - intensity}, ${255 - intensity})`;
};

const CorrelationMatrix = ({ datasetId: propDatasetId }) => {
    const datasetId = propDatasetId || localStorage.getItem('dataset_id');
    const [columns, setColumns] = useState([]);
    const [rows, setRows] = useState([]);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);

    useEffect(() => {
        if (!datasetId) return;
        const load = async () => {
            setLoading(true);
            setError(null);
            try {
                const data = await fetchCorrelationMatrix(datasetId);
                setColumns(data.columns || []);
                setRows(data.rows || []);
            } catch (err) {
                setError(err.response?.data?.detail || err.message || 'Failed to load correlation data');
            } finally {
                setLoading(false);
            }
        };
        load();
    }, [datasetId]);

    if (!datasetId) return (
        <div style={s.wrap}>
            <h2>Correlation Matrix</h2>
            <p style={s.muted}>Please upload a dataset first.</p>
        </div>
    );

    if (loading) return <div style={s.wrap}>Loading…</div>;
    if (error) return <div style={s.wrap}><p style={{ color: '#cf1322' }}>Error: {error}</p></div>;
    if (rows.length === 0) return (
        <div style={s.wrap}>
            <h2>Correlation Matrix</h2>
            <p style={s.muted}>No numeric columns found for correlation.</p>
        </div>
    );

    return (
        <div style={s.wrap}>
            <h2>Correlation Matrix</h2>
            <p style={s.muted}>Pearson correlation between numeric columns. Blue = positive, red = negative.</p>
            <div style={s.tableWrap}>
                <table style={s.table}>
                    <thead>
                        <tr>
                            <th style={s.th}></th>
                            {columns.map((col) => (
                                <th key={col} style={{ ...s.th, ...s.rotated }}>{col}</th>
                            ))}
                        </tr>
                    </thead>
                    <tbody>
                        {rows.map((row) => (
                            <tr key={row.column}>
                                <td style={s.rowLabel}>{row.column}</td>
                                {columns.map((col) => {
                                    const val = row[col];
                                    return (
                                        <td
                                            key={col}
                                            title={val != null ? val.toFixed(4) : 'N/A'}
                                            style={{ ...s.cell, backgroundColor: heatColor(val) }}
                                        >
                                            {val != null ? val.toFixed(2) : '—'}
                                        </td>
                                    );
                                })}
                            </tr>
                        ))}
                    </tbody>
                </table>
            </div>
        </div>
    );
};

const s = {
    wrap: { padding: '20px' },
    muted: { color: '#999', marginBottom: '12px' },
    tableWrap: { overflowX: 'auto' },
    table: { borderCollapse: 'collapse', fontSize: '12px' },
    th: { padding: '6px 10px', border: '1px solid #e8e8e8', backgroundColor: '#fafafa', fontWeight: 600, textAlign: 'center' },
    rotated: { whiteSpace: 'nowrap' },
    rowLabel: { padding: '6px 10px', border: '1px solid #e8e8e8', fontWeight: 600, whiteSpace: 'nowrap', backgroundColor: '#fafafa' },
    cell: { padding: '6px 10px', border: '1px solid #e8e8e8', textAlign: 'center', minWidth: '56px', cursor: 'default' },
};

export default CorrelationMatrix;
