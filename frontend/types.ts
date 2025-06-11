
import React from 'react';

export enum Language {
  EN = 'en',
  ZH_TW = 'zh-TW',
}

export enum Theme {
  LIGHT = 'light',
  DARK = 'dark',
}

export interface NavItem {
  path: string;
  labelKey: string;
  icon: (props: React.SVGProps<SVGSVGElement>) => React.ReactNode;
}

export interface User {
  name: string;
  avatarUrl?: string;
}

export interface AppState {
  user: User | null;
  isLoading: boolean;
  error: string | null;
  notifications: Notification[];
  pageTitle: string;
}

export interface AppContextType extends AppState {
  setUser: (user: User | null) => void;
  setLoading: (loading: boolean) => void;
  setError: (error: string | null) => void;
  addNotification: (notification: Omit<Notification, 'id' | 'read'>) => void;
  markNotificationAsRead: (id: string) => void;
  setPageTitle: (title: string) => void;
}

export interface ThemeState {
  theme: Theme;
}

export interface ThemeContextType extends ThemeState {
  toggleTheme: () => void;
}

export interface LanguageState {
  language: Language;
}

export interface LanguageContextType extends LanguageState {
  setLanguage: (language: Language) => void;
  t: (key: string, section?: string) => string;
}

export interface Notification {
  id: string;
  message: string;
  type: 'info' | 'warning' | 'error' | 'success';
  read: boolean;
  timestamp: Date;
}

// Data types for DatabasePage
export interface TrendData {
  id: string;
  conference: string;
  date: string;
  meeting: string;
  url: string;
  abstract: string;
  topic: string;
  other?: string;
}

// Data types for ReportPage
export enum ReportStatus {
  DRAFT = 'draft',
  PUBLISHED = 'published',
}
export interface Report {
  id: string;
  title: string;
  date: string;
  responsiblePerson: string;
  status: ReportStatus;
}

// Data types for CrawlerManagementPage
export enum CrawlerStatus {
  ENABLED = 'enabled',
  DISABLED = 'disabled',
  ERROR = 'error',
}
export interface Crawler {
  id: string;
  name: string;
  source: string;
  status: CrawlerStatus;
  lastRunTime: string;
}

// For Recharts
export interface ChartDataPoint {
  name: string;
  value: number;
}
