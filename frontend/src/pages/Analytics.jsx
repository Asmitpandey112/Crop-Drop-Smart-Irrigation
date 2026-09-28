import React from 'react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, AreaChart, Area, Legend } from 'recharts';
import { Droplets, Sprout, TrendingDown, Activity, LineChart as ChartIcon } from 'lucide-react';
import { mockMoistureHistory } from '../data/mockData';

const weeklyData = [
  { d: 'Mon', u: 300, a: 120 }, { d: 'Tue', u: 0, a: 450 }, { d: 'Wed', u: 250, a: 50  },
  { d: 'Thu', u: 400, a: 0   }, { d: 'Fri', u: 0, a: 380 }, { d: 'Sat', u: 350, a: 100 }, { d: 'Sun', u: 0, a: 420 },
];

const totalU = weeklyData.reduce((s, d) => s + d.u, 0);
const totalA = weeklyData.reduce((s, d) => s + d.a, 0);
const pct = Math.round((totalA / (totalU + totalA)) * 100);

const CustomBarTT = ({ active, payload, label }) => {
  if (active && payload?.length) return (
    <div className="card-glass p-4 border-none shadow-deep min-w-[160px]">
      <p className="text-gray-400 font-bold text-xs uppercase mb-3 text-center">{label}</p>
      {payload.map(p => (
        <div key={p.name} className="flex justify-between items-center mb-1 text-sm font-bold">
          <span style={{ color: p.color }}>{p.name}</span>
          <span>{p.value} L</span>
        </div>
      ))}
    </div>
  );
  return null;
};

const CustomAreaTT = ({ active, payload, label }) => {
  if (active && payload?.length) return (
    <div className="card-glass p-3 border-none shadow-deep text-center min-w-[100px]">
      <p className="text-gray-400 font-bold text-xs uppercase mb-1">{label}</p>
      <p className="text-water-blue font-black text-xl">{payload[0].value}%</p>
    </div>
  );
  return null;
};

const StatCard = ({ icon: Icon, l, v, suf, c, bg, d }) => (
  <div className={`card p-6 text-center anim-fade-up ${d} relative overflow-hidden group`}>
    <div className={`absolute -right-6 -top-6 w-24 h-24 rounded-full ${bg} opacity-20 group-hover:scale-150 transition-transform duration-500`} />
    <div className={`w-12 h-12 mx-auto rounded-full flex items-center justify-center mb-4 ${bg} text-white shadow-soft relative z-10`}>
      <Icon className="w-6 h-6" />
    </div>
    <p className="text-4xl font-black relative z-10 text-gray-800">{v}<span className="text-xl text-gray-400 ml-1">{suf}</span></p>
    <p className="text-xs font-bold text-gray-400 uppercase tracking-widest mt-2 relative z-10">{l}</p>
  </div>
);

export default function Analytics() {
  return (
    <div className="max-w-[1100px] mx-auto space-y-8 pb-10">
      
      {/* ── Header ── */}
      <div className="text-center anim-fade-up d0 mb-10">
        <h1 className="text-4xl font-black text-gray-900 mb-2 flex justify-center items-center gap-3">
          <ChartIcon className="w-8 h-8 text-purple-600" /> Executive Analytics
        </h1>
        <p className="text-gray-500 font-medium">Platform impact and resource savings report.</p>
      </div>

      {/* ── KPIs ── */}
      <div className="grid grid-cols-2 lg:grid-cols-4 gap-5">
        <StatCard icon={Droplets}     l="Used"        v={totalU} suf="L" bg="bg-blue-500"   d="d1" />
        <StatCard icon={Sprout}       l="Saved"       v={totalA} suf="L" bg="bg-green-500"  d="d2" />
        <StatCard icon={TrendingDown} l="Efficiency"  v={pct}    suf="%" bg="bg-emerald-500" d="d3" />
        <StatCard icon={Activity}     l="Decisions"   v="24"     suf=""  bg="bg-purple-500"  d="d4" />
      </div>

      {/* ── Charts ── */}
      <div className="grid grid-cols-1 xl:grid-cols-2 gap-6 anim-fade-up d5">
        
        <div className="card p-8">
          <div className="mb-8">
            <h2 className="text-xl font-black text-gray-900">Resource Impact</h2>
            <p className="text-sm text-gray-400">Weekly breakdown of water used vs saved</p>
          </div>
          <div className="h-[300px]">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={weeklyData} margin={{ top:0, right:0, left:-20, bottom:0 }} barSize={32}>
                <CartesianGrid strokeDasharray="4 4" vertical={false} stroke="#f1f5f9" />
                <XAxis dataKey="d" axisLine={false} tickLine={false} tick={{fill:'#94a3b8', fontSize:12, fontWeight:600}} dy={10} />
                <YAxis axisLine={false} tickLine={false} tick={{fill:'#94a3b8', fontSize:12, fontWeight:600}} />
                <Tooltip content={<CustomBarTT />} cursor={{ fill:'#f8fafc' }} />
                <Legend wrapperStyle={{ paddingTop: '20px', fontSize: '12px', fontWeight: 700, color: '#64748b' }} />
                <Bar dataKey="u" name="Used" fill="#0288D1" radius={[6,6,0,0]} />
                <Bar dataKey="a" name="Saved" fill="#22c55e" radius={[6,6,0,0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>

        <div className="card p-8">
          <div className="mb-8">
            <h2 className="text-xl font-black text-gray-900">Aggregate Moisture</h2>
            <p className="text-sm text-gray-400">Farm-wide average soil moisture trend</p>
          </div>
          <div className="h-[300px]">
            <ResponsiveContainer width="100%" height="100%">
              <AreaChart data={mockMoistureHistory} margin={{ top:20, right:0, left:-20, bottom:0 }}>
                <defs>
                  <linearGradient id="areaGrad" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="0%" stopColor="#0288D1" stopOpacity={0.4} />
                    <stop offset="100%" stopColor="#0288D1" stopOpacity={0} />
                  </linearGradient>
                </defs>
                <CartesianGrid strokeDasharray="4 4" vertical={false} stroke="#f1f5f9" />
                <XAxis dataKey="time" axisLine={false} tickLine={false} tick={{fill:'#94a3b8', fontSize:12, fontWeight:600}} dy={10} />
                <YAxis domain={[0,100]} axisLine={false} tickLine={false} tick={{fill:'#94a3b8', fontSize:12, fontWeight:600}} />
                <Tooltip content={<CustomAreaTT />} cursor={{ stroke:'#e2e8f0', strokeWidth:2, strokeDasharray:'4 4' }} />
                <Area type="monotone" dataKey="moisture" stroke="#0288D1" strokeWidth={4} fill="url(#areaGrad)" 
                      activeDot={{ r:8, fill:'#fff', stroke:'#0288D1', strokeWidth:3 }} />
              </AreaChart>
            </ResponsiveContainer>
          </div>
        </div>

      </div>
    </div>
  );
}
