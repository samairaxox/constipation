import React from 'react';

const KPICard = ({ title, value, change, positive }) => {
    return (
        <div className="bg-white p-6 rounded-2xl shadow-sm border border-gray-100 hover:shadow-md transition-shadow duration-200">
            <div className="flex justify-between items-start mb-4">
                <h3 className="text-gray-500 font-medium text-xs uppercase tracking-wider">{title}</h3>
                <span className={`text-xs font-semibold px-2 py-1 rounded-full ${positive ? 'bg-green-50 text-green-600' : 'bg-red-50 text-red-600'}`}>
                    {change}
                </span>
            </div>
            <div className="text-3xl font-bold text-gray-900 tracking-tight">{value}</div>
        </div>
    );
};

export default KPICard;
