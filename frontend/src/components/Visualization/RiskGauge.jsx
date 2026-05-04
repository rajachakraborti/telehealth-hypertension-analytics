import React from 'react';
import GaugeChart from 'react-gauge-chart';

const RiskGauge = ({ riskScore = 0 }) => {
    const gaugeValue = riskScore / 100; // Normalize risk score to a value between 0 and 1

    return (
        <div className="risk-gauge">
            <h2>Risk Score</h2>
            <GaugeChart
                id="risk-gauge"
                nrOfLevels={5}
                percent={gaugeValue}
                textColor="#000"
                needleColor="#FF0000"
                arcPadding={0.02}
                colors={['#00FF00', '#7FFF00', '#FFFF00', '#FF7F00', '#FF0000']}
            />
            <p>{riskScore}%</p>
        </div>
    );
};

export default RiskGauge;