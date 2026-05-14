import React, { useEffect, useState } from 'react';
import { fetchDataPreview } from '../../services/api';

const DataTable = ({ datasetId: propDatasetId }) => {
    const datasetId = propDatasetId || localStorage.getItem('dataset_id');
    const [columns, setColumns] = useState([]);
    const [rows, setRows] = useState([]);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);
    const [page, setPage] = useState(0);
    const PAGE_SIZE = 10;

    useEffect(() => {
        if (!datasetId) return;
        const load = async () => {
            setLoading(true);
            setError(null);
            try {
                const data = await fetchDataPreview(datasetId);
                setColumns(data.columns || []);
                setRows(data.rows || []);
                setPage(0);
            } catch (err) {
                setError(err.response?.data?.detail || err.message || 'Failed to load data');
            } finally {
                setLoading(false);
            }
        };
        load();
    }, [datasetId]);

    if (!datasetId) return (
        <div style={s.wrap}>
            <h2>Data Exploration Table</h2>
            <p style={s.muted}>Please upload a dataset first.</p>
        </div>
    );

    if (loading) return <div style={s.wrap}>Loading…</div>;
    if (error) return <div style={s.wrap}><p style={{ color: '#cf1322' }}>Error: {error}</p></div>;
    if (rows.length === 0) return (
        <div style={s.wrap}>
            <h2>Data Exploration Table</h2>
            <p style={s.muted}>No data available.</p>
        </div>
    );

    const totalPages = Math.ceil(rows.length / PAGE_SIZE);
    const pageRows = rows.slice(page * PAGE_SIZE, (page + 1) * PAGE_SIZE);

    return (
        <div style={s.wrap}>
            <h2>Data Exploration Table</h2>
            <p style={s.muted}>Showing first {rows.length} rows</p>
            <div style={s.tableWrap}>
                <table style={s.table}>
                    <thead>
                        <tr>
                            {columns.map((col) => (
                                <th key={col} style={s.th}>{col}</th>
                            ))}
                        </tr>
                    </thead>
                    <tbody>
                        {pageRows.map((row, i) => (
                            <tr key={i} style={i % 2 === 0 ? s.rowEven : s.rowOdd}>
                                {columns.map((col) => (
                                    <td key={col} style={s.td}>
                                        {row[col] == null ? <span style={s.null}>null</span> : String(row[col])}
                                    </td>
                                ))}
                            </tr>
                        ))}
                    </tbody>
                </table>
            </div>
            {totalPages > 1 && (
                <div style={s.pager}>
                    <button style={s.btn} onClick={() => setPage((p) => p - 1)} disabled={page === 0}>← Prev</button>
                    <span style={s.pageInfo}>Page {page + 1} of {totalPages}</span>
                    <button style={s.btn} onClick={() => setPage((p) => p + 1)} disabled={page === totalPages - 1}>Next →</button>
                </div>
            )}
        </div>
    );
};

const s = {
    wrap: { padding: '20px' },
    muted: { color: '#999' },
    tableWrap: { overflowX: 'auto' },
    table: { width: '100%', borderCollapse: 'collapse', fontSize: '13px' },
    th: { padding: '8px 12px', backgroundColor: '#fafafa', border: '1px solid #e8e8e8', textAlign: 'left', fontWeight: 600, whiteSpace: 'nowrap' },
    td: { padding: '6px 12px', border: '1px solid #e8e8e8', whiteSpace: 'nowrap', maxWidth: '240px', overflow: 'hidden', textOverflow: 'ellipsis' },
    null: { color: '#bbb', fontStyle: 'italic' },
    rowEven: { backgroundColor: '#fff' },
    rowOdd: { backgroundColor: '#fafafa' },
    pager: { display: 'flex', alignItems: 'center', gap: '12px', marginTop: '12px' },
    btn: { padding: '4px 12px', border: '1px solid #d9d9d9', borderRadius: '4px', cursor: 'pointer', backgroundColor: '#fff' },
    pageInfo: { fontSize: '13px', color: '#666' },
};

export default DataTable;
