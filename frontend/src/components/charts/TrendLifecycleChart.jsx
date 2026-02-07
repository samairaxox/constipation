import React from 'react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Legend } from 'recharts';

const data = [
    { name: 'Jan', value: 400, trend: 240 },
    { name: 'Feb', value: 300, trend: 139 },
    { name: 'Mar', value: 200, trend: 980 },
    { name: 'Apr', value: 278, trend: 390 },
    { name: 'May', value: 189, trend: 480 },
    { name: 'Jun', value: 239, trend: 380 },
    { name: 'Jul', value: 349, trend: 430 },
];

const TrendLifecycleChart = () => {
    return (
        <div className="bg-white rounded-xl shadow-md p-6 h-80">
            <h3 className="text-xl font-bold text-gray-800 mb-4">Trend Lifecycle Analysis</h3>
            <ResponsiveContainer width="100%" height="90%">
                <LineChart data={data}>
                    <CartesianGrid strokeDasharray="3 3" stroke="#e2e8f0" />
                    <XAxis dataKey="name" stroke="#64748b" fontSize={12} tickLine={false} axisLine={false} />
                    <YAxis stroke="#64748b" fontSize={12} tickLine={false} axisLine={false} />
                    <Tooltip
                        contentStyle={{ backgroundColor: '#fff', borderRadius: '8px', border: '1px solid #e2e8f0', boxShadow: '0 4px 6px -1px rgb(0 0 0 / 0.1)' }}
                    />
                    <Legend />
                    <Line type="monotone" dataKey="value" stroke="#6366f1" strokeWidth={3} dot={{ r: 4, strokeWidth: 2 }} activeDot={{ r: 6 }} name="Engagement" />
                    <Line type="monotone" dataKey="trend" stroke="#cbd5e1" strokeWidth={2} dot={false} name="Baseline" strokeDasharray="5 5" />
                </LineChart>
            </ResponsiveContainer>
        </div>
    );
};

export default TrendLifecycleChart;
