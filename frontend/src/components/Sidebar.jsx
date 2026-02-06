import React from 'react';

const Sidebar = () => {
    const menuItems = [
        { name: 'Dashboard', icon: '📊' },
        { name: 'Agents', icon: '🤖' },
        { name: 'Analytics', icon: '📈' },
        { name: 'Settings', icon: '⚙️' },
    ];

    return (
        <div className="w-64 bg-white h-screen border-r border-gray-200 flex flex-col fixed left-0 top-0 z-50">
            <div className="p-6 border-b border-gray-100">
                <h1 className="text-2xl font-bold bg-gradient-to-r from-blue-600 to-indigo-600 bg-clip-text text-transparent">
                    HackProject
                </h1>
            </div>
            <nav className="flex-1 p-4 space-y-2 overflow-y-auto">
                {menuItems.map((item) => (
                    <div
                        key={item.name}
                        className="flex items-center gap-3 px-4 py-3 text-gray-600 hover:bg-blue-50 hover:text-blue-600 rounded-xl cursor-pointer transition-all duration-200 group"
                    >
                        <span className="text-xl group-hover:scale-110 transition-transform">{item.icon}</span>
                        <span className="font-medium">{item.name}</span>
                    </div>
                ))}
            </nav>
            <div className="p-4 border-t border-gray-100">
                <div className="flex items-center gap-3 px-4 py-2 hover:bg-gray-50 rounded-lg cursor-pointer transition-colors">
                    <div className="w-8 h-8 rounded-full bg-indigo-100 flex items-center justify-center text-indigo-600 font-bold">U</div>
                    <div>
                        <p className="text-sm font-semibold text-gray-700">User</p>
                        <p className="text-xs text-gray-500">Admin</p>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default Sidebar;
