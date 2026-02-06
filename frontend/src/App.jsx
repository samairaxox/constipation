import React, { useState, useEffect } from 'react';
import Sidebar from './components/Sidebar';
import KPICard from './components/KPICard';
import ChartSection from './components/ChartSection';
import axios from 'axios';

function App() {
  const [serverStatus, setServerStatus] = useState('Checking...');

  useEffect(() => {
    const checkBackend = async () => {
      try {
        const res = await axios.get('http://127.0.0.1:8000/');
        if (res.data) {
          setServerStatus('Online');
        }
      } catch (err) {
        setServerStatus('Offline');
      }
    };
    checkBackend();
  }, []);

  return (
    <div className="flex bg-slate-50 min-h-screen font-sans text-gray-900">
      <Sidebar />

      <main className="flex-1 ml-64 p-8 overflow-y-auto h-screen">
        <div className="max-w-7xl mx-auto space-y-8">

          {/* Header */}
          <div className="flex justify-between items-center bg-white p-4 rounded-2xl shadow-sm border border-gray-100">
            <div>
              <h2 className="text-2xl font-bold text-gray-800">Dashboard</h2>
              <p className="text-gray-500 text-sm mt-1">Overview of system performance and agents</p>
            </div>
            <div className="flex items-center gap-4">
              <div className={`flex items-center gap-2 px-3 py-1.5 rounded-full text-sm font-medium border ${serverStatus === 'Online'
                  ? 'bg-green-50 text-green-700 border-green-200'
                  : 'bg-amber-50 text-amber-700 border-amber-200'
                }`}>
                <div className={`w-2 h-2 rounded-full ${serverStatus === 'Online' ? 'bg-green-500' : 'bg-amber-500'
                  }`}></div>
                Backend: {serverStatus}
              </div>
              <button className="px-5 py-2.5 bg-indigo-600 text-white font-medium rounded-xl hover:bg-indigo-700 transition-colors shadow-lg shadow-indigo-200">
                + New Task
              </button>
            </div>
          </div>

          {/* KPI Cards */}
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
            <KPICard title="Total Transactions" value="$54,230" change="+12.5%" positive={true} />
            <KPICard title="Active Agents" value="8" change="+2" positive={true} />
            <KPICard title="System Load" value="45%" change="-2.4%" positive={true} />
            <KPICard title="Errors" value="23" change="+5.2%" positive={false} />
          </div>

          {/* Main Content Area */}
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 h-96">
            <div className="lg:col-span-2 h-full">
              <ChartSection />
            </div>

            {/* Activity Feed */}
            <div className="bg-white p-6 rounded-2xl shadow-sm border border-gray-100 h-full overflow-hidden flex flex-col">
              <div className="flex justify-between items-center mb-6">
                <h3 className="font-bold text-gray-800">Recent Activity</h3>
                <button className="text-indigo-600 text-sm font-medium hover:text-indigo-700">View All</button>
              </div>
              <div className="space-y-6 overflow-y-auto pr-2 custom-scrollbar">
                {[1, 2, 3, 4, 5].map((i) => (
                  <div key={i} className="flex gap-4">
                    <div className="mt-1 w-2 h-2 rounded-full bg-indigo-500 shrink-0"></div>
                    <div>
                      <p className="text-sm font-medium text-gray-700">Marketing Agent process started</p>
                      <p className="text-xs text-gray-400 mt-1">2 mins ago • Automated</p>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>

          {/* Agents Section */}
          <div>
            <h3 className="text-xl font-bold text-gray-800 mb-4">Active Agents</h3>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
              {['Marketing Agent', 'Finance Agent', 'Orchestrator'].map((agent) => (
                <div key={agent} className="bg-white p-5 rounded-xl border border-gray-100 hover:border-indigo-100 transition-colors group cursor-pointer">
                  <div className="flex items-center gap-4 mb-3">
                    <div className="w-10 h-10 rounded-lg bg-indigo-50 flex items-center justify-center text-indigo-600 text-xl group-hover:bg-indigo-600 group-hover:text-white transition-colors">
                      🤖
                    </div>
                    <div>
                      <h4 className="font-bold text-gray-800">{agent}</h4>
                      <span className="text-xs px-2 py-0.5 bg-green-100 text-green-700 rounded-full">Running</span>
                    </div>
                  </div>
                  <p className="text-sm text-gray-500">Autonomous processing of {agent.toLowerCase()} tasks.</p>
                </div>
              ))}
            </div>
          </div>

        </div>
      </main>
    </div>
  );
}

export default App;
