import React, { useState, useEffect } from 'react';
import { Box, Button, Card, CardContent, CircularProgress, FormControl, Grid, InputLabel, MenuItem, Select, Switch, TextField, Typography, Divider, Chip, Alert, FormControlLabel } from '@mui/material';
import apiService, { ScraperRequest, ScraperResponse, ScraperResult } from '../services/api';

/**
 * 爬蟲控制面板組件
 * 提供用戶介面來控制爬蟲和查看結果
 */
const ScraperDashboard: React.FC = () => {
  // 爬蟲列表狀態
  const [scrapers, setScrapers] = useState<{ id: string; name: string; description: string }[]>([]);
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);
  
  // 表單狀態
  const [selectedScraper, setSelectedScraper] = useState<string>('');
  const [headless, setHeadless] = useState<boolean>(true);
  const [waitTime, setWaitTime] = useState<number>(30);
  const [useBigQuery, setUseBigQuery] = useState<boolean>(true);
  
  // 任務狀態
  const [taskId, setTaskId] = useState<string | null>(null);
  const [taskStatus, setTaskStatus] = useState<ScraperResult | null>(null);
  const [pollingInterval, setPollingInterval] = useState<NodeJS.Timeout | null>(null);
  
  // 初始化：獲取可用爬蟲列表
  useEffect(() => {
    const fetchScrapers = async () => {
      try {
        setLoading(true);
        const availableScrapers = await apiService.getAvailableScrapers();
        setScrapers(availableScrapers);
        if (availableScrapers.length > 0) {
          setSelectedScraper(availableScrapers[0].id);
        }
      } catch (err) {
        setError('無法獲取爬蟲列表，請確保 API 服務正在運行');
        console.error('獲取爬蟲列表錯誤:', err);
      } finally {
        setLoading(false);
      }
    };

    fetchScrapers();
  }, []);
  
  // 清理輪詢
  useEffect(() => {
    return () => {
      if (pollingInterval) {
        clearInterval(pollingInterval);
      }
    };
  }, [pollingInterval]);
  
  // 監控任務狀態
  const startPolling = (taskId: string) => {
    // 先清除舊的輪詢
    if (pollingInterval) {
      clearInterval(pollingInterval);
    }
    
    // 開始新的輪詢
    const interval = setInterval(async () => {
      try {
        const result = await apiService.getScraperStatus(taskId);
        setTaskStatus(result);
        
        // 如果任務完成或失敗，停止輪詢
        if (result.status === 'completed' || result.status === 'failed') {
          if (pollingInterval) {
            clearInterval(pollingInterval);
            setPollingInterval(null);
          }
        }
      } catch (err) {
        console.error('獲取任務狀態錯誤:', err);
        if (pollingInterval) {
          clearInterval(pollingInterval);
          setPollingInterval(null);
        }
      }
    }, 3000); // 每 3 秒輪詢一次
    
    setPollingInterval(interval);
  };
  
  // 運行爬蟲
  const handleRunScraper = async () => {
    try {
      setLoading(true);
      setError(null);
      setTaskId(null);
      setTaskStatus(null);
      
      // 準備請求
      const request: ScraperRequest = {
        scraper_type: selectedScraper,
        headless,
        wait_time: waitTime,
        use_bigquery: useBigQuery
      };
      
      // 呼叫 API
      const response = await apiService.runScraper(request);
      setTaskId(response.task_id);
      
      // 開始輪詢任務狀態
      startPolling(response.task_id);
    } catch (err: any) {
      setError(`運行爬蟲失敗: ${err.message || JSON.stringify(err)}`);
      console.error('運行爬蟲錯誤:', err);
    } finally {
      setLoading(false);
    }
  };
  
  // 渲染任務狀態
  const renderTaskStatus = () => {
    if (!taskId || !taskStatus) return null;
    
    const statusColors: Record<string, string> = {
      pending: 'warning',
      running: 'info',
      completed: 'success',
      failed: 'error'
    };
    
    return (
      <Card variant="outlined" sx={{ mt: 3 }}>
        <CardContent>
          <Box display="flex" justifyContent="space-between" alignItems="center" mb={2}>
            <Typography variant="h6">任務狀態</Typography>
            <Chip 
              label={taskStatus.status.toUpperCase()} 
              color={statusColors[taskStatus.status] as any} 
              variant="outlined" 
            />
          </Box>
          
          <Divider sx={{ mb: 2 }} />
          
          <Grid container spacing={2}>
            <Grid item xs={12}>
              <Typography variant="body2" color="textSecondary">任務 ID:</Typography>
              <Typography variant="body1">{taskId}</Typography>
            </Grid>
            
            {taskStatus.message && (
              <Grid item xs={12}>
                <Typography variant="body2" color="textSecondary">訊息:</Typography>
                <Typography variant="body1">{taskStatus.message}</Typography>
              </Grid>
            )}
            
            {taskStatus.file_path && (
              <Grid item xs={12}>
                <Typography variant="body2" color="textSecondary">輸出檔案:</Typography>
                <Typography variant="body1">{taskStatus.file_path}</Typography>
              </Grid>
            )}
            
            {taskStatus.status === 'running' && (
              <Grid item xs={12} sx={{ textAlign: 'center', my: 2 }}>
                <CircularProgress size={30} />
                <Typography variant="body2" color="textSecondary" sx={{ mt: 1 }}>
                  爬蟲正在執行中，請稍後...
                </Typography>
              </Grid>
            )}
            
            {taskStatus.status === 'completed' && taskStatus.data && (
              <Grid item xs={12}>
                <Typography variant="body2" color="textSecondary">爬取結果摘要:</Typography>
                <Box sx={{ mt: 1, p: 2, bgcolor: '#f5f5f5', borderRadius: 1, maxHeight: 300, overflow: 'auto' }}>
                  <Typography variant="body2">共爬取 {taskStatus.data.length} 筆資料</Typography>
                  {taskStatus.data.slice(0, 5).map((item: any, index: number) => (
                    <Box key={index} sx={{ mt: 1, p: 1, bgcolor: '#fff', borderRadius: 1 }}>
                      <Typography variant="body2" fontWeight="bold">
                        {item['會議名稱'] || item.name || `項目 ${index + 1}`}
                      </Typography>
                      {item['會議連結'] && (
                        <Typography variant="body2" component="div" sx={{ wordBreak: 'break-all' }}>
                          連結: {item['會議連結']}
                        </Typography>
                      )}
                    </Box>
                  ))}
                  {taskStatus.data.length > 5 && (
                    <Typography variant="body2" sx={{ mt: 1, fontStyle: 'italic' }}>
                      ...還有 {taskStatus.data.length - 5} 筆資料
                    </Typography>
                  )}
                </Box>
              </Grid>
            )}
          </Grid>
        </CardContent>
      </Card>
    );
  };
  
  return (
    <Box sx={{ p: 3 }}>
      <Typography variant="h4" gutterBottom>爬蟲控制面板</Typography>
      
      {error && (
        <Alert severity="error" sx={{ mb: 3 }}>{error}</Alert>
      )}
      
      <Card variant="outlined">
        <CardContent>
          <Grid container spacing={3}>
            <Grid item xs={12} md={6}>
              <FormControl fullWidth disabled={loading}>
                <InputLabel>選擇爬蟲</InputLabel>
                <Select
                  value={selectedScraper}
                  onChange={(e) => setSelectedScraper(e.target.value as string)}
                  label="選擇爬蟲"
                >
                  {scrapers.map((scraper) => (
                    <MenuItem key={scraper.id} value={scraper.id}>
                      {scraper.name}
                    </MenuItem>
                  ))}
                </Select>
              </FormControl>
              
              {scrapers.find(s => s.id === selectedScraper)?.description && (
                <Typography variant="body2" color="textSecondary" sx={{ mt: 1 }}>
                  {scrapers.find(s => s.id === selectedScraper)?.description}
                </Typography>
              )}
            </Grid>
            
            <Grid item xs={12} md={6}>
              <Grid container spacing={2}>
                <Grid item xs={12}>
                  <FormControlLabel
                    control={
                      <Switch
                        checked={headless}
                        onChange={(e) => setHeadless(e.target.checked)}
                        disabled={loading}
                      />
                    }
                    label="無頭模式（不顯示瀏覽器）"
                  />
                </Grid>
                
                <Grid item xs={12}>
                  <TextField
                    label="等待時間（秒）"
                    type="number"
                    value={waitTime}
                    onChange={(e) => setWaitTime(parseInt(e.target.value) || 30)}
                    fullWidth
                    disabled={loading}
                    InputProps={{ inputProps: { min: 5, max: 120 } }}
                    helperText="等待頁面元素的最大時間"
                  />
                </Grid>
                
                <Grid item xs={12}>
                  <FormControlLabel
                    control={
                      <Switch
                        checked={useBigQuery}
                        onChange={(e) => setUseBigQuery(e.target.checked)}
                        disabled={loading}
                      />
                    }
                    label="將結果上傳到 BigQuery"
                  />
                </Grid>
              </Grid>
            </Grid>
            
            <Grid item xs={12} sx={{ textAlign: 'center' }}>
              <Button
                variant="contained"
                color="primary"
                onClick={handleRunScraper}
                disabled={loading || !selectedScraper}
                sx={{ minWidth: 150 }}
                startIcon={loading && <CircularProgress size={20} color="inherit" />}
              >
                {loading ? '處理中...' : '執行爬蟲'}
              </Button>
            </Grid>
          </Grid>
        </CardContent>
      </Card>
      
      {renderTaskStatus()}
    </Box>
  );
};

export default ScraperDashboard;
