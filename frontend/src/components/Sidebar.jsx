import { Users, Briefcase, CheckSquare, LayoutDashboard } from 'lucide-react';
import { NavLink } from 'react-router-dom';
import clsx from 'clsx';

const navItems = [
    { icon: LayoutDashboard, label: 'Dashboard', path: '/' },
    { icon: Users, label: 'Contacts', path: '/contacts' },
    { icon: Briefcase, label: 'Deals', path: '/deals' },
    { icon: CheckSquare, label: 'Tasks', path: '/tasks' },
];

export default function Sidebar() {
    return (
        <aside className="w-64 bg-gray-900 text-white h-screen flex flex-col border-r border-gray-800 shrink-0">
            <div className="p-6">
                <h1 className="text-2xl font-bold bg-gradient-to-r from-blue-400 to-teal-400 bg-clip-text text-transparent">
                    CRM Pro
                </h1>
            </div>
            <nav className="flex-1 px-4 space-y-2">
                {navItems.map((item) => (
                    <NavLink
                        key={item.path}
                        to={item.path}
                        className={({ isActive }) =>
                            clsx(
                                'flex items-center space-x-3 px-4 py-3 rounded-lg transition-all duration-200',
                                isActive
                                    ? 'bg-blue-600 text-white shadow-lg shadow-blue-500/30 font-semibold'
                                    : 'text-gray-400 hover:bg-gray-800 hover:text-white'
                            )
                        }
                    >
                        <item.icon size={20} />
                        <span className="font-medium">{item.label}</span>
                    </NavLink>
                ))}
            </nav>
            <div className="p-4 border-t border-gray-800">
                <div className="flex items-center space-x-3 text-gray-400 text-sm">
                    <span>v1.0.0</span>
                </div>
            </div>
        </aside>
    );
}
