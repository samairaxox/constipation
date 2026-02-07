import React, { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import { ArrowLeft, TrendingDown, Users, MessageSquare, Activity, AlertTriangle, BookOpen, Zap } from 'lucide-react';
import { getTrendDetails } from '../api/trends';

const TrendDetails = () => {
    const { trendId } = useParams();
    const [trendData, setTrendData] = useState(null);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);

    useEffect(() => {
        if (!trendId) return;

        const fetchDetails = async () => {
            setLoading(true);
            setError(null); // Clear previous errors
            try {
                const data = await getTrendDetails(trendId);
                setTrendData(data);
                setLoading(false);
            } catch (err) {
                console.error("Failed to fetch trend details:", err);
                setError("Failed to load trend analysis.");
                setLoading(false);
            }
        };

        fetchDetails();
    }, [trendId]);

    if (!trendId) {
        return (
            <div className="flex flex-col items-center justify-center h-[60vh] text-center space-y-4">
                <div className="w-16 h-16 bg-slate-100 rounded-full flex items-center justify-center text-3xl">
                    🔍
                </div>
                <h2 className="text-xl font-semibold text-slate-800">Select a Trend</h2>
                <p className="text-slate-500 max-w-xs">
                    Choose a trend from the Portfolio list to view its detailed analysis and decline prediction.
                </p>
                <Link to="/" className="px-4 py-2 bg-indigo-600 text-white rounded-lg text-sm font-medium hover:bg-indigo-700 transition-colors">
                    Go to Trend List
                </Link>
            </div>
        );
    }

    if (loading) {
        return (
            <div className="flex justify-center items-center h-64">
                <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-indigo-600"></div>
            </div>
        );
    }

    if (error || !trendData) {
        return (
            <div className="bg-red-50 p-4 rounded-lg border border-red-200 text-red-700 flex items-center gap-2">
                <AlertTriangle size={20} />
                {error || "Trend not found."}
            </div>
        );
    }

    return (
        <div className="space-y-8">
            {/* Header Section */}
            <div className="space-y-4">
                <div className="flex items-center gap-4">
                    <Link to="/" className="p-2 hover:bg-slate-100 rounded-full transition-colors group">
                        <ArrowLeft size={20} className="text-slate-500 group-hover:text-slate-800" />
                    </Link>
                    <div>
                        <h1 className="text-2xl font-bold text-slate-900 tracking-tight">Trend Analysis: {trendData.name}</h1>
                        <p className="text-slate-500 text-sm">AI-Driven Decline Prediction & Explanation</p>
                    </div>
                </div>

                {/* Summary Badges */}
                <div className="bg-white p-6 rounded-xl border border-slate-200 shadow-sm flex flex-wrap gap-8 items-center ring-1 ring-black/5">
                    <div className="flex flex-col gap-1">
                        <span className="text-xs text-slate-500 font-semibold uppercase tracking-wider">Stage</span>
                        <span className="text-sm font-bold text-orange-700 bg-orange-50 px-3 py-1 rounded-full border border-orange-100 w-fit">{trendData.stage}</span>
                    </div>
                    <div className="h-10 w-px bg-slate-100"></div>
                    <div className="flex flex-col gap-1">
                        <span className="text-xs text-slate-500 font-semibold uppercase tracking-wider">Decline Probability</span>
                        <span className="text-xl font-bold text-slate-900">{trendData.probability}</span>
                    </div>
                    <div className="h-10 w-px bg-slate-100"></div>
                    <div className="flex flex-col gap-1">
                        <span className="text-xs text-slate-500 font-semibold uppercase tracking-wider">Collapse ETA</span>
                        <span className="text-xl font-bold text-slate-900">{trendData.eta}</span>
                    </div>
                    <div className="h-10 w-px bg-slate-100"></div>
                    <div className="flex flex-col gap-1">
                        <span className="text-xs text-slate-500 font-semibold uppercase tracking-wider">Confidence</span>
                        <span className="text-sm font-bold text-green-700 bg-green-50 px-2 py-1 rounded border border-green-100">{trendData.confidence}</span>
                    </div>
                </div>
            </div>

            {/* KPI Cards Row */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
                <div className="bg-white p-5 rounded-xl border border-slate-200 shadow-sm hover:shadow-md transition-shadow ring-1 ring-black/5">
                    <div className="flex items-center gap-2 mb-3 text-slate-500">
                        <Activity size={18} />
                        <span className="text-xs font-semibold uppercase tracking-wide">Engagement (7d)</span>
                    </div>
                    <div className="text-3xl font-bold text-slate-900 tracking-tight">{trendData.kpi?.engagement || '-14.2%'}</div>
                </div>
                <div className="bg-white p-5 rounded-xl border border-slate-200 shadow-sm hover:shadow-md transition-shadow ring-1 ring-black/5">
                    <div className="flex items-center gap-2 mb-3 text-slate-500">
                        <Users size={18} />
                        <span className="text-xs font-semibold uppercase tracking-wide">Influencer Part.</span>
                    </div>
                    <div className="text-3xl font-bold text-slate-900 tracking-tight">{trendData.kpi?.influencers || '-28%'}</div>
                </div>
                <div className="bg-white p-5 rounded-xl border border-slate-200 shadow-sm hover:shadow-md transition-shadow ring-1 ring-black/5">
                    <div className="flex items-center gap-2 mb-3 text-slate-500">
                        <MessageSquare size={18} />
                        <span className="text-xs font-semibold uppercase tracking-wide">Sentiment Shift</span>
                    </div>
                    <div className="text-3xl font-bold text-orange-600 tracking-tight">{trendData.kpi?.sentiment || 'Neutral → Neg'}</div>
                </div>
                <div className="bg-white p-5 rounded-xl border border-slate-200 shadow-sm hover:shadow-md transition-shadow ring-1 ring-black/5">
                    <div className="flex items-center gap-2 mb-3 text-slate-500">
                        <TrendingDown size={18} />
                        <span className="text-xs font-semibold uppercase tracking-wide">Saturation Score</span>
                    </div>
                    <div className="text-3xl font-bold text-slate-900 tracking-tight">{trendData.kpi?.saturation || '92/100'}</div>
                </div>
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
                {/* Left Column: Drivers & Chart */}
                <div className="lg:col-span-2 space-y-6">
                    {/* Decline Drivers */}
                    <div className="bg-white rounded-xl border border-slate-200 shadow-sm overflow-hidden ring-1 ring-black/5">
                        <div className="px-6 py-4 border-b border-slate-100 bg-slate-50/50 flex justify-between items-center">
                            <h3 className="font-semibold text-slate-800 flex items-center gap-2">
                                <AlertTriangle size={18} className="text-orange-500" />
                                Top 5 Decline Drivers
                            </h3>
                        </div>
                        <div className="divide-y divide-slate-100">
                            {(trendData.drivers || []).map((driver, idx) => (
                                <div key={idx} className="p-5 hover:bg-slate-50/50 transition-colors text-left">
                                    <div className="flex justify-between items-start mb-3 gap-4">
                                        <h4 className="font-semibold text-slate-900 text-sm leading-tight flex-1 text-left">{driver.name}</h4>
                                        <span className={`shrink-0 text-[10px] px-2.5 py-1 rounded-full font-bold uppercase tracking-wide border ${driver.impact === 'High' ? 'bg-red-50 text-red-700 border-red-100' :
                                                driver.impact === 'Medium' ? 'bg-orange-50 text-orange-700 border-orange-100' :
                                                    'bg-yellow-50 text-yellow-700 border-yellow-100'
                                            }`}>{driver.impact} Impact</span>
                                    </div>
                                    <ul className="text-sm text-slate-600 list-disc list-outside space-y-1.5 ml-5 text-left leading-relaxed marker:text-slate-400">
                                        {driver.evidence.map((ev, i) => (
                                            <li key={i} className="pl-1">{ev}</li>
                                        ))}
                                    </ul>
                                </div>
                            ))}
                        </div>
                    </div>

                    {/* Chart Placeholder (Reduced dominance) */}
                    <div className="bg-white p-8 rounded-xl border border-slate-200 shadow-sm h-80 flex flex-col items-center justify-center text-slate-400 border-dashed bg-slate-50/30 ring-1 ring-black/5">
                        <Activity size={48} className="mb-4 opacity-20" />
                        <p className="font-medium">Decline Trajectory Chart</p>
                        <p className="text-xs mt-2 opacity-70">Waiting for data signal...</p>
                    </div>
                </div>

                {/* Right Column: AI Insight & Strategy */}
                <div className="space-y-6">
                    {/* AI Narrative Insight */}
                    <div className="bg-gradient-to-br from-indigo-50/80 to-white p-6 rounded-xl border border-indigo-100 shadow-sm ring-1 ring-indigo-50">
                        <h3 className="font-bold text-indigo-900 flex items-center gap-2 mb-4 text-sm uppercase tracking-wide">
                            <BookOpen size={16} className="text-indigo-600" />
                            AI Insight
                        </h3>
                        <p className="text-sm text-slate-600 leading-7 text-justify text-pretty">
                            {trendData.narrative}
                        </p>
                    </div>

                    {/* Strategy Recommendations */}
                    <div className="bg-white rounded-xl border border-slate-200 shadow-sm overflow-hidden ring-1 ring-black/5">
                        <div className="px-6 py-4 border-b border-slate-100 bg-slate-50/50">
                            <h3 className="font-semibold text-slate-800 flex items-center gap-2">
                                <Zap size={18} className="text-yellow-500" />
                                Strategy Actions
                            </h3>
                        </div>
                        <div className="p-6 space-y-3">
                            <div className="p-4 bg-red-50 border border-red-100 rounded-xl hover:shadow-sm transition-shadow">
                                <h4 className="font-bold text-red-900 text-sm mb-1 flex items-center gap-2">
                                    <span className="w-2 h-2 rounded-full bg-red-500"></span>
                                    EXIT (Recommended)
                                </h4>
                                <p className="text-xs text-red-700 mt-1 leading-relaxed">Cease all new content production. Organic reach has collapsed below viable thresholds.</p>
                            </div>
                            <div className="p-4 bg-white border border-slate-200 rounded-xl opacity-60 hover:opacity-100 transition-opacity">
                                <h4 className="font-bold text-slate-700 text-sm mb-1">PIVOT</h4>
                                <p className="text-xs text-slate-500 mt-1">Nostalgia/Satire angle possible but high risk.</p>
                            </div>
                            <div className="p-4 bg-white border border-slate-200 rounded-xl opacity-60 hover:opacity-100 transition-opacity">
                                <h4 className="font-bold text-slate-700 text-sm mb-1">REVIVE</h4>
                                <p className="text-xs text-slate-500 mt-1">ROI projected to be negative (-12x).</p>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default TrendDetails;
