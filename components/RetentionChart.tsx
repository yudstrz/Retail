'use client';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';

interface RetentionChartProps {
    data: any[];
}

export default function RetentionChart({ data }: RetentionChartProps) {
    if (!data || data.length === 0) return <div className="h-64 flex items-center justify-center text-gray-400">No Data Available</div>;

    return (
        <div className="p-6 bg-white rounded-xl border border-gray-100 shadow-sm">
            <h3 className="text-lg font-bold text-gray-800 mb-4">Retention & Churn Rate</h3>
            <div className="h-80">
                <ResponsiveContainer width="100%" height="100%">
                    <LineChart data={data}>
                        <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#E5E7EB" />
                        <XAxis
                            dataKey="Month"
                            axisLine={false}
                            tickLine={false}
                            tick={{ fill: '#6B7280', fontSize: 12 }}
                            dy={10}
                        />
                        <YAxis
                            axisLine={false}
                            tickLine={false}
                            tick={{ fill: '#6B7280', fontSize: 12 }}
                            tickFormatter={(val) => `${(val * 100).toFixed(0)}%`}
                        />
                        <Tooltip
                            contentStyle={{ borderRadius: '8px', border: 'none', boxShadow: '0 4px 6px -1px rgb(0 0 0 / 0.1)' }}
                        />
                        <Legend />
                        <Line type="monotone" dataKey="RetentionRate" stroke="#10B981" strokeWidth={2} dot={{ r: 4 }} name="Retention Rate" />
                        <Line type="monotone" dataKey="ChurnRate" stroke="#EF4444" strokeWidth={2} dot={{ r: 4 }} name="Churn Rate" />
                    </LineChart>
                </ResponsiveContainer>
            </div>
        </div>
    );
}
