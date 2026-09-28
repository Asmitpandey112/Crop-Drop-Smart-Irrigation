import React, { useState, useEffect, useRef } from 'react';
import { Link } from 'react-router-dom';
import { AlertTriangle, Droplets, Sprout, LayoutDashboard, ArrowUpRight, Wifi, TrendingDown } from 'lucide-react';
import { fetchFields } from '../services/api';

/* ── Animated counter ── */
function Counter({ to, suffix = '' }) {
  const [v, setV] = useState(0);
  const ref = useRef(null);
  useEffect(() => {
    clearInterval(ref.current);
    let n = 0;
    const step = Math.max(1, Math.ceil(to / 40));
    ref.current = setInterval(() => {
      n = Math.min(n + step, to);
      setV(n);
      if (n >= to) clearInterval(ref.current);
    }, 18);
    return () => clearInterval(ref.current);
  }, [to]);
  return <>{v}{suffix}</>;
}

/* ── Status config ── */
const S = {
  IRRIGATE:      { dot:'bg-red-500',   label:'Irrigate',   badge:'badge-red',   glow:'anim-pulse-r' },
  WAIT_FOR_RAIN: { dot:'bg-blue-500',  label:'Rain coming',badge:'badge-blue',  glow:'anim-pulse-b' },
  GOOD:          { dot:'bg-green-500', label:'Good',       badge:'badge-green', glow:'' },
  NO_IRRIGATION: { dot:'bg-green-500', label:'No action',  badge:'badge-green', glow:'' },
  MONITOR:       { dot:'bg-amber-400', label:'Monitor',    badge:'badge-yellow',glow:'' },
};

const cropEmoji = { Tomato:'🍅', Rice:'🌾', Wheat:'🌱' };

