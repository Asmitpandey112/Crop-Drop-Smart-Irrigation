import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import AppLayout from './layouts/AppLayout';
import Dashboard from './pages/Dashboard';
import FieldsList from './pages/FieldsList';
import FieldDetails from './pages/FieldDetails';
import AIAdvisor from './pages/AIAdvisor';
import Simulator from './pages/Simulator';
import Analytics from './pages/Analytics';

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<AppLayout />}>
          <Route index element={<Dashboard />} />
          <Route path="fields" element={<FieldsList />} />
          <Route path="fields/:id" element={<FieldDetails />} />
          <Route path="advisor" element={<AIAdvisor />} />
          <Route path="simulator" element={<Simulator />} />
          <Route path="analytics" element={<Analytics />} />
        </Route>
      </Routes>
    </Router>
  );
}

export default App;
