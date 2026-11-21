import { useState, useEffect } from 'react';
import api, { errorMessage } from '../lib/api';
import { Plus, Trash2, User } from 'lucide-react';

export default function Contacts() {
    const [contacts, setContacts] = useState([]);
    const [loading, setLoading] = useState(true);
    const [showForm, setShowForm] = useState(false);
    const [formData, setFormData] = useState({
        first_name: '',
        last_name: '',
        email: '',
        phone: '',
        company: '',
        position: ''
    });

    useEffect(() => {
        fetchContacts();
    }, []);

    const fetchContacts = async () => {
        try {
            const response = await api.get('/contacts/');
            setContacts(response.data);
        } catch (error) {
            console.error('Error fetching contacts:', error);
        } finally {
            setLoading(false);
        }
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            await api.post('/contacts/', formData);
            setFormData({
                first_name: '',
                last_name: '',
                email: '',
                phone: '',
                company: '',
                position: ''
            });
            setShowForm(false);
            fetchContacts();
        } catch (error) {
            console.error('Error creating contact:', error);
            alert(errorMessage(error, 'Failed to create contact'));
        }
    };

    const handleDelete = async (contact) => {
        if (!confirm(`Delete ${contact.first_name} ${contact.last_name}?`)) return;
        try {
            await api.delete(`/contacts/${contact.id}`);
            setContacts(prev => prev.filter(c => c.id !== contact.id));
        } catch (error) {
            alert(errorMessage(error, 'Failed to delete contact'));
        }
    };

    const handleChange = (e) => {
        setFormData({ ...formData, [e.target.name]: e.target.value });
    };

    return (
        <div>
            <div className="flex justify-between items-center mb-6">
                <h1 className="text-3xl font-bold text-gray-800">Contacts</h1>
                <button
                    onClick={() => setShowForm(!showForm)}
                    className="flex items-center gap-2 bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition-colors"
                >
                    <Plus size={20} />
                    Add Contact
                </button>
            </div>

            {showForm && (
                <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-100 mb-6">
                    <h2 className="text-xl font-semibold mb-4">New Contact</h2>
                    <form onSubmit={handleSubmit} className="grid grid-cols-2 gap-4">
                        <input
                            name="first_name"
                            placeholder="First Name"
                            value={formData.first_name}
                            onChange={handleChange}
                            className="p-2 border rounded focus:ring-2 focus:ring-blue-500 outline-none"
                            required
                        />
                        <input
                            name="last_name"
                            placeholder="Last Name"
                            value={formData.last_name}
                            onChange={handleChange}
                            className="p-2 border rounded focus:ring-2 focus:ring-blue-500 outline-none"
                            required
                        />
                        <input
                            name="email"
                            type="email"
                            placeholder="Email"
                            value={formData.email}
                            onChange={handleChange}
                            className="p-2 border rounded focus:ring-2 focus:ring-blue-500 outline-none"
                            required
                        />
                        <input
                            name="phone"
                            placeholder="Phone"
                            value={formData.phone}
                            onChange={handleChange}
                            className="p-2 border rounded focus:ring-2 focus:ring-blue-500 outline-none"
                        />
                        <input
                            name="company"
                            placeholder="Company"
                            value={formData.company}
                            onChange={handleChange}
                            className="p-2 border rounded focus:ring-2 focus:ring-blue-500 outline-none"
                        />
                        <input
                            name="position"
                            placeholder="Position"
                            value={formData.position}
                            onChange={handleChange}
                            className="p-2 border rounded focus:ring-2 focus:ring-blue-500 outline-none"
                        />
                        <div className="col-span-2 flex justify-end gap-2 mt-2">
                            <button
                                type="button"
                                onClick={() => setShowForm(false)}
                                className="px-4 py-2 text-gray-600 hover:bg-gray-100 rounded"
                            >
                                Cancel
                            </button>
                            <button
                                type="submit"
                                className="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700"
                            >
                                Save Contact
                            </button>
                        </div>
                    </form>
                </div>
            )}

            {loading ? (
                <p>Loading...</p>
            ) : (
                <div className="bg-white rounded-xl shadow-sm border border-gray-100 overflow-hidden">
                    <table className="w-full text-left">
                        <thead className="bg-gray-50 border-b border-gray-100">
                            <tr>
                                <th className="p-4 font-semibold text-gray-600">Name</th>
                                <th className="p-4 font-semibold text-gray-600">Email</th>
                                <th className="p-4 font-semibold text-gray-600">Phone</th>
                                <th className="p-4 font-semibold text-gray-600">Company</th>
                                <th className="p-4"></th>
                            </tr>
                        </thead>
                        <tbody className="divide-y divide-gray-100">
                            {contacts.map((contact) => (
                                <tr key={contact.id} className="hover:bg-gray-50/50 transition-colors">
                                    <td className="p-4 flex items-center gap-3">
                                        <div className="w-8 h-8 rounded-full bg-blue-100 text-blue-600 flex items-center justify-center">
                                            <User size={16} />
                                        </div>
                                        <div>
                                            <div className="font-medium text-gray-900">{contact.first_name} {contact.last_name}</div>
                                            <div className="text-sm text-gray-500">{contact.position}</div>
                                        </div>
                                    </td>
                                    <td className="p-4 text-gray-600">{contact.email}</td>
                                    <td className="p-4 text-gray-600">{contact.phone}</td>
                                    <td className="p-4 text-gray-600 font-medium">{contact.company}</td>
                                    <td className="p-4 text-right">
                                        <button onClick={() => handleDelete(contact)} className="text-gray-300 hover:text-red-500" aria-label="Delete contact">
                                            <Trash2 size={18} />
                                        </button>
                                    </td>
                                </tr>
                            ))}
                            {contacts.length === 0 && (
                                <tr>
                                    <td colSpan="5" className="p-8 text-center text-gray-500">
                                        No contacts found. Create one to get started.
                                    </td>
                                </tr>
                            )}
                        </tbody>
                    </table>
                </div>
            )}
        </div>
    );
}
