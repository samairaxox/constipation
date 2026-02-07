import React from 'react';
import { AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';

const data = [
    { name: 'Week 1', saturation: 20 },
    { name: 'Week 2', saturation: 35 },
    { name: 'Week 3', saturation: 50 },
    { name: 'Week 4', saturation: 65 },
    { name: 'Week 5', saturation: 80 },
    { name: 'Week 6', saturation: 95 },
    { name: 'Week 7', saturation: 98 },
];

const SaturationLayer = () => {
    return (
        <div className="bg-white rounded-xl shadow-md p-6 h-80">
            <h3 className="text-xl font-bold text-gray-800 mb-4">Saturation Layer</h3>
            <ResponsiveContainer width="100%" height="90%">
                <AreaChart data={data}
                    margin={{ top: 10, right: 30, left: 0, bottom: 0 }}>
                    <defs>
                        <linearGradient id="colorSaturation" x1="0" y1="0" x2="0" y2="1">
                            <stop offset="5%" stopColor="#f59e0b" stopOpacity={0.8} />
                            <stop offset="95%" stopColor="#f59e0b" stopOpacity={0} />
                        </linearGradient>
                    </defs>
                    <CartesianGrid strokeDasharray="3 3" stroke="#e2e8f0" vertical={false} />
                    <XAxis dataKey="name" stroke="#64748b" fontSize={12} tickLine={false} axisLine={false} />
                    <YAxis stroke="#64748b" fontSize={12} tickLine={false} axisLine={false} />
                    <Tooltip
                        contentStyle={{ backgroundColor: '#fff', borderRadius: '8px', border: '1px solid #e2e8f0' }}
                    />
                    <Area type="monotone" dataKey="saturation" stroke="#f59e0b" fillOpacity={1} fill="url(#colorSaturation)" />
                </AreaChart>
            </ResponsiveContainer>
        </div>
    );
};

export default SaturationLayer;
