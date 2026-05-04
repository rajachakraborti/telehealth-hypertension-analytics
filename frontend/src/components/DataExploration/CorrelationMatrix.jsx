import React from 'react';
import { useEffect, useState } from 'react';
import { fetchCorrelationMatrix } from '../../services/api';
import { Table } from 'antd';

const CorrelationMatrix = ({ datasetId }) => {
    const [correlationData, setCorrelationData] = useState([]);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);

    useEffect(() => {
        if (!datasetId) return;

        const getCorrelationData = async () => {
            setLoading(true);
            setError(null);
            try {
                const data = await fetchCorrelationMatrix(datasetId);
                setCorrelationData(data || []);
            } catch (err) {
                console.error("Error fetching correlation data:", err);
                setError("Failed to load correlation data");
            } finally {
                setLoading(false);
            }
        };

        getCorrelationData();
    }, [datasetId]);

    const columns = correlationData.length > 0 ? Object.keys(correlationData[0]).map(key => ({
        title: key,
        dataIndex: key,
        key: key,
    })) : [];

    if (!datasetId) {
        return (
            <div>
                <h2>Correlation Matrix</h2>
                <p>Please select a dataset to view the correlation matrix.</p>
            </div>
        );
    }

    return (
        <div>
            <h2>Correlation Matrix</h2>
            {loading ? (
                <p>Loading...</p>
            ) : error ? (
                <p style={{ color: 'red' }}>{error}</p>
            ) : correlationData.length === 0 ? (
                <p>No correlation data available.</p>
            ) : (
                <Table
                    dataSource={correlationData}
                    columns={columns}
                    pagination={false}
                    rowKey={(record, index) => index}
                />
            )}
        </div>
    );
};

export default CorrelationMatrix;