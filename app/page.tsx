'use client';

import { useState, useEffect } from 'react';
import KPICards from '@/components/KPICards';
import RevenueChart from '@/components/RevenueChart';
import RetentionChart from '@/components/RetentionChart';
import { Filter } from 'lucide-react';

export default function Home() {
  const [filters, setFilters] = useState<{ years: string[], months: number[] }>({ years: [], months: [] });

  const [selectedYear, setSelectedYear] = useState('All');
  const [selectedMonth, setSelectedMonth] = useState('All');

  const [stats, setStats] = useState(null);
  const [revenueData, setRevenueData] = useState([]);
  const [retentionData, setRetentionData] = useState([]);
  const [loading, setLoading] = useState(true);

  // Fetch Filters
  useEffect(() => {
    fetch('/api/filters')
      .then(res => res.json())
      .then(data => {
        setFilters(data);
      })
      .catch(err => console.error("Failed to load filters", err));
  }, []);

  // Fetch Dashboard Data
  useEffect(() => {
    async function fetchData() {
      setLoading(true);
      try {
        const query = `?year=${selectedYear}&month=${selectedMonth}`;

        const [statsRes, revRes, retRes] = await Promise.all([
          fetch(`/api/stats${query}`),
          fetch(`/api/revenue${query}`),
          fetch(`/api/retention${query}`)
        ]);

        const statsData = await statsRes.json();
        const revData = await revRes.json();
        const retData = await retRes.json();

        setStats(statsData);
        setRevenueData(revData);
        setRetentionData(retData);
      } catch (error) {
        console.error("Error fetching data:", error);
      } finally {
        setLoading(false);
      }
    }

    fetchData();
  }, [selectedYear, selectedMonth]);

  return (
    <div className="min-h-screen bg-gray-50 pb-20">
      {/* Header */}
      <header className="bg-white border-b border-gray-200 sticky top-0 z-10">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
          <div className="flex items-center space-x-3">
            <div className="w-8 h-8 bg-blue-600 rounded-lg flex items-center justify-center">
              <span className="text-white font-bold text-lg">R</span>
            </div>
            <h1 className="text-xl font-bold text-gray-900">Retail Analytics</h1>
          </div>

          <div className="flex items-center space-x-4">
            {/* Simple Refresh Button or User Profile could go here */}
          </div>
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">

        {/* Filters */}
        <div className="bg-white p-4 rounded-xl shadow-sm border border-gray-100 mb-8 flex flex-wrap items-center gap-4">
          <div className="flex items-center text-gray-500 mr-2">
            <Filter size={20} className="mr-2" />
            <span className="font-medium">Filters</span>
          </div>

          <select
            className="px-4 py-2 rounded-lg border border-gray-200 bg-gray-50 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
            value={selectedYear}
            onChange={(e) => setSelectedYear(e.target.value)}
          >
            <option value="All">All Years</option>
            {filters.years.map(y => <option key={y} value={y}>{y}</option>)}
          </select>

          <select
            className="px-4 py-2 rounded-lg border border-gray-200 bg-gray-50 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
            value={selectedMonth}
            onChange={(e) => setSelectedMonth(e.target.value)}
          >
            <option value="All">All Months</option>
            {filters.months.map(m => <option key={m} value={m}>{m}</option>)}
          </select>
        </div>

        {/* Dashboard Content */}
        {loading && !stats ? (
          <div className="flex flex-col space-y-4 animate-pulse">
            <div className="h-32 bg-gray-200 rounded-xl"></div>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div className="h-80 bg-gray-200 rounded-xl"></div>
              <div className="h-80 bg-gray-200 rounded-xl"></div>
            </div>
          </div>
        ) : (
          <>
            <KPICards data={stats} />

            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
              <RevenueChart data={revenueData} />
              <RetentionChart data={retentionData} />
            </div>
          </>
        )}
      </main>

      <footer className="text-center text-gray-400 text-sm py-8">
        © 2025 Retail Analytics Dashboard | Powered by Next.js & Python
      </footer>
    </div>
  );
}
