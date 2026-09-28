import React from 'react';
import { Outlet } from 'react-router-dom';
import Sidebar from '../components/Sidebar';

export default function AppLayout() {
  return (
    <div className="flex min-h-screen" style={{ background:'#f0f2f0' }}>
      <Sidebar />
      <main className="flex-1 ml-[240px] transition-all duration-300">
        <div className="max-w-[1280px] mx-auto p-7">
          <Outlet />
        </div>
      </main>
    </div>
  );
}
