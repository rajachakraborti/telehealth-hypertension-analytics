import React from 'react';
import { Table } from 'antd';

const DataTable = ({ data = [] }) => {
    if (!data || data.length === 0) {
        return (
            <div>
                <h2>Data Exploration Table</h2>
                <p>No data available</p>
            </div>
        );
    }

    const columns = Object.keys(data[0]).map(key => ({
        title: key.charAt(0).toUpperCase() + key.slice(1),
        dataIndex: key,
        key: key,
    }));

    return (
        <div>
            <h2>Data Exploration Table</h2>
            <Table
                dataSource={data}
                columns={columns}
                rowKey={(record, index) => record.id || index}
                pagination={{ pageSize: 10 }}
                scroll={{ x: true }}
            />
        </div>
    );
};

export default DataTable;