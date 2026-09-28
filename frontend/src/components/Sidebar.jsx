import React, { useState } from 'react';
import { NavLink } from 'react-router-dom';
import {
  LayoutDashboard, Map, BrainCircuit, FlaskConical,
  LineChart, Leaf, ChevronLeft, ChevronRight,
  Wifi, Sprout, Droplets
} from 'lucide-react';

const navItems = [
  { name:'Dashboard',  path:'/',          icon: LayoutDashboard, tag:'Overview' },
  { name:'My Fields',  path:'/fields',    icon: Map,             tag:'3 fields' },
  { name:'AI Advisor', path:'/advisor',   icon: BrainCircuit,    tag:'Smart' },
  { name:'Simulator',  path:'/simulator', icon: FlaskConical,    tag:'What-if' },
  { name:'Analytics',  path:'/analytics', icon: LineChart,       tag:'Reports' },
];

export default function Sidebar() {
  const [collapsed, setCollapsed] = useState(false);

  return (
    <aside
      className={`bg-sidebar fixed left-0 top-0 h-screen z-50 flex flex-col
                  transition-all duration-300 ease-in-out
                  ${collapsed ? 'w-[72px]' : 'w-[240px]'}`}
    >
      {/* ── Logo ────────────────────────── */}
      <div className="px-4 py-5 flex items-center justify-between border-b border-white/[.07]">
        <div className={`flex items-center gap-3 overflow-hidden ${collapsed ? 'justify-center w-full' : ''}`}>
          <div className="relative flex-shrink-0">
            <div className="w-9 h-9 rounded-[11px] flex items-center justify-center
                            bg-gradient-to-br from-green-400 to-emerald-600 anim-pulse-g">
              <Leaf className="w-5 h-5 text-white" />
            </div>
            {/* Ripple ring */}
            <span className="absolute inset-0 rounded-[11px] border-2 border-green-400/40 animate-ping pointer-events-none" />
          </div>
          {!collapsed && (
            <div className="anim-slide-left overflow-hidden">
              <p className="text-white font-black text-[15px] tracking-wide leading-none">CropDrop</p>
              <p className="text-green-400/80 text-[10px] font-medium tracking-widest uppercase mt-0.5">Smart Irrigation</p>
            </div>
          )}
        </div>
        {!collapsed && (
          <button onClick={() => setCollapsed(true)}
            className="w-6 h-6 rounded-lg flex items-center justify-center text-white/30
                       hover:text-white hover:bg-white/10 transition flex-shrink-0">
            <ChevronLeft className="w-3.5 h-3.5" />
          </button>
        )}
      </div>

      {/* ── Collapsed expand btn ─────────── */}
      {collapsed && (
        <button onClick={() => setCollapsed(false)}
          className="mx-auto mt-3 w-8 h-8 rounded-xl flex items-center justify-center
                     text-white/30 hover:text-white hover:bg-white/10 transition">
          <ChevronRight className="w-4 h-4" />
        </button>
      )}

      {/* ── Live pill ───────────────────── */}
      {!collapsed && (
        <div className="mx-3 mt-4 px-3 py-2 rounded-xl bg-green-500/10 border border-green-500/20
                        flex items-center gap-2">
          <Wifi className="w-3 h-3 text-green-400 flex-shrink-0" />
          <span className="text-green-400 text-[11px] font-semibold live-dot">Sensors active</span>
        </div>
      )}

      {/* ── Nav items ───────────────────── */}
      <nav className="flex-1 px-2 mt-4 space-y-0.5 overflow-y-auto">
        {navItems.map(item => {
          const Icon = item.icon;
          return (
            <NavLink
              key={item.path}
              to={item.path}
              end={item.path === '/'}
              className={({ isActive }) =>
                `nav-item group flex items-center gap-3 px-3 py-2.5 cursor-pointer relative
                 ${isActive ? 'active' : 'text-white/45 hover:text-white/80'}
                 ${collapsed ? 'justify-center' : ''}`
              }
            >
              {({ isActive }) => (
                <>
                  {isActive && !collapsed && (
                    <span className="absolute left-0 top-1/2 -translate-y-1/2 w-[3px] h-5
                                     bg-green-400 rounded-r-full" />
                  )}
                  <Icon className={`w-[18px] h-[18px] flex-shrink-0
                                   ${isActive ? 'text-white' : 'text-white/45 group-hover:text-white/80'}
                                   transition-colors`} />
                  {!collapsed && (
                    <div className="flex-1 min-w-0">
                      <p className="text-[13px] font-semibold leading-none">{item.name}</p>
                      {!isActive && (
                        <p className="text-[10px] text-white/30 mt-0.5">{item.tag}</p>
                      )}
                    </div>
                  )}
                </>
              )}
            </NavLink>
          );
        })}
      </nav>

      {/* ── Stats strip ─────────────────── */}
      {!collapsed && (
        <div className="mx-3 mb-3 p-3 rounded-2xl border border-white/[.07] bg-white/[.03]">
          <p className="text-white/30 text-[10px] font-bold uppercase tracking-widest mb-2">Today</p>
          <div className="flex justify-between">
            {[
              { icon: Droplets, val:'350 L', label:'Used' },
              { icon: Sprout,   val:'420 L', label:'Saved' },
            ].map(s => (
              <div key={s.label} className="text-center">
                <s.icon className="w-4 h-4 mx-auto text-green-400 mb-1" />
                <p className="text-white text-xs font-bold">{s.val}</p>
                <p className="text-white/30 text-[10px]">{s.label}</p>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* ── Footer ──────────────────────── */}
      {!collapsed && (
        <div className="px-4 py-4 border-t border-white/[.06] text-center">
          <p className="text-white/20 text-[10px] font-medium">🌾 Prototype · v1.0 · Phase 5</p>
        </div>
      )}
    </aside>
  );
}
