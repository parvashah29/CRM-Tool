import { useState, useEffect } from 'react';
import api from '../lib/api';
import { Plus, DollarSign } from 'lucide-react';

const STAGES = ['New', 'Negotiation', 'Won', 'Lost'];

export default function Deals() {
    const [deals, setDeals] = useState([]);
    const [contacts, setContacts] = useState([]); // Needed for creating deals
    const [loading, setLoading] = useState(true);
    const [showForm, setShowForm] = useState(false);
    const [formData, setFormData] = useState({
        title: '',
        value: '',
        stage: 'New',
        contact_id: '',
        expected_close_date: ''
    });

    useEffect(() => {
        fetchDeals();
        fetchContacts();
    }, []);

    const fetchDeals = async () => {
        try {
            const response = await api.get('/deals/');
            setDeals(response.data);
        } catch (error) {
            console.error('Error fetching deals:', error);
        } finally {
            setLoading(false);
        }
    };

    const fetchContacts = async () => {
        try {
            const response = await api.get('/contacts/');
            setContacts(response.data);
        } catch (error) {
            console.error('Error fetching contacts:', error);
        }
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            await api.post('/deals/', formData);
            setFormData({
                title: '',
                value: '',
                stage: 'New',
                contact_id: '',
                expected_close_date: ''
            });
            setShowForm(false);
            fetchDeals();
        } catch (error) {
            console.error('Error creating deal:', error);
        }
    };

    const handleChange = (e) => {
        setFormData({ ...formData, [e.target.name]: e.target.value });
    };

    return (
        <div>
            <div className="flex justify-between items-center mb-6">
                <h1 className="text-3xl font-bold text-gray-800">Deals Pipeline</h1>
                <button
                    onClick={() => setShowForm(!showForm)}
                    className="flex items-center gap-2 bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition-colors"
                >
                    <Plus size={20} />
                    New Deal
                </button>
            </div>

            {showForm && (
                <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-100 mb-6">
                    <h2 className="text-xl font-semibold mb-4">New Deal</h2>
                    <form onSubmit={handleSubmit} className="grid grid-cols-2 gap-4">
                        <input
                            name="title"
                            placeholder="Deal Title"
                            value={formData.title}
                            onChange={handleChange}
                            className="p-2 border rounded focus:ring-2 focus:ring-blue-500 outline-none"
                            required
                        />
                        <input
                            name="value"
                            type="number"
                            placeholder="Value ($)"
                            value={formData.value}
                            onChange={handleChange}
                            className="p-2 border rounded focus:ring-2 focus:ring-blue-500 outline-none"
                            required
                        />
                        <select
                            name="stage"
                            value={formData.stage}
                            onChange={handleChange}
                            className="p-2 border rounded focus:ring-2 focus:ring-blue-500 outline-none"
                        >
                            {STAGES.map(stage => <option key={stage} value={stage}>{stage}</option>)}
                        </select>
                        <select
                            name="contact_id"
                            value={formData.contact_id}
                            onChange={handleChange}
                            className="p-2 border rounded focus:ring-2 focus:ring-blue-500 outline-none"
                            required
                        >
                            <option value="">Select Contact</option>
                            {contacts.map(c => (
                                <option key={c.id} value={c.id}>{c.first_name} {c.last_name}</option>
                            ))}
                        </select>
                        <input
                            name="expected_close_date"
                            type="date"
                            value={formData.expected_close_date}
                            onChange={handleChange}
                            className="p-2 border rounded focus:ring-2 focus:ring-blue-500 outline-none"
                        />

                        <div className="col-span-2 flex justify-end gap-2 mt-2">
                            <button type="button" onClick={() => setShowForm(false)} className="px-4 py-2 text-gray-600 hover:bg-gray-100 rounded">Cancel</button>
                            <button type="submit" className="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700">Save Deal</button>
                        </div>
                    </form>
                </div>
            )}

            <div className="flex gap-6 overflow-x-auto pb-4 h-[calc(100vh-12rem)]">
                {STAGES.map(stage => {
                    const stageDeals = deals.filter(d => d.stage === stage);
                    return (
                        <div key={stage} className="flex-1 min-w-[280px] bg-gray-100/50 rounded-xl p-4 flex flex-col">
                            <h3 className="font-semibold text-gray-700 mb-4 flex justify-between items-center">
                                {stage}
                                <span className="bg-gray-200 text-gray-600 text-xs px-2 py-1 rounded-full">{stageDeals.length}</span>
                            </h3>
                            <div className="space-y-3 overflow-y-auto flex-1 pr-2">
                                {stageDeals.map(deal => (
                                    <div key={deal.id} className="bg-white p-4 rounded-lg shadow-sm border border-gray-100 hover:shadow-md transition-shadow cursor-pointer">
                                        <h4 className="font-medium text-gray-900 mb-1">{deal.title}</h4>
                                        <div className="flex items-center text-green-600 font-medium text-sm mb-2">
                                            <DollarSign size={14} className="mr-1" />
                                            {deal.value}
                                        </div>
                                        <div className="text-xs text-gray-500">
                                            Close: {deal.expected_close_date || 'N/A'}
                                        </div>
                                    </div>
                                ))}
                            </div>
                        </div>
                    );
                })}
            </div>
        </div>
    );
}
