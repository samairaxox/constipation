import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { ArrowRight, Activity, TrendingDown, AlertTriangle, TrendingUp, Users } from 'lucide-react';
import { getTrends } from '../api/trends';
import TrendLifecycleChart from '../components/charts/TrendLifecycleChart';
import DeclineRadarMeter from '../components/charts/DeclineRadarMeter';
import SaturationLayer from '../components/charts/SaturationLayer';
import KPICard from '../components/KPICard';

const getStageBadge = (stage) => {
    const styles = {
        'Growth': 'bg-green-50 text-green-700 ring-1 ring-green-600/20',
        'Peak': 'bg-blue-50 text-blue-700 ring-1 ring-blue-600/20',
        'Early Decline': 'bg-yellow-50 text-yellow-700 ring-1 ring-yellow-600/20',
        'Collapse': 'bg-orange-50 text-orange-700 ring-1 ring-orange-600/20',
        'Dead': 'bg-red-50 text-red-700 ring-1 ring-red-600/20',
    };
    return (
        <span className={`px-2.5 py-0.5 rounded-full text-xs font-semibold ${styles[stage] || 'bg-slate-100 text-slate-700 ring-1 ring-slate-600/20'}`}>
            {stage}
        </span>
    );
};

const Home = () => {
    const navigate = useNavigate();
    const [trends, setTrends] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        const fetchTrends = async () => {
            try {
                const data = await getTrends();
                setTrends(data);
                setLoading(false);
            } catch (err) {
                console.error("Failed to fetch trends:", err);
                setError("Failed to load trend data. Please check API connection.");
                setLoading(false);
            }
        };
        fetchTrends();
    }, []);

    if (loading) {
        return (
            <div className="flex justify-center items-center h-64">
                <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-indigo-600"></div>
            </div>
        );
    }

    if (error) {
        return (
            <div className="bg-red-50 p-4 rounded-lg border border-red-200 text-red-700 flex items-center gap-2">
                <AlertTriangle size={20} />
                {error}
            </div>
        );
    }

    return (
        <div className="space-y-8">
            <div className="flex justify-between items-center">
                <div>
                    <h1 className="text-2xl font-bold text-slate-900 tracking-tight">Dashboard Overview</h1>
                    <p className="text-slate-500 text-sm mt-1">Real-time surveillance of digital trend lifecycles.</p>
                </div>
                <button className="px-4 py-2 bg-indigo-600 text-white rounded-lg text-sm font-semibold hover:bg-indigo-700 transition-all shadow-sm hover:shadow-md active:scale-95">
                    + Track New Trend
                </button>
            </div>

            {/* TOP SECTION: KPIs & Performance Chart */}
            <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
                {/* KPI Column */}
                <div className="lg:col-span-1 space-y-4">
                    <KPICard title="Total Active Trends" value="1,248" change="+12%" positive={true} />
                    <KPICard title="High Risk Alerts" value="14" change="+3" positive={false} />
                    <KPICard title="Avg. Decline Velocity" value="-22%" change="-5%" positive={false} />
                </div>
                {/* Chart Column */}
                <div className="lg:col-span-2">
                    <TrendLifecycleChart />
                </div>
            </div>

            {/* MIDDLE SECTION: Deep Analysis & Simulation */}
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                <DeclineRadarMeter />
                <SaturationLayer />
                {/* What-If Simulator Preview */}
                <div className="bg-white rounded-xl shadow-md p-6 h-80 flex flex-col justify-center items-center text-center space-y-4 border border-slate-100">
                    <div className="p-3 bg-indigo-50 rounded-full text-indigo-600">
                        <Activity size={32} />
                    </div>
                    <h3 className="text-xl font-bold text-gray-800">What-If Simulator</h3>
                    <p className="text-sm text-slate-500">Test scenarios: Ad Spend, Saturation, and Virality impacts.</p>
                    <button
                        onClick={() => navigate('/simulator')}
                        className="px-4 py-2 bg-white border border-indigo-200 text-indigo-600 font-medium rounded-lg hover:bg-indigo-50 transition-colors"
                    >
                        Launch Simulator
                    </button>
                </div>
            </div>

            {/* BOTTOM SECTION: Active Agents / Trends Table */}
            <div className="bg-white rounded-xl shadow-md border border-slate-200 overflow-hidden ring-1 ring-black/5">
                <div className="px-6 py-4 border-b border-slate-100 flex justify-between items-center bg-slate-50/50">
                    <h3 className="text-lg font-bold text-slate-800 tracking-tight">Active Trend Agents</h3>
                    <button className="text-sm text-indigo-600 font-medium hover:text-indigo-700">View All</button>
                </div>
                <div className="overflow-x-auto">
                    <table className="w-full text-left text-sm text-slate-600">
                        <thead className="bg-slate-50/50 border-b border-slate-200">
                            <tr>
                                <th className="px-6 py-4 font-semibold text-xs text-slate-500 uppercase tracking-wider">Trend Name</th>
                                <th className="px-6 py-4 font-semibold text-xs text-slate-500 uppercase tracking-wider">Stage</th>
                                <th className="px-6 py-4 font-semibold text-xs text-slate-500 uppercase tracking-wider">Health</th>
                                <th className="px-6 py-4 font-semibold text-xs text-slate-500 uppercase tracking-wider">Collapse Prob.</th>
                                <th className="px-6 py-4 font-semibold text-xs text-slate-500 uppercase tracking-wider text-right">Action</th>
                            </tr>
                        </thead>
                        <tbody className="divide-y divide-slate-100">
                            {trends.map((trend) => (
                                <tr key={trend.id} className="hover:bg-slate-50/80 transition-colors duration-150 group">
                                    <td className="px-6 py-4 font-medium text-slate-900">{trend.name}</td>
                                    <td className="px-6 py-4">{getStageBadge(trend.stage)}</td>
                                    <td className="px-6 py-4">
                                        <div className="flex items-center gap-2">
                                            <div className="w-16 h-2 bg-slate-100 rounded-full overflow-hidden">
                                                <div
                                                    className={`h-full rounded-full ${trend.health < 40 ? 'bg-red-500' : trend.health < 70 ? 'bg-yellow-500' : 'bg-green-500'}`}
                                                    style={{ width: `${trend.health}%` }}
                                                ></div>
                                            </div>
                                            <span className="text-xs font-medium tabular-nums">{trend.health}/100</span>
                                        </div>
                                    </td>
                                    <td className="px-6 py-4">
                                        <span className={`font-medium ${trend.probability === 'Critical' || trend.probability === 'Very High' ? 'text-red-600' : 'text-slate-600'}`}>
                                            {trend.probability}
                                        </span>
                                    </td>
                                    <td className="px-6 py-4 text-right">
                                        <button
                                            onClick={() => navigate(`/details/${trend.id}`)}
                                            className="inline-flex items-center gap-1 px-3 py-1.5 bg-white border border-slate-200 text-slate-600 rounded-lg text-xs font-medium hover:bg-indigo-50 hover:text-indigo-600 hover:border-indigo-100 transition-all shadow-sm group-hover:shadow-md"
                                        >
                                            Analyze
                                            <ArrowRight size={14} className="group-hover:translate-x-0.5 transition-transform" />
                                        </button>
                                    </td>
                                </tr>
                            ))}
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
    );
};

export default Home;
