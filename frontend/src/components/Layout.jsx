import { Outlet } from 'react-router-dom';
import Sidebar from './Sidebar';

export default function Layout() {
    return (
        <div className="flex h-screen bg-gray-50 text-gray-900 font-sans overflow-hidden">
            <Sidebar />
            <main className="flex-1 overflow-auto relative w-full">
                <div className="p-8 max-w-7xl mx-auto h-full">
                    <Outlet />
                </div>
            </main>
        </div>
    );
}
