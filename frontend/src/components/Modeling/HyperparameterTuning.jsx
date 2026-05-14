import React, { useState, useEffect } from 'react';
import { fetchHyperparameterOptions, fetchDataPreview, tuneHyperparameters } from '../../services/api';

const parseParamValue = (raw) => {
    return raw.split(',').map((v) => {
        v = v.trim();
        if (v === 'null') return null;
        const n = Number(v);
        return isNaN(n) ? v : n;
    });
};

const HyperparameterTuning = () => {
    const [modelType, setModelType] = useState('');
    const [paramInputs, setParamInputs] = useState({});
    const [columns, setColumns] = useState([]);
    const [target, setTarget] = useState('');
    const [result, setResult] = useState(null);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);

    const datasetId = localStorage.getItem('dataset_id');

    useEffect(() => {
        if (datasetId) {
            fetchDataPreview(datasetId)
                .then((d) => setColumns(d.columns || []))
                .catch(() => {});
        }
    }, []);

    useEffect(() => {
        if (!modelType) return;
        fetchHyperparameterOptions(modelType).then((opts) => {
            const inputs = {};
            Object.entries(opts).forEach(([k, v]) => {
                inputs[k] = Array.isArray(v) ? v.map(String).join(', ') : String(v);
            });
            setParamInputs(inputs);
        });
    }, [modelType]);

    const handleTune = async () => {
        if (!datasetId) { setError('No dataset loaded. Please upload a file first.'); return; }
        if (!modelType)  { setError('Please select a model.'); return; }
        if (!target)     { setError('Please select a target column.'); return; }

        const param_grid = {};
        for (const [k, v] of Object.entries(paramInputs)) {
            param_grid[k] = parseParamValue(v);
        }

        setLoading(true);
        setError(null);
        setResult(null);
        try {
            const data = await tuneHyperparameters({ dataset_id: datasetId, model_type: modelType, target, param_grid });
            setResult(data);
        } catch (err) {
            setError(err.response?.data?.detail || err.message || 'Tuning failed.');
        } finally {
            setLoading(false);
        }
    };

    return (
        <div style={s.wrap}>
            <h2>Hyperparameter Tuning</h2>
            <p style={s.muted}>Grid search over a parameter grid to find the best hyperparameters.</p>

            {!datasetId && <div style={s.warn}>No dataset loaded — please upload a file first.</div>}

            <div style={s.field}>
                <label style={s.label}>Select Model</label>
                <select style={s.select} value={modelType} onChange={(e) => setModelType(e.target.value)}>
                    <option value="">-- choose a model --</option>
                    <option value="logistic_regression">Logistic Regression</option>
                    <option value="random_forest">Random Forest</option>
                    <option value="gradient_boosting">Gradient Boosting</option>
                    <option value="xgboost">XGBoost</option>
                </select>
            </div>

            <div style={s.field}>
                <label style={s.label}>Target Column</label>
                <select style={s.select} value={target} onChange={(e) => setTarget(e.target.value)} disabled={columns.length === 0}>
                    <option value="">-- choose target --</option>
                    {columns.map((c) => <option key={c} value={c}>{c}</option>)}
                </select>
            </div>

            {modelType && Object.keys(paramInputs).length > 0 && (
                <div style={s.field}>
                    <label style={s.label}>Hyperparameters <span style={s.hint}>(comma-separated values for grid search)</span></label>
                    {Object.entries(paramInputs).map(([param, val]) => (
                        <div key={param} style={s.paramRow}>
                            <span style={s.paramName}>{param}</span>
                            <input
                                style={s.input}
                                type="text"
                                value={val}
                                onChange={(e) => setParamInputs({ ...paramInputs, [param]: e.target.value })}
                            />
                        </div>
                    ))}
                </div>
            )}

            <button
                onClick={handleTune}
                disabled={loading || !datasetId || !modelType || !target}
                style={{
                    ...s.btn,
                    backgroundColor: loading || !datasetId || !modelType || !target ? '#d9d9d9' : '#722ed1',
                    cursor: loading || !datasetId || !modelType || !target ? 'not-allowed' : 'pointer',
                }}
            >
                {loading ? 'Tuning…' : 'Tune Hyperparameters'}
            </button>

            {error && <div style={s.errorBox}><p style={{ color: '#cf1322', margin: 0 }}>{error}</p></div>}

            {result && (
                <div style={s.resultBox}>
                    <h3 style={{ marginTop: 0 }}>Best Parameters</h3>
                    <div style={s.paramTable}>
                        {Object.entries(result.best_params).map(([k, v]) => (
                            <div key={k} style={s.paramResult}>
                                <span style={s.paramKey}>{k}</span>
                                <span style={s.paramVal}>{String(v)}</span>
                            </div>
                        ))}
                    </div>

                    <h3>Metrics</h3>
                    <div style={s.metrics}>
                        {Object.entries(result.metrics).map(([k, v]) => (
                            <div key={k} style={s.metric}>
                                <strong>{k === 'best_cv_score' ? (v * 100).toFixed(1) + '%' : (v * 100).toFixed(1) + '%'}</strong>
                                <span>{k.replace(/_/g, ' ')}</span>
                            </div>
                        ))}
                    </div>
                </div>
            )}
        </div>
    );
};

const s = {
    wrap: { padding: '20px' },
    muted: { color: '#666', marginBottom: '20px' },
    warn: { marginBottom: '16px', padding: '12px 16px', backgroundColor: '#fffbe6', border: '1px solid #ffe58f', borderRadius: '4px', color: '#ad6800' },
    field: { marginBottom: '20px' },
    label: { display: 'block', marginBottom: '6px', fontWeight: 600, fontSize: '14px' },
    hint: { fontWeight: 400, color: '#999', fontSize: '12px' },
    select: { width: '100%', maxWidth: '360px', padding: '8px 12px', border: '1px solid #d9d9d9', borderRadius: '4px', fontSize: '14px' },
    paramRow: { display: 'flex', alignItems: 'center', gap: '12px', marginBottom: '8px' },
    paramName: { width: '120px', textAlign: 'right', fontSize: '14px', color: '#555' },
    input: { flex: 1, maxWidth: '300px', padding: '6px 10px', border: '1px solid #d9d9d9', borderRadius: '4px', fontSize: '14px' },
    btn: { padding: '10px 24px', color: 'white', border: 'none', borderRadius: '4px', fontSize: '15px' },
    errorBox: { marginTop: '16px', padding: '12px 16px', backgroundColor: '#fff2f0', border: '1px solid #ffccc7', borderRadius: '4px' },
    resultBox: { marginTop: '24px', padding: '20px', backgroundColor: '#f9f0ff', border: '1px solid #d3adf7', borderRadius: '8px' },
    paramTable: { display: 'flex', flexDirection: 'column', gap: '6px', marginBottom: '16px' },
    paramResult: { display: 'flex', gap: '12px', fontSize: '14px' },
    paramKey: { fontWeight: 600, width: '120px' },
    paramVal: { color: '#722ed1', fontWeight: 600 },
    metrics: { display: 'flex', gap: '24px', flexWrap: 'wrap' },
    metric: { display: 'flex', flexDirection: 'column', alignItems: 'center', gap: '2px', fontSize: '13px', color: '#555' },
};

export default HyperparameterTuning;
