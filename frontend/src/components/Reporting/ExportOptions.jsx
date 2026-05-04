import React from 'react';

const ExportOptions = ({ onExport }) => {
    const handleExport = (format) => {
        if (onExport) {
            onExport(format);
        }
    };

    return (
        <div className="export-options">
            <h3>Export Report</h3>
            <button onClick={() => handleExport('pdf')}>Export as PDF</button>
            <button onClick={() => handleExport('csv')}>Export as CSV</button>
            <button onClick={() => handleExport('word')}>Export as Word Document</button>
        </div>
    );
};

export default ExportOptions;