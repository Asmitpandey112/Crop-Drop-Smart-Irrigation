import React, { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, ReferenceLine } from 'recharts';
import { Droplets, Thermometer, CloudRain, Activity, ChevronLeft, MapPin } from 'lucide-react';
import { fetchFieldDetails, fetchFieldReadings } from '../services/api';

const S = {
  IRRIGATE:      { label:'Irrigate Now', badge:'badge-red',    light:'text-red-600 bg-red-50' },
  WAIT_FOR_RAIN: { label:'Rain Coming',  badge:'badge-blue',   light:'text-blue-600 bg-blue-50' },
  GOOD:          { label:'Good',         badge:'badge-green',  light:'text-green-600 bg-green-50' },
  NO_IRRIGATION: { label:'No Action',    badge:'badge-green',  light:'text-green-600 bg-green-50' },
  MONITOR:       { label:'Monitor',      badge:'badge-yellow', light:'text-amber-600 bg-amber-50' },
};

const CustomTooltip = ({ active, payload, label }) => {
  if (active && payload?.length) return (
    <div className="card-glass p-3 shadow-deep min-w-[120px] text-center border-none">
      <p className="text-gray-400 font-bold text-xs uppercase mb-1">{label}</p>
      <p className="text-water-blue font-black text-xl">{payload[0].value}%</p>
    </div>
  );
  return null;
};

