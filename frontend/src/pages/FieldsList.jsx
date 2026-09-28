import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { Plus, SlidersHorizontal } from 'lucide-react';
import { fetchFields } from '../services/api';

const S = {
  IRRIGATE:      { label:'Irrigate Now', badge:'badge-red',    dot:'bg-red-500',   glow:'anim-pulse-r', topBar:'linear-gradient(90deg,#ef4444,#f97316)' },
  WAIT_FOR_RAIN: { label:'Rain Coming',  badge:'badge-blue',   dot:'bg-blue-500',  glow:'anim-pulse-b', topBar:'linear-gradient(90deg,#0288D1,#60a5fa)' },
  GOOD:          { label:'Good',         badge:'badge-green',  dot:'bg-green-500', glow:'',             topBar:'linear-gradient(90deg,#22c55e,#34d399)' },
  NO_IRRIGATION: { label:'No Action',    badge:'badge-green',  dot:'bg-green-500', glow:'',             topBar:'linear-gradient(90deg,#22c55e,#34d399)' },
  MONITOR:       { label:'Monitor',      badge:'badge-yellow', dot:'bg-amber-400', glow:'',             topBar:'linear-gradient(90deg,#f59e0b,#fde68a)' },
};
const cropEmoji = { Tomato:'🍅', Rice:'🌾', Wheat:'🌱' };

function FieldCard({ f, i }) {
  const st = S[f.status] || S.MONITOR;
  const m  = f.soil_moisture ?? 0;
  const barCol = m < 35 ? '#ef4444' : m < 60 ? '#f59e0b' : '#22c55e';

  return (
    <Link to={`/fields/${f.id}`}
      className={`card block overflow-hidden anim-fade-up d${Math.min(i,5)}`}>
      {/* Top colour bar */}
      <div className="h-1.5" style={{ background: st.topBar }} />

      <div className="p-5">
        {/* Header row */}
        <div className="flex items-start justify-between mb-4">
          <div className="flex items-center gap-3">
            <div className="w-12 h-12 rounded-2xl flex items-center justify-center text-2xl
                            bg-gradient-to-br from-gray-50 to-gray-100 group-hover:scale-105 transition-transform">
              {cropEmoji[f.crop] || '🌿'}
            </div>
            <div>
              <p className="font-black text-gray-800 text-[15px]">{f.name}</p>
              <p className="text-xs text-gray-400 mt-0.5">{f.crop} · {f.growth_stage} · {f.area} ac</p>
            </div>
          </div>
          <span className={`badge ${st.badge}`}>
            <span className={`w-1.5 h-1.5 rounded-full ${st.dot} ${st.glow}`} />
            {st.label}
          </span>
        </div>

        {/* Moisture bar */}
        <div className="mb-4">
          <div className="flex justify-between text-xs font-semibold mb-1.5">
            <span className="text-gray-500">Soil Moisture</span>
            <span className="font-bold" style={{ color: barCol }}>{m}%</span>
          </div>
          <div className="progress-track">
            <div className="progress-fill" style={{ width:`${m}%`, background: barCol }} />
          </div>
        </div>

        {/* Stats grid */}
        <div className="grid grid-cols-3 gap-2">
          {[
            { emoji:'🌡️', label:'Temp',    val:`${f.temperature ?? '--'}°C`    },
            { emoji:'💧', label:'Humidity', val:`${f.humidity ?? '--'}%`         },
            { emoji:'🌧️', label:'Rain',    val:`${f.rain_probability ?? '--'}%` },
          ].map(s => (
            <div key={s.label}
              className="bg-gray-50 rounded-xl py-2.5 px-2 text-center hover:bg-gray-100 transition-colors">
              <p className="text-base leading-none">{s.emoji}</p>
              <p className="text-[10px] text-gray-400 font-semibold mt-1">{s.label}</p>
              <p className="text-xs font-bold text-gray-700 mt-0.5">{s.val}</p>
            </div>
          ))}
        </div>

        {/* Recommend footer */}
        {f.status === 'IRRIGATE' && (
          <div className="mt-4 flex items-center gap-2 px-3 py-2.5 rounded-xl
                          bg-red-50 border border-red-100">
            <span className="text-sm">💧</span>
            <span className="text-xs font-bold text-red-700">
              Apply <strong>{f.recommended_water} L</strong> at {f.recommended_time}
            </span>
          </div>
        )}
        {f.status === 'WAIT_FOR_RAIN' && (
          <div className="mt-4 flex items-center gap-2 px-3 py-2.5 rounded-xl
                          bg-blue-50 border border-blue-100">
            <span className="text-sm">🌧️</span>
            <span className="text-xs font-bold text-blue-700">Rain expected — hold irrigation</span>
          </div>
        )}
      </div>
    </Link>
  );
}

const FILTERS = ['ALL','IRRIGATE','WAIT_FOR_RAIN','GOOD','MONITOR'];

export default function FieldsList() {
  const [fields,  setFields]  = useState([]);
  const [loading, setLoading] = useState(true);
  const [active,  setActive]  = useState('ALL');

  useEffect(() => {
    fetchFields().then(setFields).catch(console.error).finally(() => setLoading(false));
  }, []);

  const shown = active === 'ALL' ? fields : fields.filter(f => f.status === active);
  const counts = FILTERS.reduce((acc,f) => {
    acc[f] = f === 'ALL' ? fields.length : fields.filter(x => x.status === f).length;
    return acc;
  }, {});

  return (
    <div className="space-y-6">

      {/* Page header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 anim-fade-up">
        <div>
          <h1 className="text-2xl font-black text-gray-900">My Fields</h1>
          <p className="text-sm text-gray-400 mt-0.5">
            {fields.length} fields · {fields.filter(f => f.status === 'IRRIGATE').length} require attention
          </p>
        </div>
        <div className="flex gap-2">
          <button className="btn-ghost flex items-center gap-2">
            <SlidersHorizontal className="w-4 h-4" /> Filter
          </button>
          <button className="btn-primary flex items-center gap-2 text-sm py-2.5 px-4">
            <Plus className="w-4 h-4" /> Add Field
          </button>
        </div>
      </div>

      {/* Filter tabs */}
      <div className="flex flex-wrap gap-2 anim-fade-up d1">
        {FILTERS.map(f => (
          <button key={f}
            onClick={() => setActive(f)}
            className={`px-4 py-1.5 rounded-full text-xs font-bold border transition-all
                        ${active === f
                          ? 'bg-primary-green text-white border-primary-green shadow-glow-g'
                          : 'bg-white text-gray-500 border-gray-200 hover:border-primary-green hover:text-primary-green'}`}>
            {f === 'ALL' ? 'All' : f.replace('_',' ')}
            {counts[f] > 0 && (
              <span className={`ml-1.5 px-1.5 py-0.5 rounded-full text-[10px]
                               ${active === f ? 'bg-white/25 text-white' : 'bg-gray-100 text-gray-500'}`}>
                {counts[f]}
              </span>
            )}
          </button>
        ))}
      </div>

      {/* Cards grid */}
      {loading
        ? <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-5">
            {[1,2,3].map(i => <div key={i} className="h-72 shimmer" />)}
          </div>
        : shown.length === 0
        ? <div className="card p-12 text-center anim-scale-up">
            <p className="text-4xl mb-3">🌿</p>
            <p className="font-bold text-gray-600">No fields match this filter</p>
          </div>
        : <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-5">
            {shown.map((f, i) => <FieldCard key={f.id} f={f} i={i} />)}
          </div>
      }
    </div>
  );
}
