import React, { useState, useEffect } from 'react';
import {
    Chart as ChartJS,
    CategoryScale,
    LinearScale,
    BarElement,
    Title,
    Tooltip,
    Legend,
} from 'chart.js';
import { Bar } from 'react-chartjs-2';

// Register Chart.js components
ChartJS.register(
    CategoryScale,
    LinearScale,
    BarElement,
    Title,
    Tooltip,
    Legend
);

const FeatureImportance = () => {
    const [featureData, setFeatureData] = useState([]);
    const [loading, setLoading] = useState(false);

    useEffect(() => {
        // Sample data for demonstration
        const sampleData = [
            { feature: 'Age', importance: 0.25 },
            { feature: 'Systolic BP', importance: 0.35 },
            { feature: 'Diastolic BP', importance: 0.28 },
            { feature: 'BMI', importance: 0.18 },
            { feature: 'Heart Rate', importance: 0.15 },
            { feature: 'Cholesterol', importance: 0.12 },
            { feature: 'Smoking Status', importance: 0.10 },
            { feature: 'Physical Activity', importance: 0.08 },
        ];
        setFeatureData(sampleData);
    }, []);

    if (loading) {
        return <div style={{ padding: '20px' }}>Loading feature importance...</div>;
    }

    if (featureData.length === 0) {
        return (
            <div style={{ padding: '20px' }}>
                <h2>Feature Importance</h2>
                <p style={{ color: '#666' }}>
                    Train a model first to view feature importance scores.
                </p>
            </div>
        );
    }

    const data = {
        labels: featureData.map(item => item.feature),
        datasets: [
            {
                label: 'Feature Importance',
                data: featureData.map(item => item.importance),
                backgroundColor: 'rgba(24, 144, 255, 0.6)',
                borderColor: 'rgba(24, 144, 255, 1)',
                borderWidth: 1,
            },
        ],
    };

    const options = {
        indexAxis: 'y',
        responsive: true,
        maintainAspectRatio: false,
        scales: {
            x: {
                beginAtZero: true,
                max: 1,
                title: {
                    display: true,
                    text: 'Importance Score',
                },
            },
            y: {
                title: {
                    display: true,
                    text: 'Features',
                },
            },
        },
        plugins: {
            legend: {
                display: true,
                position: 'top',
            },
            title: {
                display: true,
                text: 'Feature Importance Analysis',
            },
        },
    };

    return (
        <div style={{ padding: '20px' }}>
            <h2>Feature Importance</h2>
            <p style={{ marginBottom: '20px', color: '#666' }}>
                Shows the relative importance of each feature in the trained model's predictions.
            </p>
            <div style={{ height: '400px', backgroundColor: 'white', padding: '20px', borderRadius: '8px', boxShadow: '0 2px 8px rgba(0,0,0,0.1)' }}>
                <Bar data={data} options={options} />
            </div>
        </div>
    );
};

export default FeatureImportance;