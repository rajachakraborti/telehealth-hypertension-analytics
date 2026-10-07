import React, { useEffect, useState } from 'react';
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
import { classifyAbpmRecord } from '../../services/api';

ChartJS.register(CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend);

const STAGE_COLORS = { Normal: '#2f855a', Elevated: '#b7791f', 'Stage 1': '#dd6b20', 'Stage 2': '#c53030' };
const card = { background: '#fff', border: '1px solid #e2e8f0', borderRadius: 8, padding: 16, marginBottom: 16 };

const ABPMClassifier = () => {
    const [samples, setSamples] = useState([]);
    const [recordText, setRecordText] = useState('');
    const [result, setResult] = useState(null);
    const [error, setError] = useState('');
    const [loading, setLoading] = useState(false);

    useEffect(() => {
        fetch('/sample_abpm_patients.json')
            .then((r) => (r.ok ? r.json() : []))
            .then(setSamples)
            .catch(() => setSamples([]));
    }, []);

    const loadSample = (sample) => {
        setRecordText(JSON.stringify(sample.record, null, 2));
        setResult(null);
        setError('');
    };

    const classify = async () => {
        setError('');
        setResult(null);
        let record;
        try {
            record = JSON.parse(recordText);
        } catch (e) {
            setError('The record is not valid JSON.');
            return;
        }
        setLoading(true);
        try {
            setResult(await classifyAbpmRecord(record));
        } catch (err) {
            const detail = err.response?.data?.detail;
            setError(typeof detail === 'string' ? detail : 'Classification failed. Check the record and that you are signed in as a clinician.');
        } finally {
            setLoading(false);
        }
    };

    const probData = result && {
        labels: Object.keys(result.probabilities),
        datasets: [{
            label: 'Probability',
            data: Object.values(result.probabilities),
            backgroundColor: Object.keys(result.probabilities).map((s) => STAGE_COLORS[s]),
        }],
    };
    const drivers = result ? result.explanation.top_drivers : [];
    const shapData = result && {
        labels: drivers.map((d) => `${d.label} (${d.value})`),
        datasets: [{
            label: `Contribution toward ${result.stage}`,
            data: drivers.map((d) => d.shap),
            backgroundColor: drivers.map((d) => (d.shap >= 0 ? '#c53030' : '#2b6cb0')),
        }],
    };
    const barOptions = (title, max) => ({
        indexAxis: 'y',
        plugins: { legend: { display: false }, title: { display: true, text: title } },
        scales: max ? { x: { min: 0, max } } : {},
    });

    return (
        <div style={{ padding: 20, maxWidth: 980 }}>
            <h2>ABPM Staging (24-hour record)</h2>
            <p style={{ color: '#4a5568' }}>
                Classifies one patient's 24-hour ambulatory record into an ACC/AHA stage and shows which
                measurements drove the result. Paste a record as JSON or load a sample.
            </p>

            <div style={card}>
                <div style={{ marginBottom: 8 }}>
                    {samples.map((s) => (
                        <button key={s.label} onClick={() => loadSample(s)} style={{ marginRight: 8 }}>
                            {s.label}
                        </button>
                    ))}
                </div>
                <textarea
                    aria-label="ABPM record JSON"
                    value={recordText}
                    onChange={(e) => setRecordText(e.target.value)}
                    rows={10}
                    style={{ width: '100%', fontFamily: 'monospace', fontSize: 12 }}
                    placeholder='{"age": 56, "bmi": 27.5, "readings": [{"hour": 0.0, "sbp": 108, "dbp": 66, "hr": 62, "awake": false}, ...]}'
                />
                <button onClick={classify} disabled={loading || !recordText.trim()} style={{ marginTop: 8 }}>
                    {loading ? 'Classifying...' : 'Classify record'}
                </button>
                {error && <p role="alert" style={{ color: '#c53030' }}>{error}</p>}
            </div>

            {result && (
                <>
                    <div style={card}>
                        <h3 style={{ marginTop: 0 }}>
                            Predicted stage:{' '}
                            <span style={{ color: STAGE_COLORS[result.stage] }}>{result.stage}</span>{' '}
                            <small style={{ color: '#4a5568' }}>({Math.round(result.confidence * 100)}% confidence)</small>
                        </h3>
                        {result.needs_manual_review && (
                            <p role="alert" style={{ background: '#fffaf0', border: '1px solid #dd6b20', padding: 8 }}>
                                Confidence is below {Math.round(result.review_threshold * 100)}%: manual clinician review recommended.
                            </p>
                        )}
                        <p>{result.explanation.narrative}</p>
                        {result.data_quality.warnings.map((w) => <p key={w} style={{ color: '#b7791f' }}>{w}</p>)}
                        <small style={{ color: '#4a5568' }}>
                            {result.data_quality.valid_readings} valid readings ({result.data_quality.day_readings} awake,{' '}
                            {result.data_quality.night_readings} asleep). Model {result.model.id} ({result.model.sha256}).
                            Inference {result.timing_ms.inference} ms, explanation {result.timing_ms.explanation} ms.
                        </small>
                    </div>

                    <div style={{ display: 'flex', gap: 16, flexWrap: 'wrap' }}>
                        <div style={{ ...card, flex: '1 1 380px' }}>
                            <Bar data={probData} options={barOptions('Stage probabilities', 1)} />
                        </div>
                        <div style={{ ...card, flex: '1 1 380px' }}>
                            <Bar data={shapData} options={barOptions(`Top drivers (TreeSHAP, toward ${result.stage})`)} />
                            <small style={{ color: '#4a5568' }}>Red raises the predicted-stage score; blue lowers it.</small>
                        </div>
                    </div>

                    <p style={{ color: '#718096', fontSize: 12 }}>{result.disclaimer}</p>
                </>
            )}
        </div>
    );
};

export default ABPMClassifier;
