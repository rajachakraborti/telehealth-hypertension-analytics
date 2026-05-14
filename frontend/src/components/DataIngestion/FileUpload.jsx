import React, { useState } from 'react';
import { uploadFile } from '../../services/api';

const FileUpload = () => {
    const [file, setFile] = useState(null);
    const [error, setError] = useState('');
    const [success, setSuccess] = useState('');
    const [loading, setLoading] = useState(false);
    const [uploadResult, setUploadResult] = useState(null);

    const handleFileChange = (event) => {
        setFile(event.target.files[0]);
        setError('');
        setSuccess('');
        setUploadResult(null);
    };

    const handleSubmit = async (event) => {
        event.preventDefault();
        if (!file) {
            setError('Please select a file to upload.');
            return;
        }

        setLoading(true);
        setError('');
        setSuccess('');

        try {
            const response = await uploadFile(file);
            setSuccess('File uploaded successfully!');
            setUploadResult(response);
            if (response.dataset_id) {
                localStorage.setItem('dataset_id', response.dataset_id);
            }
            setFile(null);
            // Reset file input
            event.target.reset();
        } catch (err) {
            setError(err.response?.data?.detail || 'Error uploading file. Please try again.');
        } finally {
            setLoading(false);
        }
    };

    return (
        <div style={{ padding: '20px' }}>
            <h2>Upload Data File</h2>
            <p style={{ marginBottom: '20px', color: '#666' }}>
                Upload CSV, Excel, or JSON files containing your hypertension data for analysis.
            </p>

            <form onSubmit={handleSubmit}>
                <div style={{
                    border: '2px dashed #d9d9d9',
                    borderRadius: '8px',
                    padding: '40px',
                    textAlign: 'center',
                    marginBottom: '20px',
                    backgroundColor: '#fafafa'
                }}>
                    <input
                        type="file"
                        onChange={handleFileChange}
                        accept=".csv,.xlsx,.xls,.json"
                        style={{ marginBottom: '10px' }}
                    />
                    <p style={{ color: '#999', fontSize: '14px' }}>
                        Supported formats: CSV, Excel (.xlsx, .xls), JSON
                    </p>
                </div>

                <button
                    type="submit"
                    disabled={loading || !file}
                    style={{
                        padding: '12px 24px',
                        backgroundColor: loading || !file ? '#d9d9d9' : '#1890ff',
                        color: 'white',
                        border: 'none',
                        borderRadius: '4px',
                        fontSize: '16px',
                        cursor: loading || !file ? 'not-allowed' : 'pointer'
                    }}
                >
                    {loading ? 'Uploading...' : 'Upload File'}
                </button>
            </form>

            {error && (
                <div style={{ marginTop: '20px', padding: '15px', backgroundColor: '#fff2f0', border: '1px solid #ffccc7', borderRadius: '4px' }}>
                    <p style={{ color: '#cf1322', margin: 0 }}>{error}</p>
                </div>
            )}

            {success && (
                <div style={{ marginTop: '20px', padding: '15px', backgroundColor: '#f6ffed', border: '1px solid #b7eb8f', borderRadius: '4px' }}>
                    <p style={{ color: '#52c41a', margin: 0 }}>{success}</p>
                </div>
            )}

            {uploadResult && (
                <div style={{ marginTop: '20px', padding: '20px', backgroundColor: 'white', borderRadius: '8px', boxShadow: '0 2px 8px rgba(0,0,0,0.1)' }}>
                    <h3>Upload Summary</h3>
                    <p><strong>Filename:</strong> {uploadResult.filename}</p>
                    <p><strong>Rows:</strong> {uploadResult.rows}</p>
                    <p><strong>Columns:</strong> {uploadResult.columns?.join(', ')}</p>
                </div>
            )}
        </div>
    );
};

export default FileUpload;