import React, { useState } from 'react';
import axios from 'axios';

const URLImport = () => {
    const [url, setUrl] = useState('');
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);
    const [success, setSuccess] = useState(null);

    const handleUrlChange = (e) => {
        setUrl(e.target.value);
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        setLoading(true);
        setError(null);
        setSuccess(null);

        try {
            const response = await axios.post('/api/data-ingestion/url', { url });
            setSuccess('Data ingested successfully!');
        } catch (err) {
            setError('Failed to ingest data. Please check the URL and try again.');
        } finally {
            setLoading(false);
        }
    };

    return (
        <div>
            <h2>Import Data from URL</h2>
            <form onSubmit={handleSubmit}>
                <input
                    type="text"
                    value={url}
                    onChange={handleUrlChange}
                    placeholder="Enter data URL"
                    required
                />
                <button type="submit" disabled={loading}>
                    {loading ? 'Ingesting...' : 'Ingest Data'}
                </button>
            </form>
            {error && <p style={{ color: 'red' }}>{error}</p>}
            {success && <p style={{ color: 'green' }}>{success}</p>}
        </div>
    );
};

export default URLImport;