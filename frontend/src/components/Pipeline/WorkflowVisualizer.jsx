import React, { useEffect, useState } from 'react';
import { fetchWorkflowData } from '../../services/api';

const STAGE_ROUTES = {
    ingestion:    '/data-ingestion/file-upload',
    exploration:  '/data-exploration/summary-statistics',
    cleaning:     '/data-cleaning/imputation',
    modeling:     '/modeling/model-selection',
    visualization:'/visualization/chart-builder',
    reporting:    '/reporting/report-generator',
};

// Derive completed stages from localStorage
const getCompletedStages = () => {
    const completed = new Set();
    if (localStorage.getItem('dataset_id')) {
        completed.add('ingestion');
        completed.add('exploration');
    }
    return completed;
};

const WorkflowVisualizer = () => {
    const [stages, setStages] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const completed = getCompletedStages();

    useEffect(() => {
        fetchWorkflowData()
            .then((d) => setStages(d.stages || []))
            .catch((err) => setError(err.response?.data?.detail || err.message))
            .finally(() => setLoading(false));
    }, []);

    if (loading) return <div style={{ padding: '20px' }}>Loading workflow…</div>;
    if (error)   return <div style={{ padding: '20px', color: '#cf1322' }}>Error: {error}</div>;

    return (
        <div style={s.wrap}>
            <h2>Pipeline Workflow</h2>
            <p style={s.muted}>The analytics pipeline runs through these stages in order.</p>

            <div style={s.pipeline}>
                {stages.map((stage, idx) => {
                    const done = completed.has(stage.id);
                    const isLast = idx === stages.length - 1;
                    return (
                        <React.Fragment key={stage.id}>
                            <div style={s.stageCol}>
                                <div style={s.circle(done)}>
                                    {done ? '✓' : idx + 1}
                                </div>
                                <div style={s.card(done)}>
                                    <div style={s.stageName(done)}>{stage.name}</div>
                                    <div style={s.stageDesc}>{stage.description}</div>
                                    <a href={STAGE_ROUTES[stage.id]} style={s.link}>
                                        Go →
                                    </a>
                                </div>
                            </div>
                            {!isLast && <div style={s.arrow}>▶</div>}
                        </React.Fragment>
                    );
                })}
            </div>

            <div style={s.legend}>
                <span style={s.legendDone}>■ Completed</span>
                <span style={s.legendPending}>■ Pending</span>
            </div>
        </div>
    );
};

const s = {
    wrap: { padding: '20px' },
    muted: { color: '#666', marginBottom: '24px' },
    pipeline: {
        display: 'flex',
        alignItems: 'flex-start',
        flexWrap: 'wrap',
        gap: '8px',
    },
    stageCol: {
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        gap: '8px',
        width: '140px',
    },
    circle: (done) => ({
        width: '36px',
        height: '36px',
        borderRadius: '50%',
        backgroundColor: done ? '#52c41a' : '#d9d9d9',
        color: done ? '#fff' : '#666',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        fontWeight: 700,
        fontSize: '14px',
        flexShrink: 0,
    }),
    card: (done) => ({
        padding: '12px',
        border: `1px solid ${done ? '#b7eb8f' : '#e8e8e8'}`,
        borderRadius: '8px',
        backgroundColor: done ? '#f6ffed' : '#fafafa',
        width: '100%',
        boxSizing: 'border-box',
    }),
    stageName: (done) => ({
        fontWeight: 600,
        fontSize: '13px',
        color: done ? '#389e0d' : '#333',
        marginBottom: '4px',
    }),
    stageDesc: {
        fontSize: '11px',
        color: '#888',
        lineHeight: '1.4',
        marginBottom: '8px',
    },
    link: {
        fontSize: '12px',
        color: '#1890ff',
        textDecoration: 'none',
    },
    arrow: {
        color: '#bbb',
        fontSize: '18px',
        marginTop: '10px',
        flexShrink: 0,
    },
    legend: { display: 'flex', gap: '16px', marginTop: '24px', fontSize: '13px' },
    legendDone:    { color: '#52c41a' },
    legendPending: { color: '#d9d9d9' },
};

export default WorkflowVisualizer;
