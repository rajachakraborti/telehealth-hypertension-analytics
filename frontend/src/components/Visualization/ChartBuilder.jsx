import React, { useState, useEffect } from 'react';
import {
    Chart as ChartJS,
    CategoryScale,
    LinearScale,
    BarElement,
    LineElement,
    PointElement,
    ArcElement,
    Title,
    Tooltip,
    Legend,
} from 'chart.js';
import { Bar, Line, Pie } from 'react-chartjs-2';
import { fetchDataPreview } from '../../services/api';

ChartJS.register(
    CategoryScale, LinearScale, BarElement,
    LineElement, PointElement, ArcElement,
    Title, Tooltip, Legend,
);

const COLORS = [
    'rgba(24,144,255,0.7)', 'rgba(82,196,26,0.7)', 'rgba(250,173,20,0.7)',
    'rgba(245,34,45,0.7)',  'rgba(114,46,209,0.7)', 'rgba(19,194,194,0.7)',
    'rgba(250,84,28,0.7)',  'rgba(235,47,150,0.7)',
];

const ChartBuilder = () => {
    const [columns, setColumns] = useState([]);
    const [rows, setRows] = useState([]);
    const [chartType, setChartType] = useState('bar');
    const [xCol, setXCol] = useState('');
    const [yCol, setYCol] = useState('');
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);

    const datasetId = localStorage.getItem('dataset_id');

    useEffect(() => {
        if (!datasetId) return;
        setLoading(true);
        fetchDataPreview(datasetId)
            .then((d) => {
                setColumns(d.columns || []);
                setRows(d.rows || []);
                const cols = d.columns || [];
                setXCol(cols[0] || '');
                const numericCol = cols.find((c) =>
                    d.rows.length > 0 && typeof d.rows[0][c] === 'number'
                );
                setYCol(numericCol || cols[1] || '');
            })
            .catch(() => setError('Failed to load dataset.'))
            .finally(() => setLoading(false));
    }, []);

    const numericCols = columns.filter((c) => rows.length > 0 && typeof rows[0][c] === 'number');

    const buildChartData = () => {
        if (!xCol || !yCol || rows.length === 0) return null;

        if (chartType === 'pie') {
            const grouped = {};
            rows.forEach((r) => {
                const key = String(r[xCol] ?? 'N/A');
                grouped[key] = (grouped[key] || 0) + (Number(r[yCol]) || 0);
            });
            return {
                labels: Object.keys(grouped),
                datasets: [{
                    data: Object.values(grouped),
                    backgroundColor: COLORS,
                    borderWidth: 1,
                }],
            };
        }

        return {
            labels: rows.map((r) => String(r[xCol] ?? '')),
            datasets: [{
                label: yCol,
                data: rows.map((r) => Number(r[yCol]) || 0),
                backgroundColor: COLORS[0],
                borderColor: COLORS[0].replace('0.7', '1'),
                borderWidth: 1,
                fill: false,
                tension: 0.3,
            }],
        };
    };

    const chartData = buildChartData();
    const chartOptions = {
        responsive: true,
        plugins: { legend: { position: 'top' }, title: { display: false } },
    };

    const ChartComponent = chartType === 'bar' ? Bar : chartType === 'line' ? Line : Pie;

    return (
        <div style={s.wrap}>
            <h2>Chart Builder</h2>

            {!datasetId && <div style={s.warn}>No dataset loaded — please upload a file first.</div>}
            {loading && <p style={s.muted}>Loading data…</p>}
            {error && <div style={s.errorBox}><p style={{ color: '#cf1322', margin: 0 }}>{error}</p></div>}

            {columns.length > 0 && (
                <>
                    <div style={s.controls}>
                        <div style={s.field}>
                            <label style={s.label}>Chart Type</label>
                            <select style={s.select} value={chartType} onChange={(e) => setChartType(e.target.value)}>
                                <option value="bar">Bar</option>
                                <option value="line">Line</option>
                                <option value="pie">Pie</option>
                            </select>
                        </div>
                        <div style={s.field}>
                            <label style={s.label}>{chartType === 'pie' ? 'Category (slice labels)' : 'X Axis'}</label>
                            <select style={s.select} value={xCol} onChange={(e) => setXCol(e.target.value)}>
                                {columns.map((c) => <option key={c} value={c}>{c}</option>)}
                            </select>
                        </div>
                        <div style={s.field}>
                            <label style={s.label}>{chartType === 'pie' ? 'Value (slice size)' : 'Y Axis'}</label>
                            <select style={s.select} value={yCol} onChange={(e) => setYCol(e.target.value)}>
                                {numericCols.map((c) => <option key={c} value={c}>{c}</option>)}
                            </select>
                        </div>
                    </div>

                    {chartData ? (
                        <div style={s.chartWrap}>
                            <ChartComponent data={chartData} options={chartOptions} />
                        </div>
                    ) : (
                        <p style={s.muted}>Select columns above to draw a chart.</p>
                    )}
                </>
            )}
        </div>
    );
};

const s = {
    wrap: { padding: '20px' },
    muted: { color: '#999' },
    warn: { marginBottom: '16px', padding: '12px 16px', backgroundColor: '#fffbe6', border: '1px solid #ffe58f', borderRadius: '4px', color: '#ad6800' },
    errorBox: { marginBottom: '16px', padding: '12px 16px', backgroundColor: '#fff2f0', border: '1px solid #ffccc7', borderRadius: '4px' },
    controls: { display: 'flex', gap: '24px', flexWrap: 'wrap', marginBottom: '24px', alignItems: 'flex-end' },
    field: { display: 'flex', flexDirection: 'column', gap: '4px' },
    label: { fontWeight: 600, fontSize: '13px' },
    select: { padding: '7px 10px', border: '1px solid #d9d9d9', borderRadius: '4px', fontSize: '14px', minWidth: '160px' },
    chartWrap: { maxWidth: '720px' },
};

export default ChartBuilder;
