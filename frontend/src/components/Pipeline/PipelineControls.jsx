import React, { useState, useEffect, useRef } from 'react';
import {
    startPipeline, stopPipeline, resetPipeline,
    advancePipeline, fetchPipelineStatus,
} from '../../services/api';

const STATUS_COLOR = {
    idle:    '#8c8c8c',
    running: '#1890ff',
    stopped: '#faad14',
};

const STAGE_NAMES = [
    'Data Ingestion', 'Data Exploration', 'Data Cleaning',
    'Modeling', 'Visualization', 'Reporting',
];

const PipelineControls = () => {
    const [status, setStatus] = useState(null);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);
    const pollRef = useRef(null);

    const loadStatus = async () => {
        try {
            const data = await fetchPipelineStatus();
            setStatus(data.status);
        } catch (e) {
            setError(e.response?.data?.detail || e.message);
        }
    };

    useEffect(() => {
        loadStatus();
        return () => clearInterval(pollRef.current);
    }, []);

    useEffect(() => {
        clearInterval(pollRef.current);
        if (status?.status === 'running') {
            pollRef.current = setInterval(loadStatus, 2000);
        }
        return () => clearInterval(pollRef.current);
    }, [status?.status]);

    const call = async (fn) => {
        setLoading(true);
        setError(null);
        try {
            const data = await fn();
            setStatus(data.status);
        } catch (e) {
            setError(e.response?.data?.detail || e.message);
        } finally {
            setLoading(false);
        }
    };

    const isRunning = status?.status === 'running';
    const isIdle    = !status || status.status === 'idle';
    const isDone    = isRunning && status.current_step >= status.total_steps;
    const progress  = status?.total_steps > 0
        ? Math.round((status.current_step / status.total_steps) * 100)
        : 0;

    return (
        <div style={s.wrap}>
            <h2>Pipeline Controls</h2>
            <p style={s.muted}>
                Run the full analytics pipeline step-by-step, or start and advance through each stage manually.
            </p>

            {/* Status badge */}
            <div style={s.statusRow}>
                <span style={s.badge(STATUS_COLOR[status?.status] || '#8c8c8c')}>
                    {status?.status ?? 'idle'}
                </span>
                {isRunning && (
                    <span style={s.stepLabel}>
                        Step {status.current_step} of {status.total_steps}
                        {status.current_step > 0 && status.current_step <= STAGE_NAMES.length &&
                            ` — ${STAGE_NAMES[status.current_step - 1]} complete`}
                    </span>
                )}
            </div>

            {/* Progress bar */}
            {isRunning && (
                <div style={s.trackWrap}>
                    <div style={s.track}>
                        <div style={{ ...s.fill, width: `${progress}%` }} />
                    </div>
                    <span style={s.pct}>{progress}%</span>
                </div>
            )}

            {/* Stage checklist */}
            {status && status.total_steps > 0 && (
                <div style={s.stages}>
                    {STAGE_NAMES.map((name, i) => {
                        const done    = i < status.current_step;
                        const current = i === status.current_step && isRunning;
                        return (
                            <div key={name} style={s.stageRow}>
                                <div style={s.dot(done, current)} />
                                <span style={{ color: done ? '#52c41a' : current ? '#1890ff' : '#999' }}>
                                    {name}
                                </span>
                            </div>
                        );
                    })}
                </div>
            )}

            {/* Buttons */}
            <div style={s.btnRow}>
                <button
                    style={s.btn('#52c41a')}
                    disabled={loading || isRunning}
                    onClick={() => call(startPipeline)}
                >
                    ▶ Start
                </button>
                <button
                    style={s.btn('#1890ff')}
                    disabled={loading || !isRunning || isDone}
                    onClick={() => call(advancePipeline)}
                >
                    ⏭ Advance Step
                </button>
                <button
                    style={s.btn('#faad14')}
                    disabled={loading || !isRunning}
                    onClick={() => call(stopPipeline)}
                >
                    ⏹ Stop
                </button>
                <button
                    style={s.btn('#8c8c8c')}
                    disabled={loading || isRunning}
                    onClick={() => call(resetPipeline)}
                >
                    ↺ Reset
                </button>
            </div>

            {isDone && (
                <div style={s.successBox}>
                    All pipeline stages complete. Proceed to Reporting to export your results.
                </div>
            )}

            {error && (
                <div style={s.errorBox}>
                    <p style={{ margin: 0, color: '#cf1322' }}>{error}</p>
                </div>
            )}
        </div>
    );
};

const s = {
    wrap:      { padding: '20px' },
    muted:     { color: '#666', marginBottom: '20px' },
    statusRow: { display: 'flex', alignItems: 'center', gap: '12px', marginBottom: '16px' },
    badge: (color) => ({
        padding: '3px 12px', borderRadius: '12px', fontSize: '13px',
        fontWeight: 600, color: '#fff', backgroundColor: color,
        textTransform: 'capitalize',
    }),
    stepLabel: { fontSize: '13px', color: '#555' },
    trackWrap: { display: 'flex', alignItems: 'center', gap: '10px', marginBottom: '20px' },
    track:     { flex: 1, height: '10px', backgroundColor: '#e8e8e8', borderRadius: '5px', overflow: 'hidden' },
    fill:      { height: '100%', backgroundColor: '#1890ff', borderRadius: '5px', transition: 'width 0.4s' },
    pct:       { fontSize: '13px', color: '#555', width: '36px', textAlign: 'right' },
    stages:    { display: 'flex', flexDirection: 'column', gap: '8px', marginBottom: '24px' },
    stageRow:  { display: 'flex', alignItems: 'center', gap: '10px', fontSize: '14px' },
    dot: (done, current) => ({
        width: '10px', height: '10px', borderRadius: '50%', flexShrink: 0,
        backgroundColor: done ? '#52c41a' : current ? '#1890ff' : '#d9d9d9',
    }),
    btnRow:    { display: 'flex', gap: '12px', flexWrap: 'wrap', marginBottom: '16px' },
    btn: (color) => ({
        padding: '9px 18px', backgroundColor: color, color: '#fff',
        border: 'none', borderRadius: '4px', fontSize: '14px',
        cursor: 'pointer', opacity: 1,
    }),
    successBox: {
        padding: '12px 16px', backgroundColor: '#f6ffed',
        border: '1px solid #b7eb8f', borderRadius: '4px',
        color: '#389e0d', fontSize: '14px',
    },
    errorBox: {
        padding: '12px 16px', backgroundColor: '#fff2f0',
        border: '1px solid #ffccc7', borderRadius: '4px',
    },
};

export default PipelineControls;