export default function FieldDetails() {
  const { id } = useParams();
  const [f, setF] = useState(null);
  const [history, setHistory] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    Promise.all([fetchFieldDetails(id), fetchFieldReadings(id)])
      .then(([fData, hData]) => { setF(fData); setHistory(hData); })
      .catch(console.error)
      .finally(() => setLoading(false));
  }, [id]);

  if (loading) return (
    <div className="space-y-6">
      <div className="h-48 shimmer" />
      <div className="grid grid-cols-4 gap-4">{[1,2,3,4].map(i=><div key={i} className="h-32 shimmer"/>)}</div>
      <div className="h-80 shimmer" />
    </div>
  );
  if (!f) return <div className="card p-10 text-center font-bold text-red-500">Field not found.</div>;

  const st = S[f.status] || S.MONITOR;
  const m = f.soil_moisture ?? 0;
  const barCol = m < 35 ? '#ef4444' : m < 60 ? '#f59e0b' : '#22c55e';

  return (
    <div className="space-y-6 max-w-[1000px] mx-auto pb-10">
      
      {/* ── Breadcrumb ── */}
      <Link to="/fields" className="inline-flex items-center gap-1.5 text-xs font-bold text-gray-500 hover:text-primary-green anim-fade-up d0 transition-colors">
        <ChevronLeft className="w-4 h-4" /> Back to My Fields
      </Link>

      {/* ── Hero Presentation Banner ── */}
      <div className="card-dark p-8 relative overflow-hidden anim-fade-up d1 group">
        <div className="absolute right-0 top-0 bottom-0 w-1/2 bg-gradient-to-l from-green-500/10 to-transparent pointer-events-none" />
        <div className="absolute -bottom-24 -right-24 w-64 h-64 rounded-full bg-blue-500/10 blur-3xl group-hover:bg-blue-500/20 transition-all duration-700 pointer-events-none" />
        
        <div className="relative z-10 flex flex-col md:flex-row md:items-center justify-between gap-6">
          <div>
            <div className="inline-flex items-center gap-2 mb-3">
              <span className={`badge ${st.badge}`}>{st.label}</span>
              <span className="text-white/40 text-xs font-semibold">• {f.growth_stage}</span>
            </div>
            <h1 className="text-4xl md:text-5xl font-black text-white tracking-tight mb-2 flex items-center gap-3">
              {f.name}
            </h1>
            <p className="text-white/60 font-medium flex items-center gap-2">
              <MapPin className="w-4 h-4" /> {f.crop} · {f.area} acres
            </p>
          </div>

          {/* Call to action panel */}
          {f.status === 'IRRIGATE' && (
            <div className="card-glass p-5 flex items-center gap-5 anim-scale-up">
              <div className="text-center px-4 border-r border-gray-200/20">
                <p className="text-xs font-bold text-gray-400 uppercase mb-1">Suggest</p>
                <p className="text-3xl font-black text-water-blue">{f.recommended_water} <span className="text-base">L</span></p>
              </div>
              <div className="text-center px-4">
                <p className="text-xs font-bold text-gray-400 uppercase mb-1">Time</p>
                <p className="text-3xl font-black text-gray-700">{f.recommended_time}</p>
              </div>
            </div>
          )}
        </div>
      </div>

      {/* ── Presentation Metric Cards ── */}
      <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
        {[
          { l:'Moisture', v:`${f.soil_moisture}%`,  i:Droplets,    c:'#0288D1', b:'bg-blue-50' },
          { l:'Temp',     v:`${f.temperature}°C`,   i:Thermometer, c:'#F59E0B', b:'bg-amber-50' },
          { l:'Humidity', v:`${f.humidity}%`,       i:Activity,    c:'#2E7D32', b:'bg-green-50' },
          { l:'Rain',     v:`${f.rain_probability}%`,i:CloudRain,  c:'#0369A1', b:'bg-sky-50' },
        ].map((m, i) => (
          <div key={m.l} className={`card p-5 anim-fade-up d${Math.min(i+2,5)} text-center group`}>
            <div className={`w-12 h-12 mx-auto rounded-2xl flex items-center justify-center mb-3 transition-transform group-hover:scale-110 ${m.b}`}>
              <m.i className="w-6 h-6" style={{ color: m.c }} />
            </div>
            <p className="text-3xl font-black" style={{ color: m.c }}>{m.v}</p>
            <p className="text-xs font-bold text-gray-400 uppercase tracking-widest mt-1">{m.l}</p>
          </div>
        ))}
      </div>

      {/* ── Presentation Chart ── */}
      <div className="card p-8 anim-fade-up d5">
        <div className="flex items-center justify-between mb-8">
          <div>
            <h2 className="text-xl font-black text-gray-800">Moisture Trend</h2>
            <p className="text-sm text-gray-400 mt-1">Live tracking over 24 hours</p>
          </div>
          <div className="px-4 py-2 bg-gray-50 rounded-xl border border-gray-100 flex items-center gap-3">
            <span className="text-xs font-bold text-gray-500 uppercase">Current:</span>
            <div className="w-32 progress-track">
              <div className="progress-fill" style={{ width: `${m}%`, background: barCol }} />
            </div>
            <span className="text-sm font-black" style={{ color: barCol }}>{m}%</span>
          </div>
        </div>

        {history.length > 0 ? (
          <div className="h-[320px]">
            <ResponsiveContainer width="100%" height="100%">
              <LineChart data={history} margin={{ top:20, right:20, left:-20, bottom:0 }}>
                <defs>
                  <linearGradient id="lineGrad" x1="0" y1="0" x2="1" y2="0">
                    <stop offset="0%" stopColor="#38bdf8" />
                    <stop offset="100%" stopColor="#0288D1" />
                  </linearGradient>
                </defs>
                <CartesianGrid strokeDasharray="4 4" vertical={false} stroke="#f1f5f9" />
                <XAxis dataKey="time" axisLine={false} tickLine={false} tick={{fill:'#94a3b8', fontSize:12, fontWeight:600}} dy={12} />
                <YAxis domain={[0,100]} axisLine={false} tickLine={false} tick={{fill:'#94a3b8', fontSize:12, fontWeight:600}} />
                <Tooltip content={<CustomTooltip />} cursor={{ stroke:'#e2e8f0', strokeWidth:2, strokeDasharray:'4 4' }} />
                <ReferenceLine y={35} stroke="#ef4444" strokeDasharray="4 4" label={{ value:'Critical Min', fill:'#ef4444', fontSize:10, fontWeight:700, position:'insideTopLeft' }} />
                <Line
                  type="monotone" dataKey="moisture" stroke="url(#lineGrad)" strokeWidth={4}
                  dot={{ r:6, fill:'#fff', stroke:'#0288D1', strokeWidth:3 }}
                  activeDot={{ r:8, fill:'#0288D1', stroke:'#fff', strokeWidth:3, filter:'drop-shadow(0 4px 8px rgba(2,136,209,0.4))' }}
                />
              </LineChart>
            </ResponsiveContainer>
          </div>
        ) : (
          <div className="h-64 flex items-center justify-center text-gray-400 font-medium">No history recorded yet</div>
        )}
      </div>

    </div>
  );
}
