import React from 'react';
import { Radar, RadarChart, PolarGrid, PolarAngleAxis, PolarRadiusAxis, ResponsiveContainer, Tooltip } from 'recharts';

const data = [
    { subject: 'Engagement', A: 120, fullMark: 150 },
    { subject: 'Saturation', A: 98, fullMark: 150 },
    { subject: 'Sentiment', A: 86, fullMark: 150 },
    { subject: 'Velocity', A: 99, fullMark: 150 },
    { subject: 'Reach', A: 85, fullMark: 150 },
    { subject: 'Innovation', A: 65, fullMark: 150 },
];

const DeclineRadarMeter = () => {
    return (
        <div className="bg-white rounded-xl shadow-md p-6 h-80">
            <h3 className="text-xl font-bold text-gray-800 mb-4">Decline Radar Meter</h3>
            <div className="h-full w-full flex items-center justify-center -mt-4">
                <ResponsiveContainer width="100%" height="100%">
                    <RadarChart cx="50%" cy="50%" outerRadius="80%" data={data}>
                        <PolarGrid stroke="#e2e8f0" />
                        <PolarAngleAxis dataKey="subject" tick={{ fill: '#64748b', fontSize: 12 }} />
                        <PolarRadiusAxis angle={30} domain={[0, 150]} tick={false} axisLine={false} />
                        <Radar name="Trend Health" dataKey="A" stroke="#8b5cf6" fill="#8b5cf6" fillOpacity={0.5} />
                        <Tooltip />
                    </RadarChart>
                </ResponsiveContainer>
            </div>
        </div>
    );
};

export default DeclineRadarMeter;
