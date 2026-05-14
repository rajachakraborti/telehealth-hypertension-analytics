import React, { useState } from 'react';
import { generateReport, exportToCsv } from '../../services/api';

const ReportGenerator = () => {
    const [reportType, setReportType] = useState('pdf');
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);
    const [success, setSuccess] = useState('');

    const datasetId = localStorage.getItem('dataset_id');

    const handleGenerate = async () => {
        if (!datasetId) {
            setError('No dataset loaded. Please upload a file first.');
            return;
        }
        setLoading(true);
        setError(null);
        setSuccess('');
        try {
            if (reportType === 'pdf') {
                await generateReport(datasetId, 'Telehealth Hypertension Analytics Report');
                setSuccess('PDF downloaded successfully.');
            } else {
                await exportToCsv(datasetId);
                setSuccess('CSV downloaded successfully.');
            }
        } catch (err) {
            setError(err.response?.data?.detail || err.message || 'Failed to generate report.');
        } finally {
            setLoading(false);
        }
    };

    return (
        <div style={s.wrap}>
            <h2>Generate Report</h2>
            <p style={s.muted}>Export your dataset and analytics as a PDF summary or raw CSV.</p>

            {!datasetId && (
                <div style={s.warn}>No dataset loaded — please upload a file first.</div>
            )}

            <div style={s.field}>
                <label style={s.label}>Select Report Type</label>
                <select style={s.select} value={reportType} onChange={(e) => setReportType(e.target.value)}>
                    <option value="pdf">PDF — Summary report with statistics</option>
                    <option value="csv">CSV — Raw dataset export</option>
                </select>
            </div>

            <button
                onClick={handleGenerate}
                disabled={loading || !datasetId}
                style={{
                    ...s.btn,
                    backgroundColor: loading || !datasetId ? '#d9d9d9' : '#1890ff',
                    cursor: loading || !datasetId ? 'not-allowed' : 'pointer',
                }}
            >
                {loading ? 'Generating…' : `Generate ${reportType.toUpperCase()}`}
            </button>

            {error && (
                <div style={s.errorBox}>
                    <p style={{ color: '#cf1322', margin: 0 }}>{error}</p>
                </div>
            )}

            {success && (
                <div style={s.successBox}>
                    <p style={{ color: '#52c41a', margin: 0 }}>{success}</p>
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
    label: { display: 'block', marginBottom: '6px', fontWeight: 600, fontSize: '14px' },
    select: { width: '100%', maxWidth: '400px', padding: '8px 12px', border: '1px solid #d9d9d9', borderRadius: '4px', fontSize: '14px' },
    btn: { padding: '10px 24px', color: 'white', border: 'none', borderRadius: '4px', fontSize: '15px' },
    errorBox: { marginTop: '16px', padding: '12px 16px', backgroundColor: '#fff2f0', border: '1px solid #ffccc7', borderRadius: '4px' },
    successBox: { marginTop: '16px', padding: '12px 16px', backgroundColor: '#f6ffed', border: '1px solid #b7eb8f', borderRadius: '4px' },
};

export default ReportGenerator;
