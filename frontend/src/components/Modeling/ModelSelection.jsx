import React, { useState, useEffect } from 'react';
import { fetchAvailableModels, fetchDataPreview, trainModel } from '../../services/api';

const ModelSelection = () => {
    const [models, setModels] = useState([]);
    const [selectedModel, setSelectedModel] = useState('');
    const [columns, setColumns] = useState([]);
    const [target, setTarget] = useState('');
    const [trainingStatus, setTrainingStatus] = useState(null);
    const [result, setResult] = useState(null);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);

    const datasetId = localStorage.getItem('dataset_id');

    useEffect(() => {
        fetchAvailableModels()
            .then((data) => setModels(data.models || []))
            .catch(() => setError('Failed to load model list.'));

        if (datasetId) {
            fetchDataPreview(datasetId)
                .then((data) => setColumns(data.columns || []))
                .catch(() => {});
        }
    }, []);

    const handleTrain = async () => {
        if (!datasetId) { setError('No dataset loaded. Please upload a file first.'); return; }
        if (!selectedModel) { setError('Please select a model.'); return; }
        if (!target) { setError('Please select a target column.'); return; }

        setLoading(true);
        setError(null);
        setResult(null);
        setTrainingStatus('Training in progress…');

        try {
            const data = await trainModel({ dataset_id: datasetId, model_type: selectedModel, target });
            setResult(data);
            setTrainingStatus('Training complete!');
        } catch (err) {
            setError(err.response?.data?.detail || 'Error training model.');
            setTrainingStatus(null);
        } finally {
            setLoading(false);
        }
    };

    return (
        <div style={s.wrap}>
            <h2>Model Training</h2>

            {!datasetId && <div style={s.warn}>No dataset loaded — please upload a file first.</div>}

            <div style={s.field}>
                <label style={s.label}>Select Model</label>
                <select style={s.select} value={selectedModel} onChange={(e) => setSelectedModel(e.target.value)}>
                    <option value="" disabled>-- choose a model --</option>
                    {models.map((m) => (
                        <option key={m.id} value={m.id}>{m.name}</option>
                    ))}
                </select>
            </div>

            <div style={s.field}>
                <label style={s.label}>Target Column</label>
                <select style={s.select} value={target} onChange={(e) => setTarget(e.target.value)} disabled={columns.length === 0}>
                    <option value="" disabled>-- choose target --</option>
                    {columns.map((col) => (
                        <option key={col} value={col}>{col}</option>
                    ))}
                </select>
            </div>

            <button
                onClick={handleTrain}
                disabled={loading || !datasetId || !selectedModel || !target}
                style={{
                    ...s.btn,
                    backgroundColor: loading || !datasetId || !selectedModel || !target ? '#d9d9d9' : '#1890ff',
                    cursor: loading || !datasetId || !selectedModel || !target ? 'not-allowed' : 'pointer',
                }}
            >
                {loading ? 'Training…' : 'Train Model'}
            </button>

            {trainingStatus && !error && <p style={s.status}>{trainingStatus}</p>}

            {error && <div style={s.errorBox}><p style={{ color: '#cf1322', margin: 0 }}>{error}</p></div>}

            {result && (
                <div style={s.resultBox}>
                    <h3 style={{ marginTop: 0 }}>Results</h3>
                    <div style={s.metrics}>
                        {Object.entries(result.metrics).map(([k, v]) => (
                            <div key={k} style={s.metric}>
                                <strong>{(v * 100).toFixed(1)}%</strong>
                                <span>{k.replace('_', ' ')}</span>
                            </div>
                        ))}
                    </div>
                    {result.feature_importance && Object.keys(result.feature_importance).length > 0 && (
                        <>
                            <h4>Feature Importance</h4>
                            {Object.entries(result.feature_importance)
                                .sort(([, a], [, b]) => b - a)
                                .map(([feat, imp]) => (
                                    <div key={feat} style={s.barRow}>
                                        <span style={s.barLabel}>{feat}</span>
                                        <div style={s.barTrack}>
                                            <div style={{ ...s.barFill, width: `${(imp * 100).toFixed(1)}%` }} />
                                        </div>
                                        <span style={s.barVal}>{(imp * 100).toFixed(1)}%</span>
                                    </div>
                                ))}
                        </>
                    )}
                </div>
            )}
        </div>
    );
};

const s = {
    wrap: { padding: '20px' },
    warn: { marginBottom: '16px', padding: '12px 16px', backgroundColor: '#fffbe6', border: '1px solid #ffe58f', borderRadius: '4px', color: '#ad6800' },
    field: { marginBottom: '16px' },
    label: { display: 'block', marginBottom: '6px', fontWeight: 600, fontSize: '14px' },
    select: { width: '100%', maxWidth: '360px', padding: '8px 12px', border: '1px solid #d9d9d9', borderRadius: '4px', fontSize: '14px' },
    btn: { padding: '10px 24px', color: 'white', border: 'none', borderRadius: '4px', fontSize: '15px' },
    status: { marginTop: '12px', color: '#52c41a' },
    errorBox: { marginTop: '16px', padding: '12px 16px', backgroundColor: '#fff2f0', border: '1px solid #ffccc7', borderRadius: '4px' },
    resultBox: { marginTop: '20px', padding: '20px', backgroundColor: '#f6ffed', border: '1px solid #b7eb8f', borderRadius: '8px' },
    metrics: { display: 'flex', gap: '24px', marginBottom: '16px', flexWrap: 'wrap' },
    metric: { display: 'flex', flexDirection: 'column', alignItems: 'center', gap: '2px', fontSize: '13px', color: '#555' },
    barRow: { display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '6px', fontSize: '13px' },
    barLabel: { width: '140px', textAlign: 'right', whiteSpace: 'nowrap', overflow: 'hidden', textOverflow: 'ellipsis' },
    barTrack: { flex: 1, height: '12px', backgroundColor: '#e8e8e8', borderRadius: '6px', overflow: 'hidden' },
    barFill: { height: '100%', backgroundColor: '#1890ff', borderRadius: '6px' },
    barVal: { width: '44px', textAlign: 'right' },
};

export default ModelSelection;
