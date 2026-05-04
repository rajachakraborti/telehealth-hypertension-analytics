import React, { useState } from 'react';
import { Chart } from 'react-chartjs-2';

const ChartBuilder = ({ data }) => {
    const [chartType, setChartType] = useState('bar');
    const [selectedData, setSelectedData] = useState(null);

    const handleChartTypeChange = (event) => {
        setChartType(event.target.value);
    };

    const handleDataSelection = (event) => {
        const selected = data.find(item => item.label === event.target.value);
        setSelectedData(selected);
    };

    const chartData = {
        labels: selectedData ? selectedData.labels : [],
        datasets: [
            {
                label: selectedData ? selectedData.label : 'No Data',
                data: selectedData ? selectedData.values : [],
                backgroundColor: 'rgba(75,192,192,0.4)',
                borderColor: 'rgba(75,192,192,1)',
                borderWidth: 1,
            },
        ],
    };

    return (
        <div>
            <h2>Chart Builder</h2>
            <select onChange={handleChartTypeChange}>
                <option value="bar">Bar Chart</option>
                <option value="line">Line Chart</option>
                <option value="pie">Pie Chart</option>
            </select>
            <select onChange={handleDataSelection}>
                {data.map((item, index) => (
                    <option key={index} value={item.label}>{item.label}</option>
                ))}
            </select>
            <Chart type={chartType} data={chartData} />
        </div>
    );
};

export default ChartBuilder;