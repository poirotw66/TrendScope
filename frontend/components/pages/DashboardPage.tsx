import React, { useEffect, useState } from 'react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, PieChart, Pie, Cell } from 'recharts';
import { Card } from '../ui/Card';
import { Button } from '../ui/Button';
import { useAppContext } from '../../hooks/useAppContext';
import { useLanguage } from '../../hooks/useLanguage';
import { getMockChartData, getMockDashboardStats } from '../../services/mockDataService';
import { ChartDataPoint } from '../../types';
import { PlusCircleIcon, UploadIcon, ExclamationTriangleIcon, DocumentReportIcon, CogIcon } from '../../constants'; // Added more icons for variety

const OverviewCard: React.FC<{ title: string; value: string | number; icon: React.ReactNode; colorClass?: string, iconBgClass?: string }> = ({ title, value, icon, colorClass = "text-primary-500 dark:text-primary-400", iconBgClass = "bg-primary-500/10 dark:bg-primary-400/10" }) => (
  <Card className="flex-1 min-w-[200px] hover:shadow-xl transition-shadow duration-200">
    <div className="flex items-center space-x-4">
      <div className={`p-3 rounded-xl ${iconBgClass}`}>{icon}</div>
      <div>
        <p className="text-sm text-neutral-500 dark:text-neutral-400">{title}</p>
        <p className="text-2xl font-semibold text-neutral-800 dark:text-neutral-100">{value}</p>
      </div>
    </div>
  </Card>
);


