
import React from 'react';
import { HashRouter, Routes, Route } from 'react-router-dom';
import { MainLayout } from './components/layout/MainLayout';
import { DashboardPage } from './components/pages/DashboardPage';
import { DatabasePage } from './components/pages/DatabasePage';
import { PPTUploadPage } from './components/pages/PPTUploadPage';
import { ReportPage } from './components/pages/ReportPage';
import { ReportGeneratorPage } from './components/pages/ReportGeneratorPage'; // Added import
import { BatchReportsPage } from './components/pages/BatchReportsPage';
import { BatchReportTasksPage } from './components/pages/BatchReportTasksPage';

import { CrawlerManagementPage } from './components/pages/CrawlerManagementPage';

import { NotFoundPage } from './components/pages/NotFoundPage';

const App: React.FC = () => {
  return (
    <HashRouter>
      <MainLayout>
        <Routes>
          <Route path="/" element={<DashboardPage />} />
          <Route path="/database" element={<DatabasePage />} />
          <Route path="/ppt-upload" element={<PPTUploadPage />} />
          <Route path="/reports" element={<ReportPage />} />
          <Route path="/report-generator" element={<ReportGeneratorPage />} /> {/* Added route */}
          <Route path="/batch-reports" element={<BatchReportsPage />} />
          <Route path="/batch-report-tasks" element={<BatchReportTasksPage />} />

          <Route path="/crawlers" element={<CrawlerManagementPage />} />

          <Route path="*" element={<NotFoundPage />} />
        </Routes>
      </MainLayout>
    </HashRouter>
  );
};

export default App;
