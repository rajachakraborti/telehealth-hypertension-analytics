import React, { useEffect, useState } from 'react';
import GaugeChart from 'react-gauge-chart';
import { fetchDashboard } from '../../services/api';

const RISK_LEVELS = [
    { max: 25,  label: 'Low Risk',     color: '#52c41a' },
    { max: 50,  label: 'Moderate Risk',color: '#faad14' },
    { max: 75,  label: 'High Risk',    color: '#fa8c16' },
    { max: 100, label: 'Critical Risk',color: '#cf1322' },
];

const getRiskLevel = (score) =>
    RISK_LEVELS.find((r) => score <= r.max) || RISK_LEVELS[RISK_LEVELS.length - 1];

const RiskGauge = ({ riskScore: propScore }) => {
    const [riskScore, setRiskScore] = useState(propScore ?? 0);
    const [stats, setStats] = useState(null);
    const [loading, setLoading] = useState(false);

    const datasetId = localStorage.getItem('dataset_id');

    useEffect(() => {
        if (propScore !== undefined) return;
        if (!datasetId) return;
        setLoading(true);
        fetchDashboard(datasetId)
            .then((d) => {
                setRiskScore(d.risk_score ?? 0);
                setStats(d);
            })
            .catch(() => {})
            .finally(() => setLoading(false));
    }, []);

    useEffect(() => {
        if (propScore !== undefined) setRiskScore(propScore);
    }, [propScore]);

    const level = getRiskLevel(riskScore);

    return (
        <div style={s.wrap}>
            <h2>Risk Score</h2>

            {!datasetId && !propScore && (
                <div style={s.warn}>No dataset loaded — please upload a file first.</div>
            )}

            {loading && <p style={s.muted}>Loading…</p>}

            <GaugeChart
                id="risk-gauge"
                nrOfLevels={20}
                percent={riskScore / 100}
                textColor="#333"
                needleColor="#555"
                needleBaseColor="#555"
                arcPadding={0.02}
                colors={['#52c41a', '#faad14', '#fa8c16', '#cf1322']}
                formatTextValue={() => `${riskScore}%`}
            />

            <div style={s.levelBadge(level.color)}>
                {level.label}
            </div>

            {stats && (
                <div style={s.statGrid}>
                    <div style={s.stat}><strong>{stats.total_patients}</strong><span>Patients</span></div>
                    {Object.entries(stats.stats || {}).map(([k, v]) => (
                        <div key={k} style={s.stat}>
                            <strong>{v}</strong>
                            <span>{k.replace(/_/g, ' ')}</span>
                        </div>
                    ))}
                </div>
            )}
        </div>
    );
};

const s = {
    wrap: { padding: '20px', maxWidth: '520px' },
    muted: { color: '#999' },
    warn: { marginBottom: '16px', padding: '12px 16px', backgroundColor: '#fffbe6', border: '1px solid #ffe58f', borderRadius: '4px', color: '#ad6800' },
    levelBadge: (color) => ({
        textAlign: 'center',
        marginTop: '8px',
        fontWeight: 700,
        fontSize: '18px',
        color,
    }),
    statGrid: {
        display: 'flex', flexWrap: 'wrap', gap: '16px',
        marginTop: '24px', padding: '16px',
        backgroundColor: '#fafafa', borderRadius: '8px',
    },
    stat: {
        display: 'flex', flexDirection: 'column', alignItems: 'center',
        gap: '2px', fontSize: '13px', color: '#555', minWidth: '80px',
    },
};

export default RiskGauge;
