import React from 'react';
import { useNavigate } from 'react-router-dom';
import { Bell, Search, LogOut } from 'lucide-react';

const Header = ({ title }) => {
    const navigate = useNavigate();

    const handleLogout = () => {
        localStorage.removeItem('auth');
        navigate('/login');
    };

    return (
        <header className="fixed top-0 right-0 left-64 h-16 bg-white/80 backdrop-blur-md border-b border-slate-200/50 flex items-center justify-between px-8 z-10 transition-all duration-200">
            <div className="flex items-center gap-4">
                <h2 className="text-lg font-semibold text-slate-800">{title}</h2>
            </div>

            <div className="flex items-center gap-6">
                <div className="relative">
                    <Search className="absolute left-3 top-2.5 text-slate-400" size={18} />
                    <input
                        type="text"
                        placeholder="Search trends..."
                        className="pl-10 pr-4 py-2 bg-slate-100/50 border border-slate-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500/20 focus:border-indigo-500 w-64 text-sm transition-all duration-200 placeholder:text-slate-400"
                    />
                </div>

                <button className="relative p-2 hover:bg-slate-100 rounded-full transition-colors">
                    <Bell size={20} className="text-slate-600" />
                    <span className="absolute top-2 right-2.5 w-2 h-2 bg-red-500 rounded-full border-2 border-white"></span>
                </button>

                <div className="h-8 w-px bg-slate-200"></div>

                <div className="flex items-center gap-3">
                    <div className="w-8 h-8 bg-indigo-100 rounded-full flex items-center justify-center text-indigo-600 font-bold text-sm">
                        AD
                    </div>
                    <button
                        onClick={handleLogout}
                        className="p-2 hover:bg-slate-100 rounded-full transition-colors text-slate-500 hover:text-red-600"
                        title="Sign Out"
                    >
                        <LogOut size={18} />
                    </button>
                </div>
            </div>
        </header>
    );
};

export default Header;
