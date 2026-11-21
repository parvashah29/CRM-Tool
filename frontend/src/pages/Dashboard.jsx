import { useEffect, useState } from 'react';
import { Users, Briefcase, DollarSign, CheckSquare } from 'lucide-react';
import api, { errorMessage } from '../lib/api';

const money = (n) => `$${Number(n || 0).toLocaleString()}`;

function StatCard({ icon, label, value, tone }) {
    const Icon = icon;
    return (
        <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-100 flex items-center gap-4">
            <div className={`w-12 h-12 rounded-lg flex items-center justify-center ${tone}`}>
                <Icon size={22} />
            </div>
            <div>
                <div className="text-sm text-gray-500">{label}</div>
                <div className="text-2xl font-bold text-gray-900">{value}</div>
            </div>
        </div>
    );
}

export default function Dashboard() {
    const [stats, setStats] = useState(null);
    const [error, setError] = useState('');

    useEffect(() => {
        api.get('/stats')
            .then(res => setStats(res.data))
            .catch(err => setError(errorMessage(err, 'Failed to load dashboard')));
    }, []);

    if (error) return <div className="text-red-600">{error}</div>;
    if (!stats) return <p>Loading...</p>;

    const stages = Object.entries(stats.deals_by_stage);
    const maxCount = Math.max(1, ...stages.map(([, n]) => n));

    return (
        <div>
            <h1 className="text-3xl font-bold mb-6 text-gray-800">Dashboard</h1>
            <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-4 gap-4 mb-8">
                <StatCard icon={Users} label="Contacts" value={stats.contacts} tone="bg-blue-100 text-blue-600" />
                <StatCard icon={Briefcase} label="Open pipeline" value={money(stats.open_pipeline_value)} tone="bg-amber-100 text-amber-600" />
                <StatCard icon={DollarSign} label="Won revenue" value={money(stats.won_value)} tone="bg-green-100 text-green-600" />
                <StatCard icon={CheckSquare} label="Open tasks" value={`${stats.tasks_open} / ${stats.tasks_open + stats.tasks_done}`} tone="bg-purple-100 text-purple-600" />
            </div>

            <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-100 max-w-xl">
                <h2 className="text-lg font-semibold mb-4 text-gray-800">Deals by stage</h2>
                <div className="space-y-3">
                    {stages.map(([stage, count]) => (
                        <div key={stage} className="flex items-center gap-3">
                            <div className="w-28 text-sm text-gray-600">{stage}</div>
                            <div className="flex-1 bg-gray-100 rounded-full h-3">
                                <div className="bg-blue-500 h-3 rounded-full" style={{ width: `${(count / maxCount) * 100}%` }} />
                            </div>
                            <div className="w-6 text-sm text-gray-700 text-right">{count}</div>
                        </div>
                    ))}
                </div>
            </div>
        </div>
    );
}
