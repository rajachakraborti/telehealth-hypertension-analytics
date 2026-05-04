import React, { useState } from 'react';
import { generateReport } from '../../services/api';

const ReportGenerator = () => {
    const [reportType, setReportType] = useState('pdf');
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);
    const [successMessage, setSuccessMessage] = useState('');

    const handleReportTypeChange = (event) => {
        setReportType(event.target.value);
    };

    const handleGenerateReport = async () => {
        setLoading(true);
        setError(null);
        setSuccessMessage('');

        try {
            const response = await generateReport(reportType);
            if (response.status === 200) {
                setSuccessMessage('Report generated successfully!');
            } else {
                throw new Error('Failed to generate report');
            }
        } catch (err) {
            setError(err.message);
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="report-generator">
            <h2>Generate Report</h2>
            <div>
                <label htmlFor="report-type">Select Report Type:</label>
                <select id="report-type" value={reportType} onChange={handleReportTypeChange}>
                    <option value="pdf">PDF</option>
                    <option value="csv">CSV</option>
                </select>
            </div>
            <button onClick={handleGenerateReport} disabled={loading}>
                {loading ? 'Generating...' : 'Generate Report'}
            </button>
            {error && <p className="error">{error}</p>}
            {successMessage && <p className="success">{successMessage}</p>}
        </div>
    );
};

export default ReportGenerator;