import { useState, useEffect } from 'react';
import api, { errorMessage } from '../lib/api';
import { Plus, CheckCircle, Circle, Trash2 } from 'lucide-react';
import clsx from 'clsx';

export default function Tasks() {
    const [tasks, setTasks] = useState([]);
    const [loading, setLoading] = useState(true);
    const [showForm, setShowForm] = useState(false);
    const [formData, setFormData] = useState({
        title: '',
        description: '',
        due_date: ''
    });

    useEffect(() => {
        fetchTasks();
    }, []);

    const fetchTasks = async () => {
        try {
            const response = await api.get('/tasks/');
            setTasks(response.data);
        } catch (error) {
            console.error('Error fetching tasks:', error);
        } finally {
            setLoading(false);
        }
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            await api.post('/tasks/', formData);
            setFormData({
                title: '',
                description: '',
                due_date: ''
            });
            setShowForm(false);
            fetchTasks();
        } catch (error) {
            console.error('Error creating task:', error);
            alert(errorMessage(error, 'Failed to create task'));
        }
    };

    const handleChange = (e) => {
        setFormData({ ...formData, [e.target.name]: e.target.value });
    };

    const toggleTask = async (task) => {
        try {
            const res = await api.put(`/tasks/${task.id}`, { is_completed: !task.is_completed });
            setTasks(prev => prev.map(t => (t.id === task.id ? res.data : t)));
        } catch (error) {
            alert(errorMessage(error, 'Failed to update task'));
        }
    };

    const deleteTask = async (task) => {
        try {
            await api.delete(`/tasks/${task.id}`);
            setTasks(prev => prev.filter(t => t.id !== task.id));
        } catch (error) {
            alert(errorMessage(error, 'Failed to delete task'));
        }
    };

    return (
        <div>
            <div className="flex justify-between items-center mb-6">
                <h1 className="text-3xl font-bold text-gray-800">Tasks</h1>
                <button
                    onClick={() => setShowForm(!showForm)}
                    className="flex items-center gap-2 bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition-colors"
                >
                    <Plus size={20} />
                    New Task
                </button>
            </div>

            {showForm && (
                <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-100 mb-6">
                    <h2 className="text-xl font-semibold mb-4">New Task</h2>
                    <form onSubmit={handleSubmit} className="grid grid-cols-2 gap-4">
                        <input
                            name="title"
                            placeholder="Task Title"
                            value={formData.title}
                            onChange={handleChange}
                            className="col-span-2 p-2 border rounded focus:ring-2 focus:ring-blue-500 outline-none"
                            required
                        />
                        <textarea
                            name="description"
                            placeholder="Description"
                            value={formData.description}
                            onChange={handleChange}
                            className="col-span-2 p-2 border rounded focus:ring-2 focus:ring-blue-500 outline-none"
                            rows="3"
                        />
                        <input
                            name="due_date"
                            type="date"
                            value={formData.due_date}
                            onChange={handleChange}
                            className="p-2 border rounded focus:ring-2 focus:ring-blue-500 outline-none"
                        />

                        <div className="col-span-2 flex justify-end gap-2 mt-2">
                            <button type="button" onClick={() => setShowForm(false)} className="px-4 py-2 text-gray-600 hover:bg-gray-100 rounded">Cancel</button>
                            <button type="submit" className="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700">Save Task</button>
                        </div>
                    </form>
                </div>
            )}

            {loading && <p className="text-gray-500 mb-2">Loading...</p>}
            <div className="space-y-3">
                {tasks.map((task) => (
                    <div key={task.id} className="bg-white p-4 rounded-xl shadow-sm border border-gray-100 flex items-start gap-4 hover:shadow-md transition-shadow">
                        <button onClick={() => toggleTask(task)} aria-label="Toggle complete" className={clsx("mt-1", task.is_completed ? "text-green-500" : "text-gray-300 hover:text-gray-400")}>
                            {task.is_completed ? <CheckCircle size={24} /> : <Circle size={24} />}
                        </button>
                        <div className="flex-1">
                            <h3 className={clsx("font-medium text-lg", task.is_completed && "text-gray-400 line-through")}>{task.title}</h3>
                            <p className="text-gray-600 text-sm mt-1">{task.description}</p>
                            {task.due_date && <div className="text-xs text-gray-400 mt-2">Due: {task.due_date}</div>}
                        </div>
                        <button onClick={() => deleteTask(task)} className="text-gray-300 hover:text-red-500" aria-label="Delete task">
                            <Trash2 size={18} />
                        </button>
                    </div>
                ))}
                {tasks.length === 0 && (
                    <div className="text-center p-8 text-gray-500">No tasks yet.</div>
                )}
            </div>
        </div>
    );
}