export const DashboardPage: React.FC = () => {
  const { setPageTitle } = useAppContext();
  const { t, language } = useLanguage(); // Added language for dynamic chart labels
  
  const [stats, setStats] = useState(getMockDashboardStats());
  const [taskStatusData, setTaskStatusData] = useState<ChartDataPoint[]>([]);
  const [summaryTrendData, setSummaryTrendData] = useState<ChartDataPoint[]>([]);

  useEffect(() => {
    setPageTitle(t('dashboard', 'sidebar'));
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [setPageTitle, t, language]); // Add language dependency for re-rendering charts if labels change

  useEffect(() => {
     setTaskStatusData([
      { name: t('completed', 'dashboard') || 'Completed', value: Math.floor(Math.random() * 100) + 20 },
      { name: t('inProgress', 'dashboard') || 'In Progress', value: Math.floor(Math.random() * 50) + 10 },
      { name: t('pending', 'dashboard') || 'Pending', value: Math.floor(Math.random() * 30) + 5 },
      { name: t('failed', 'dashboard') || 'Failed', value: Math.floor(Math.random() * 10) + 2 },
    ]);
    setSummaryTrendData(getMockChartData(7, t('day', 'dashboard') || 'Day'));
  }, [t, language]); // update chart data when language changes
  
  const PIE_COLORS = ['#0ea5e9', '#10b981', '#f59e0b', '#ef4444']; // primary, green, amber, red

  return (
    <div className="space-y-6 md:space-y-8">
      <h2 className="text-2xl md:text-3xl font-semibold text-neutral-700 dark:text-neutral-200">{t('overview', 'dashboard')}</h2>
      
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
        <OverviewCard title={t('currentTasks', 'dashboard')} value={stats.currentTasks} icon={<PlusCircleIcon className="w-6 h-6 text-sky-500" />} colorClass="text-sky-500" iconBgClass="bg-sky-500/10 dark:bg-sky-400/10" />
        <OverviewCard title={t('summariesToday', 'dashboard')} value={stats.summariesToday} icon={<DocumentReportIcon className="w-6 h-6 text-emerald-500" />} colorClass="text-emerald-500" iconBgClass="bg-emerald-500/10 dark:bg-emerald-400/10" />
        <OverviewCard title={t('pendingReports', 'dashboard')} value={stats.pendingReports} icon={<CogIcon className="w-6 h-6 text-amber-500" />} colorClass="text-amber-500" iconBgClass="bg-amber-500/10 dark:bg-amber-400/10" />
        <OverviewCard title={t('systemAlerts', 'dashboard')} value={stats.systemAlerts} icon={<ExclamationTriangleIcon className="w-6 h-6 text-red-500" />} colorClass="text-red-500" iconBgClass="bg-red-500/10 dark:bg-red-400/10" />
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-5 gap-6 md:gap-8">
        <Card title={t('taskStatus', 'dashboard')} className="lg:col-span-2">
          <ResponsiveContainer width="100%" height={300}>
            <PieChart>
              <Pie data={taskStatusData} dataKey="value" nameKey="name" cx="50%" cy="50%" outerRadius={100} labelLine={false}
                 label={({ cx, cy, midAngle, innerRadius, outerRadius, percent, index }) => {
                    const radius = innerRadius + (outerRadius - innerRadius) * 0.5;
                    const x = cx + radius * Math.cos(-midAngle * (Math.PI / 180));
                    const y = cy + radius * Math.sin(-midAngle * (Math.PI / 180));
                    return (
                      <text x={x} y={y} fill="white" textAnchor={x > cx ? 'start' : 'end'} dominantBaseline="central" className="text-xs font-medium">
                        {`${(percent * 100).toFixed(0)}%`}
                      </text>
                    );
                  }}
              >
                 {taskStatusData.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={PIE_COLORS[index % PIE_COLORS.length]} stroke="none" />
                  ))}
              </Pie>
              <Tooltip
                contentStyle={{
                  backgroundColor: 'rgba(255, 255, 255, 0.9)',
                  backdropFilter: 'blur(5px)',
                  borderRadius: '0.75rem', // rounded-xl
                  borderColor: 'rgba(200,200,200,0.3)',
                  boxShadow: '0 4px 6px -1px rgba(0,0,0,0.1), 0 2px 4px -1px rgba(0,0,0,0.06)'
                }}
                labelStyle={{ color: '#334155', fontWeight: '500' }} // neutral-700
                itemStyle={{ color: '#475569' }} // neutral-600
              />
              <Legend wrapperStyle={{fontSize: "0.875rem", paddingTop: "10px"}} />
            </PieChart>
          </ResponsiveContainer>
        </Card>
        <Card title={t('summaryTrend', 'dashboard')} className="lg:col-span-3">
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={summaryTrendData} margin={{ top: 5, right: 0, left: -20, bottom: 5 }}>
              <CartesianGrid strokeDasharray="3 3" className="stroke-neutral-200 dark:stroke-neutral-700/50" />
              <XAxis dataKey="name" className="text-xs fill-neutral-600 dark:fill-neutral-400" />
              <YAxis className="text-xs fill-neutral-600 dark:fill-neutral-400" />
              <Tooltip
                contentStyle={{
                  backgroundColor: 'rgba(255, 255, 255, 0.9)',
                  backdropFilter: 'blur(5px)',
                  borderRadius: '0.75rem',
                  borderColor: 'rgba(200,200,200,0.3)',
                   boxShadow: '0 4px 6px -1px rgba(0,0,0,0.1), 0 2px 4px -1px rgba(0,0,0,0.06)'
                }}
                labelStyle={{ color: '#334155', fontWeight: '500' }}
                itemStyle={{ color: '#0ea5e9' }} // primary-500
              />
              <Legend wrapperStyle={{fontSize: "0.875rem"}}/>
              <Bar dataKey="value" fill="url(#colorValue)" name={t('summariesToday', 'dashboard')} barSize={30} radius={[4, 4, 0, 0]} />
               <defs>
                <linearGradient id="colorValue" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="5%" stopColor="#0ea5e9" stopOpacity={0.8}/>
                  <stop offset="95%" stopColor="#0ea5e9" stopOpacity={0.4}/>
                </linearGradient>
              </defs>
            </BarChart>
          </ResponsiveContainer>
        </Card>
      </div>
      
      <Card title={t('quickAccess', 'dashboard')}>
        <div className="flex flex-col sm:flex-row space-y-3 sm:space-y-0 sm:space-x-4">
          <Button variant="primary" size="md" leftIcon={<PlusCircleIcon className="w-5 h-5" />}>
            {t('createTask', 'dashboard')}
          </Button>
          <Button variant="secondary" size="md" leftIcon={<UploadIcon className="w-5 h-5" />}>
            {t('uploadFile', 'dashboard')}
          </Button>
        </div>
      </Card>
    </div>
  );
};

// Add translations for new chart labels if they don't exist
// dashboard: {
//   ...
//   completed: "Completed",
//   inProgress: "In Progress",
//   pending: "Pending",
//   failed: "Failed",
//   day: "Day"
// }
//
// dashboard: {
//    ...
//   completed: "已完成",
//   inProgress: "進行中",
//   pending: "待處理",
//   failed: "失敗",
//   day: "日"
// }
// This should be done in LanguageContext.tsx but added here for completeness of thought.
// I will ensure these keys are added to LanguageContext.tsx