export default function Dashboard() {
  const [fields, setFields]   = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchFields().then(setFields).catch(console.error).finally(() => setLoading(false));
  }, []);

  const attn  = fields.filter(f => f.status === 'IRRIGATE').length;
  const saved  = 420;
  const used   = 350;

  return (
    <div className="space-y-7">

      {/* ══════════ HERO BANNER ══════════ */}
      <div className="relative overflow-hidden rounded-[28px] bg-hero p-8 anim-fade-up">
        {/* Decorative blobs */}
        <div className="absolute -top-16 -right-16 w-64 h-64 rounded-full
                        bg-green-600/20 blur-3xl pointer-events-none" />
        <div className="absolute bottom-0 left-1/3 w-48 h-48 rounded-full
                        bg-sky-600/15 blur-3xl pointer-events-none" />
        {/* Rotating ring */}
        <div className="absolute top-6 right-8 w-28 h-28 rounded-full
                        border-2 border-green-500/20 anim-spin-slow pointer-events-none">
          <div className="absolute top-2 left-2 right-2 bottom-2 rounded-full
                          border border-dashed border-green-400/20" />
        </div>

        <div className="relative z-10 flex flex-col md:flex-row md:items-end md:justify-between gap-6">
          <div>
            <div className="inline-flex items-center gap-2 px-3 py-1.5 rounded-full
                            bg-green-500/20 border border-green-500/30 mb-4">
              <Wifi className="w-3 h-3 text-green-400" />
              <span className="text-green-300 text-xs font-semibold live-dot">Live sensor data</span>
            </div>
            <h1 className="text-3xl md:text-4xl font-black text-white leading-tight">
              Good morning,<br />
              <span className="text-grad-gb">Farmer 🌾</span>
            </h1>
            <p className="text-white/50 text-sm mt-2 max-w-sm">
              {attn > 0 ? `${attn} field${attn > 1 ? 's' : ''} need irrigation today.` : 'All fields are adequately watered.'} Here's your farm overview.
            </p>
          </div>

          {/* Hero mini stats */}
          <div className="flex gap-3 flex-wrap">
            {[
              { label:'Fields',      val: fields.length, suf:'',  bg:'rgba(255,255,255,.06)', border:'rgba(255,255,255,.1)' },
              { label:'Need Attn.',  val: attn,          suf:'',  bg:'rgba(220,38,38,.15)',   border:'rgba(220,38,38,.25)' },
              { label:'Water Saved', val: saved,         suf:' L',bg:'rgba(46,125,50,.2)',    border:'rgba(46,125,50,.3)'  },
            ].map(s => (
              <div key={s.label}
                className="px-5 py-4 rounded-2xl text-center min-w-[90px]"
                style={{ background: s.bg, border:`1px solid ${s.border}` }}>
                <p className="text-white font-black text-2xl leading-none">
                  <Counter to={loading ? 0 : s.val} suffix={s.suf} />
                </p>
                <p className="text-white/50 text-xs font-medium mt-1">{s.label}</p>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* ══════════ STAT CARDS ══════════ */}
      <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
        {loading
          ? [1,2,3,4].map(i => <div key={i} className="h-28 shimmer" />)
          : [
              { icon:'💧', label:'Today\'s Usage',   val:used,          suf:' L', from:'#0288D1', to:'#01579B', d:'d0' },
              { icon:'🌱', label:'Water Avoided',    val:saved,         suf:' L', from:'#2E7D32', to:'#1B5E20', d:'d1' },
              { icon:'📐', label:'Total Acreage',    val: fields.reduce((s,f)=>s+(f.area||0),0), suf:' ac', from:'#7E22CE', to:'#6B21A8', d:'d2' },
              { icon:'☁️', label:'Avg Rain Prob.',   val: Math.round(fields.reduce((s,f)=>s+(f.rain_probability||0),0)/(fields.length||1)), suf:'%', from:'#0369A1', to:'#075985', d:'d3' },
            ].map(s => (
              <div key={s.label} className={`card p-5 anim-fade-up ${s.d}`}>
                <div className="flex items-start justify-between mb-4">
                  <div className="w-10 h-10 rounded-2xl flex items-center justify-center text-xl"
                    style={{ background:`linear-gradient(135deg,${s.from}22,${s.to}11)` }}>
                    {s.icon}
                  </div>
                  <ArrowUpRight className="w-4 h-4 text-gray-300" />
                </div>
                <p className="text-2xl font-black" style={{ color: s.from }}>
                  <Counter to={s.val} suffix={s.suf} />
                </p>
                <p className="text-gray-500 text-xs font-semibold mt-1">{s.label}</p>
              </div>
            ))
        }
      </div>

      {/* ══════════ BOTTOM GRID ══════════ */}
      <div className="grid grid-cols-1 xl:grid-cols-5 gap-5">

        {/* Alert list — 3 cols */}
        <div className="xl:col-span-3 space-y-3 anim-fade-up d2">
          <div className="flex items-center justify-between">
            <h2 className="font-black text-gray-800 text-base flex items-center gap-2">
              <AlertTriangle className="w-4 h-4 text-red-500" />
              Irrigation Alerts
            </h2>
            <Link to="/fields" className="text-xs font-semibold text-primary-green hover:underline flex items-center gap-1">
              All fields <ArrowUpRight className="w-3 h-3" />
            </Link>
          </div>

          {loading
            ? [1,2].map(i => <div key={i} className="h-24 shimmer" />)
            : fields.filter(f => f.status === 'IRRIGATE').length === 0
            ? (
                <div className="card p-8 text-center">
                  <div className="w-14 h-14 rounded-full bg-green-50 flex items-center justify-center mx-auto mb-3 anim-float">
                    <Sprout className="w-7 h-7 text-primary-green" />
                  </div>
                  <p className="font-bold text-gray-700">All fields are in great shape!</p>
                  <p className="text-gray-400 text-sm mt-1">No immediate irrigation needed.</p>
                </div>
              )
            : fields.filter(f => f.status === 'IRRIGATE').map((f, i) => {
                const st = S[f.status] || S.MONITOR;
                return (
                  <div key={f.id} className={`card p-5 anim-fade-up d${i}`}>
                    <div className="flex items-start justify-between gap-4">
                      <div className="flex items-center gap-3">
                        <div className={`w-2.5 h-2.5 rounded-full flex-shrink-0 ${st.dot} ${st.glow}`} />
                        <div>
                          <p className="font-bold text-gray-800">{f.name}</p>
                          <p className="text-xs text-gray-400 mt-0.5">{f.crop} · {f.growth_stage} · {f.area} ac</p>
                        </div>
                      </div>
                      <span className={`badge ${st.badge}`}>{st.label}</span>
                    </div>
                    <div className="mt-4 flex items-center gap-5 text-sm text-gray-500">
                      <span className="flex items-center gap-1.5">
                        <Droplets className="w-4 h-4 text-blue-400" />
                        Moisture: <strong className="text-gray-800">{f.soil_moisture}%</strong>
                      </span>
                      <span className="flex items-center gap-1.5">
                        <span className="text-blue-400">💧</span>
                        Suggest: <strong className="text-gray-800">{f.recommended_water} L</strong>
                      </span>
                      <Link to={`/fields/${f.id}`}
                        className="ml-auto text-xs font-bold text-primary-green flex items-center gap-1 hover:gap-2 transition-all">
                        Details <ArrowUpRight className="w-3 h-3" />
                      </Link>
                    </div>
                  </div>
                );
              })
          }
        </div>

        {/* Field cards — 2 cols */}
        <div className="xl:col-span-2 space-y-3 anim-fade-up d3">
          <h2 className="font-black text-gray-800 text-base flex items-center gap-2">
            <LayoutDashboard className="w-4 h-4 text-primary-green" />
            Field Status
          </h2>
          {loading
            ? [1,2,3].map(i => <div key={i} className="h-20 shimmer" />)
            : fields.map((f, i) => {
                const st = S[f.status] || S.MONITOR;
                const moist = f.soil_moisture ?? 0;
                const barColor = moist < 35 ? '#ef4444' : moist < 60 ? '#f59e0b' : '#22c55e';
                return (
                  <Link to={`/fields/${f.id}`} key={f.id}
                    className={`card p-4 flex items-center gap-4 cursor-pointer anim-fade-up d${i}`}>
                    <div className="w-10 h-10 rounded-2xl flex items-center justify-center text-2xl flex-shrink-0"
                      style={{ background:'rgba(0,0,0,.03)' }}>
                      {cropEmoji[f.crop] || '🌿'}
                    </div>
                    <div className="flex-1 min-w-0">
                      <div className="flex items-center justify-between">
                        <p className="font-bold text-gray-800 text-sm">{f.name}</p>
                        <span className={`badge ${st.badge} text-[10px]`}>{st.label}</span>
                      </div>
                      <div className="progress-track mt-2">
                        <div className="progress-fill" style={{ width:`${moist}%`, background: barColor }} />
                      </div>
                      <p className="text-[11px] text-gray-400 mt-1">Moisture: {moist}%</p>
                    </div>
                  </Link>
                );
              })
          }
          <Link to="/fields"
            className="block text-center py-3 rounded-2xl border-2 border-dashed border-gray-200
                       text-xs font-bold text-gray-400 hover:border-primary-green hover:text-primary-green transition-colors">
            + View all fields
          </Link>
        </div>
      </div>
    </div>
  );
}
