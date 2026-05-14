import React from 'react';
import { useEffect, useState } from 'react';
import { fetchSummaryStatistics } from '../../services/api';

const fmt = (val) => (val == null ? '—' : Number(val).toLocaleString(undefined, { maximumFractionDigits: 4 }));

const parseStatistics = (stats) => {
    const meta = {
        row_count: stats.row_count,
        column_count: stats.column_count,
        total_missing: stats.total_missing,
        missing_percentage: stats.missing_percentage || {},
    };

    const prefixes = ['mean_', 'median_', 'std_', 'min_', 'max_'];
    const columns = {};
    for (const [key, value] of Object.entries(stats)) {
        const prefix = prefixes.find((p) => key.startsWith(p));
        if (!prefix) continue;
        const col = key.slice(prefix.length);
        if (!columns[col]) columns[col] = {};
        columns[col][prefix.slice(0, -1)] = value;
    }

    return { meta, columns };
};

const SummaryStatistics = ({ datasetId: propDatasetId }) => {
    const datasetId = propDatasetId || localStorage.getItem('dataset_id');
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
                setStatistics(data.statistics);
            } catch (err) {
                setError(err.message || 'Failed to fetch statistics');
            } finally {
                setLoading(false);
            }
        };
        getStatistics();
    }, [datasetId]);

    if (!datasetId) return <div style={styles.wrap}><h2>Summary Statistics</h2><p style={styles.muted}>Please upload a dataset first to view statistics.</p></div>;
    if (loading) return <div style={styles.wrap}>Loading…</div>;
    if (error) return <div style={styles.wrap}><p style={{ color: '#cf1322' }}>Error: {error}</p></div>;
    if (!statistics) return <div style={styles.wrap}><h2>Summary Statistics</h2><p style={styles.muted}>No statistics available.</p></div>;

    const { meta, columns } = parseStatistics(statistics);
    const colNames = Object.keys(columns);

    return (
        <div style={styles.wrap}>
            <h2>Summary Statistics</h2>

            <div style={styles.metaRow}>
                <span style={styles.badge}>Rows: {meta.row_count ?? '—'}</span>
                <span style={styles.badge}>Columns: {meta.column_count ?? '—'}</span>
                <span style={styles.badge}>Missing cells: {meta.total_missing ?? '—'}</span>
            </div>

            {colNames.length > 0 && (
                <div style={styles.tableWrap}>
                    <table style={styles.table}>
                        <thead>
                            <tr>
                                <th style={styles.th}>Column</th>
                                <th style={{ ...styles.th, ...styles.num }}>Mean</th>
                                <th style={{ ...styles.th, ...styles.num }}>Median</th>
                                <th style={{ ...styles.th, ...styles.num }}>Std Dev</th>
                                <th style={{ ...styles.th, ...styles.num }}>Min</th>
                                <th style={{ ...styles.th, ...styles.num }}>Max</th>
                                <th style={{ ...styles.th, ...styles.num }}>Missing %</th>
                            </tr>
                        </thead>
                        <tbody>
                            {colNames.map((col, i) => (
                                <tr key={col} style={i % 2 === 0 ? styles.rowEven : styles.rowOdd}>
                                    <td style={styles.td}>{col}</td>
                                    <td style={{ ...styles.td, ...styles.num }}>{fmt(columns[col].mean)}</td>
                                    <td style={{ ...styles.td, ...styles.num }}>{fmt(columns[col].median)}</td>
                                    <td style={{ ...styles.td, ...styles.num }}>{fmt(columns[col].std)}</td>
                                    <td style={{ ...styles.td, ...styles.num }}>{fmt(columns[col].min)}</td>
                                    <td style={{ ...styles.td, ...styles.num }}>{fmt(columns[col].max)}</td>
                                    <td style={{ ...styles.td, ...styles.num }}>{fmt(meta.missing_percentage[col])}%</td>
                                </tr>
                            ))}
                        </tbody>
                    </table>
                </div>
            )}
        </div>
    );
};

const styles = {
    wrap: { padding: '20px' },
    muted: { color: '#999' },
    metaRow: { display: 'flex', gap: '12px', marginBottom: '20px', flexWrap: 'wrap' },
    badge: {
        padding: '4px 12px',
        backgroundColor: '#f0f5ff',
        border: '1px solid #adc6ff',
        borderRadius: '4px',
        fontSize: '13px',
        color: '#2f54eb',
    },
    tableWrap: { overflowX: 'auto' },
    table: {
        width: '100%',
        borderCollapse: 'collapse',
        fontSize: '14px',
    },
    th: {
        padding: '10px 14px',
        backgroundColor: '#fafafa',
        border: '1px solid #e8e8e8',
        textAlign: 'left',
        fontWeight: 600,
        whiteSpace: 'nowrap',
    },
    td: {
        padding: '8px 14px',
        border: '1px solid #e8e8e8',
        whiteSpace: 'nowrap',
    },
    num: { textAlign: 'right' },
    rowEven: { backgroundColor: '#ffffff' },
    rowOdd: { backgroundColor: '#fafafa' },
};

export default SummaryStatistics;
