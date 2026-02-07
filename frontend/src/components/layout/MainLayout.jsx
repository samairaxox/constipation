import React from 'react';
import { Outlet, useLocation } from 'react-router-dom';
import Sidebar from './Sidebar';
import Header from './Header';

const MainLayout = () => {
    const location = useLocation();

    // Simple map to determine header title based on current path
    const getPageTitle = (pathname) => {
        switch (pathname) {
            case '/': return 'Dashboard - Trend List';
            case '/details': return 'Trend Analysis Details';
            case '/chat': return 'AI Analyst Chat';
            case '/simulator': return 'Scenario Simulator';
            default: return 'Dashboard';
        }
    };

    return (
        <div className="flex min-h-screen bg-slate-50">
            <Sidebar />
            <div className="flex-1 ml-64">
                <Header title={getPageTitle(location.pathname)} />
                <main className="mt-16 p-8">
                    <div className="max-w-7xl mx-auto">
                        <Outlet />
                    </div>
                </main>
            </div>
        </div>
    );
};

export default MainLayout;
