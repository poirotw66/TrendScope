import React, { useState, useEffect } from 'react';
import {
  Box,
  Button,
  Card,
  CardContent,
  CircularProgress,
  FormControl,
  Grid,
  InputLabel,
  MenuItem,
  Select,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  TablePagination,
  TextField,
  Typography,
  Chip,
  Paper,
  Link,
  Alert
} from '@mui/material';
import apiService, { Session } from '../services/api';

/**
 * 會議資料展示組件
 * 顯示從 BigQuery 獲取的會議資料
 */
const SessionsViewer: React.FC = () => {
  // 資料狀態
  const [sessions, setSessions] = useState<Session[]>([]);
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);
  
  // 過濾和分頁狀態
  const [source, setSource] = useState<string>('');
  const [sources, setSources] = useState<string[]>([]);
  const [page, setPage] = useState<number>(0);
  const [rowsPerPage, setRowsPerPage] = useState<number>(10);
  
  // 初始化：獲取會議資料
  useEffect(() => {
    const fetchSessions = async () => {
      try {
        setLoading(true);
        setError(null);
        
        const data = await apiService.getSessions(source || undefined);
        setSessions(data);
        
        // 收集所有唯一的來源
        const uniqueSources = Array.from(new Set(data.map(session => session.source)));
        setSources(uniqueSources);
      } catch (err: any) {
        setError(`無法獲取會議資料: ${err.message || JSON.stringify(err)}`);
        console.error('獲取會議資料錯誤:', err);
      } finally {
        setLoading(false);
      }
    };

    fetchSessions();
  }, [source]);
  
  // 處理分頁變更
  const handleChangePage = (event: unknown, newPage: number) => {
    setPage(newPage);
  };

  const handleChangeRowsPerPage = (event: React.ChangeEvent<HTMLInputElement>) => {
    setRowsPerPage(parseInt(event.target.value, 10));
    setPage(0);
  };
  
  // 渲染會議資料表格
  const renderSessionsTable = () => {
    if (loading) {
      return (
        <Box sx={{ display: 'flex', justifyContent: 'center', my: 4 }}>
          <CircularProgress />
        </Box>
      );
    }
    
    if (error) {
      return (
        <Alert severity="error" sx={{ my: 2 }}>{error}</Alert>
      );
    }
    
    if (sessions.length === 0) {
      return (
        <Alert severity="info" sx={{ my: 2 }}>
          沒有找到符合條件的會議資料。{source && `請嘗試更改過濾條件或確保已有 "${source}" 的資料上傳到 BigQuery。`}
        </Alert>
      );
    }
    
    return (
      <Paper sx={{ width: '100%', mb: 2 }}>
        <TableContainer>
          <Table aria-label="會議資料表格">
            <TableHead>
              <TableRow>
                <TableCell>會議名稱</TableCell>
                <TableCell>來源</TableCell>
                <TableCell>標籤</TableCell>
                <TableCell>地點</TableCell>
                <TableCell>日期</TableCell>
                <TableCell>操作</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {sessions
                .slice(page * rowsPerPage, page * rowsPerPage + rowsPerPage)
                .map((session) => (
                  <TableRow key={session.id} hover>
                    <TableCell>
                      <Typography variant="body2" fontWeight="medium">
                        {session.name}
                      </Typography>
                      {session.description && (
                        <Typography variant="caption" color="textSecondary" sx={{ display: 'block', mt: 0.5 }}>
                          {session.description.length > 100 
                            ? `${session.description.substring(0, 100)}...` 
                            : session.description}
                        </Typography>
                      )}
                    </TableCell>
                    <TableCell>{session.source}</TableCell>
                    <TableCell>
                      {session.tags && session.tags.length > 0 ? (
                        <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 0.5 }}>
                          {session.tags.slice(0, 3).map((tag, index) => (
                            <Chip key={index} label={tag} size="small" />
                          ))}
                          {session.tags.length > 3 && (
                            <Chip label={`+${session.tags.length - 3}`} size="small" variant="outlined" />
                          )}
                        </Box>
                      ) : (
                        <Typography variant="caption" color="textSecondary">無標籤</Typography>
                      )}
                    </TableCell>
                    <TableCell>{session.location || '-'}</TableCell>
                    <TableCell>
                      {session.start_date ? (
                        <Typography variant="body2">
                          {new Date(session.start_date).toLocaleDateString()}
                        </Typography>
                      ) : '-'}
                    </TableCell>
                    <TableCell>
                      {session.url ? (
                        <Link href={session.url} target="_blank" rel="noopener">
                          查看原始頁面
                        </Link>
                      ) : '-'}
                    </TableCell>
                  </TableRow>
                ))}
            </TableBody>
          </Table>
        </TableContainer>
        <TablePagination
          rowsPerPageOptions={[5, 10, 25, 50]}
          component="div"
          count={sessions.length}
          rowsPerPage={rowsPerPage}
          page={page}
          onPageChange={handleChangePage}
          onRowsPerPageChange={handleChangeRowsPerPage}
          labelRowsPerPage="每頁行數:"
        />
      </Paper>
    );
  };
  
  return (
    <Box sx={{ p: 3 }}>
      <Typography variant="h4" gutterBottom>會議資料查看器</Typography>
      <Typography variant="body1" paragraph>
        此頁面顯示從 BigQuery 獲取的會議資料，您可以按來源進行過濾。
      </Typography>
      
      <Card variant="outlined" sx={{ mb: 3 }}>
        <CardContent>
          <Grid container spacing={2} alignItems="center">
            <Grid item xs={12} sm={6} md={4}>
              <FormControl fullWidth>
                <InputLabel>按來源過濾</InputLabel>
                <Select
                  value={source}
                  onChange={(e) => {
                    setSource(e.target.value as string);
                    setPage(0);
                  }}
                  label="按來源過濾"
                  displayEmpty
                >
                  <MenuItem value="">所有來源</MenuItem>
                  {sources.map((src) => (
                    <MenuItem key={src} value={src}>{src}</MenuItem>
                  ))}
                </Select>
              </FormControl>
            </Grid>
            
            <Grid item xs={12} sm={6} md={2}>
              <Button 
                variant="outlined"
                onClick={() => {
                  setSource('');
                  setPage(0);
                }}
                fullWidth
              >
                重置過濾
              </Button>
            </Grid>
            
            <Grid item xs={12} md={6}>
              <Box sx={{ display: 'flex', justifyContent: { xs: 'flex-start', md: 'flex-end' } }}>
                <Typography variant="body2" color="textSecondary">
                  顯示 {sessions.length} 個會議資料
                  {source && ` (來源: ${source})`}
                </Typography>
              </Box>
            </Grid>
          </Grid>
        </CardContent>
      </Card>
      
      {renderSessionsTable()}
    </Box>
  );
};

export default SessionsViewer;
