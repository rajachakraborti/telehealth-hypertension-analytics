import React, { useEffect, useState } from 'react';
import { Card, CardHeader, CardContent, Grid } from '@mui/material';
import RiskGauge from './RiskGauge';
import { fetchDashboard } from '../../services/api';

const STAT_LABELS = {
    age:          { label: 'Avg Age',         unit: 'yrs' },
    systolic_bp:  { label: 'Avg Systolic BP', unit: 'mmHg' },
    diastolic_bp: { label: 'Avg Diastolic BP',unit: 'mmHg' },
    bmi:          { label: 'Avg BMI',          unit: '' },
    cholesterol:  { label: 'Avg Cholesterol',  unit: 'mg/dL' },
};

const Dashboard = () => {
    const [dashData, setDashData] = useState(null);
    const datasetId = localStorage.getItem('dataset_id');

    useEffect(() => {
        if (!datasetId) return;
        fetchDashboard(datasetId)
            .then(setDashData)
            .catch(() => {});
    }, []);

    const riskScore = dashData?.risk_score ?? 0;

    return (
        <Grid container spacing={3}>
            <Grid item xs={12}>
                <Card>
                    <CardHeader title="Welcome to Telehealth Hypertension Analytics" />
                    <CardContent>
                        <p>Use the sidebar to navigate through different features:</p>
                        <ul>
                            <li><strong>Data Ingestion</strong> - Upload or import your data</li>
                            <li><strong>Data Exploration</strong> - View statistics and correlations</li>
                            <li><strong>Data Cleaning</strong> - Handle missing values and outliers</li>
                            <li><strong>Modeling</strong> - Train and tune predictive models</li>
                            <li><strong>Visualization</strong> - Create charts and dashboards</li>
                            <li><strong>Reporting</strong> - Generate and export reports</li>
                        </ul>
                    </CardContent>
                </Card>
            </Grid>

            <Grid item xs={12} md={6}>
                <Card>
                    <CardHeader title="Risk Assessment" />
                    <CardContent>
                        <RiskGauge riskScore={riskScore} />
                        <p style={{ textAlign: 'center', marginTop: '10px', color: '#666' }}>
                            {dashData
                                ? `Based on ${dashData.total_patients} patient records`
                                : 'Upload data to see risk assessment'}
                        </p>
                    </CardContent>
                </Card>
            </Grid>

            <Grid item xs={12} md={6}>
                <Card>
                    <CardHeader title="Quick Stats" />
                    <CardContent>
                        {!dashData ? (
                            <p style={{ color: '#999' }}>No data loaded yet. Upload a dataset to get started.</p>
                        ) : (
                            <div>
                                <div style={s.statRow}>
                                    <span style={s.statLabel}>Total Patients</span>
                                    <span style={s.statValue}>{dashData.total_patients}</span>
                                </div>
                                <div style={s.statRow}>
                                    <span style={s.statLabel}>Hypertension Risk</span>
                                    <span style={{ ...s.statValue, color: riskScore > 50 ? '#cf1322' : '#52c41a' }}>
                                        {riskScore}%
                                    </span>
                                </div>
                                {Object.entries(dashData.stats || {}).map(([key, val]) => {
                                    const meta = STAT_LABELS[key] || { label: key, unit: '' };
                                    return (
                                        <div key={key} style={s.statRow}>
                                            <span style={s.statLabel}>{meta.label}</span>
                                            <span style={s.statValue}>{val} {meta.unit}</span>
                                        </div>
                                    );
                                })}
                            </div>
                        )}
                    </CardContent>
                </Card>
            </Grid>
        </Grid>
    );
};

const s = {
    statRow: {
        display: 'flex',
        justifyContent: 'space-between',
        alignItems: 'center',
        padding: '8px 0',
        borderBottom: '1px solid #f0f0f0',
    },
    statLabel: { color: '#666', fontSize: '14px' },
    statValue: { fontWeight: 600, fontSize: '15px' },
};

export default Dashboard;
