import React from 'react';

const WhatIfSimulator = () => {
    return (
        <div className="space-y-6">
            <h1 className="text-2xl font-bold text-slate-800">What-If Simulator</h1>
            <p className="text-slate-600">Adjust parameters to simulate trend decline scenarios.</p>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                <div className="md:col-span-1 bg-white p-6 rounded-xl shadow-sm border border-slate-200 space-y-6">
                    <div>
                        <label className="block text-sm font-medium text-slate-700 mb-2">Campaign Budget Impact</label>
                        <input type="range" className="w-full accent-indigo-600" />
                        <div className="flex justify-between text-xs text-slate-500 mt-1">
                            <span>Low</span>
                            <span>High</span>
                        </div>
                    </div>
                    <div>
                        <label className="block text-sm font-medium text-slate-700 mb-2">Sentiment Shift</label>
                        <input type="range" className="w-full accent-indigo-600" />
                    </div>
                </div>

                <div className="md:col-span-2 bg-white p-6 rounded-xl shadow-sm border border-slate-200 h-96 flex items-center justify-center text-slate-400 bg-slate-50">
                    Simulation Results Visualization
                </div>
            </div>
        </div>
    );
};

export default WhatIfSimulator;
