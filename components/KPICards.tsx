import React from 'react';
import { DollarSign, ShoppingBag, Users, TrendingUp, Activity } from 'lucide-react';

interface KPIProps {
    data: {
        revenue: number;
        orders: number;
        customers: number;
        top_product: string;
        aov: number;
        clv: number;
    } | null;
}

const KPICard = ({ title, value, icon: Icon, color }: { title: string, value: string, icon: any, color: string }) => (
    <div className={`p-6 rounded-xl border border-gray-100 bg-white shadow-sm flex items-center space-x-4`}>
        <div className={`p-3 rounded-full ${color} text-white`}>
            <Icon size={24} />
        </div>
        <div>
            <p className="text-sm text-gray-500 font-medium">{title}</p>
            <h3 className="text-2xl font-bold text-gray-800">{value}</h3>
        </div>
    </div>
);

export default function KPICards({ data }: KPIProps) {
    if (!data) return <div className="animate-pulse h-32 bg-gray-100 rounded-xl"></div>;

    const formatCurrency = (val: number) => `$${val.toLocaleString(undefined, { maximumFractionDigits: 0 })}`;
    const formatNumber = (val: number) => val.toLocaleString();

    return (
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
            <KPICard
                title="Total Revenue"
                value={formatCurrency(data.revenue)}
                icon={DollarSign}
                color="bg-blue-500"
            />
            <KPICard
                title="Total Orders"
                value={formatNumber(data.orders)}
                icon={ShoppingBag}
                color="bg-purple-500"
            />
            <KPICard
                title="Total Customers"
                value={formatNumber(data.customers)}
                icon={Users}
                color="bg-green-500"
            />
            <div className="col-span-1 md:col-span-3 grid grid-cols-1 md:grid-cols-3 gap-6">
                <div className="md:col-span-2 p-6 rounded-xl border border-blue-100 bg-blue-50/50">
                    <p className="text-sm text-blue-600 font-medium mb-1">Top Product</p>
                    <h3 className="text-lg font-bold text-gray-800 line-clamp-1" title={data.top_product}>
                        {data.top_product}
                    </h3>
                </div>
                <div className="grid grid-cols-1 gap-4">
                    <div className="flex justify-between items-center p-4 rounded-xl bg-gray-50 border border-gray-100">
                        <span className="text-sm text-gray-500">AOV</span>
                        <span className="font-bold text-gray-800">${data.aov.toFixed(2)}</span>
                    </div>
                    <div className="flex justify-between items-center p-4 rounded-xl bg-gray-50 border border-gray-100">
                        <span className="text-sm text-gray-500">CLV</span>
                        <span className="font-bold text-gray-800">${data.clv.toFixed(2)}</span>
                    </div>
                </div>
            </div>
        </div>
    );
}
