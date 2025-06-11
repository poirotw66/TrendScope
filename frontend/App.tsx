
import React from 'react';
import { HashRouter, Routes, Route } from 'react-router-dom';
import { MainLayout } from './components/layout/MainLayout';
import { DashboardPage } from './components/pages/DashboardPage';
import { DatabasePage } from './components/pages/DatabasePage';
import { ReportPage } from './components/pages/ReportPage';
import { ReportGeneratorPage } from './components/pages/ReportGeneratorPage'; // Added import
import { CrawlerManagementPage } from './components/pages/CrawlerManagementPage';
import { SystemSettingsPage } from './components/pages/SystemSettingsPage';
import { LogQueryPage } from './components/pages/LogQueryPage';
import { NotFoundPage } from './components/pages/NotFoundPage';

const App: React.FC = () => {
  return (
    <HashRouter>
      <MainLayout>
        <Routes>
          <Route path="/" element={<DashboardPage />} />
          <Route path="/database" element={<DatabasePage />} />
          <Route path="/reports" element={<ReportPage />} />
          <Route path="/report-generator" element={<ReportGeneratorPage />} /> {/* Added route */}
          <Route path="/crawlers" element={<CrawlerManagementPage />} />
          <Route path="/settings" element={<SystemSettingsPage />} />
          <Route path="/logs" element={<LogQueryPage />} />
          <Route path="*" element={<NotFoundPage />} />
        </Routes>
      </MainLayout>
    </HashRouter>
  );
};

export default App;
