import React from 'react';
import { NavLink } from 'react-router-dom';
import { Home, BarChart2, MessageCircle, Search, Settings, LayoutDashboard } from 'lucide-react';

const navItems = [
    { path: '/', label: 'Dashboard', icon: Home },
    { path: '/details', label: 'Trend Details', icon: BarChart2 },
    { path: '/chat', label: 'Chat Analyst', icon: MessageCircle },
    { path: '/simulator', label: 'What-If Simulator', icon: Search },
    { path: '/settings', label: 'Settings', icon: Settings },
];

const Sidebar = () => {
    return (
        <aside className="fixed inset-y-0 left-0 w-64 bg-white border-r border-slate-200 p-4 shadow-sm flex flex-col z-20">
            <div className="flex items-center justify-center mb-8 pt-2">
                <div className="p-2 bg-indigo-50 rounded-lg">
                    <LayoutDashboard size={28} className="text-indigo-600" />
                </div>
                <span className="ml-3 text-lg font-bold text-slate-800 tracking-tight">Trend Predictor</span>
            </div>
            <nav className="flex-1 space-y-1">
                {navItems.map((item) => (
                    <NavLink
                        key={item.path}
                        to={item.path}
                        className={({ isActive }) =>
                            `flex items-center px-4 py-3 rounded-xl text-sm font-medium transition-all duration-200 group ${isActive
                                ? 'bg-indigo-50 text-indigo-700 shadow-sm ring-1 ring-indigo-200'
                                : 'text-slate-500 hover:bg-slate-50 hover:text-slate-900'
                            }`
                        }
                    >
                        <item.icon size={20} className="mr-3 transition-colors duration-200 group-hover:text-current" />
                        {item.label}
                    </NavLink>
                ))}
            </nav>
            <div className="mt-auto pt-6 border-t border-slate-100">
                <div className="flex items-center gap-3 px-2">
                    <div className="w-8 h-8 rounded-full bg-indigo-100 flex items-center justify-center text-xs font-bold text-indigo-700">
                        AD
                    </div>
                    <div className="overflow-hidden">
                        <p className="text-sm font-medium text-slate-700 truncate">Arshia Dang</p>
                        <p className="text-xs text-slate-500 truncate">Pro Account</p>
                    </div>
                </div>
            </div>
        </aside>
    );
};

export default Sidebar;
