import { useState, useEffect, useRef, useCallback } from 'react';
import {
  Search, ChevronDown, ChevronUp, ExternalLink, Shield, Sparkles,
  FileCheck, Link2, Sun, Moon, Globe, ArrowRight, CheckCircle2,
  AlertCircle, HelpCircle, XCircle, Info, FileText, ClipboardList,
  Building2, MapPin, Send, Loader2, X, MessageSquare, ChevronRight,
  Landmark, Users, BookOpen, Heart,
} from 'lucide-react';
import { api } from './api/client';
import { t } from './lib/i18n';
import { INDIAN_STATES, EDUCATION_LEVELS, OCCUPATIONS, CATEGORIES } from './constants';

const STATES = INDIAN_STATES;
const EDUS = EDUCATION_LEVELS;
const OCCS = OCCUPATIONS;
const CATS = CATEGORIES;

// Loading steps
const LOADING_STEPS = [
  'loading.understanding',
  'loading.searching',
  'loading.reading',
  'loading.checking',
  'loading.preparing',
];

// Status config
const STATUS_CONFIG = {
  LIKELY_ELIGIBLE: { color: 'bg-emerald-50 text-emerald-700 border-emerald-200', darkColor: 'dark:bg-emerald-950/50 dark:text-emerald-300 dark:border-emerald-800', icon: CheckCircle2, label: 'status.LIKELY_ELIGIBLE' },
  POSSIBLY_ELIGIBLE: { color: 'bg-amber-50 text-amber-700 border-amber-200', darkColor: 'dark:bg-amber-950/50 dark:text-amber-300 dark:border-amber-800', icon: HelpCircle, label: 'status.POSSIBLY_ELIGIBLE' },
  NEEDS_MORE_INFORMATION: { color: 'bg-sky-50 text-sky-700 border-sky-200', darkColor: 'dark:bg-sky-950/50 dark:text-sky-300 dark:border-sky-800', icon: Info, label: 'status.NEEDS_MORE_INFORMATION' },
  LIKELY_NOT_ELIGIBLE: { color: 'bg-red-50 text-red-700 border-red-200', darkColor: 'dark:bg-red-950/50 dark:text-red-300 dark:border-red-800', icon: XCircle, label: 'status.LIKELY_NOT_ELIGIBLE' },
  UNVERIFIED: { color: 'bg-gray-50 text-gray-600 border-gray-200', darkColor: 'dark:bg-gray-800/50 dark:text-gray-300 dark:border-gray-700', icon: AlertCircle, label: 'status.UNVERIFIED' },
};

function App() {
  // State
  const [lang, setLang] = useState('en');
  const [theme, setTheme] = useState(() =>
    typeof window !== 'undefined' && window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light'
  );
  const [query, setQuery] = useState('');
  const [profile, setProfile] = useState({});
  const [showProfile, setShowProfile] = useState(false);
  const [loading, setLoading] = useState(false);
  const [loadingStep, setLoadingStep] = useState(0);
  const [results, setResults] = useState(null);
  const [error, setError] = useState(null);
  const [expandedScheme, setExpandedScheme] = useState(null);
  const [sessionId, setSessionId] = useState(null);
  const [followUp, setFollowUp] = useState('');
  const [page, setPage] = useState('home'); // 'home' | 'results' | 'about'
  const resultsRef = useRef(null);
  const searchRef = useRef(null);

  // Theme effect
  useEffect(() => {
    document.documentElement.classList.toggle('dark', theme === 'dark');
  }, [theme]);

  // Loading animation
  useEffect(() => {
    if (!loading) return;
    const interval = setInterval(() => {
      setLoadingStep(prev => (prev < LOADING_STEPS.length - 1 ? prev + 1 : prev));
    }, 3000);
    return () => clearInterval(interval);
  }, [loading]);

  const handleSearch = useCallback(async (searchQuery = null) => {
    const q = searchQuery || query;
    if (!q.trim()) return;

    setLoading(true);
    setLoadingStep(0);
    setError(null);
    setResults(null);
    setPage('results');

    try {
      const cleanProfile = {};
      if (profile.age) cleanProfile.age = profile.age;
      if (profile.state) cleanProfile.state = profile.state;
      if (profile.education) cleanProfile.education = profile.education;
      if (profile.occupation) cleanProfile.occupation = profile.occupation;
      if (profile.income) cleanProfile.income = profile.income;
      if (profile.gender) cleanProfile.gender = profile.gender;
      if (profile.category) cleanProfile.category = profile.category;
      if (profile.disability) cleanProfile.disability = profile.disability;

      const hasProfile = Object.keys(cleanProfile).length > 0;

      const payload = {
        query: q,
        profile: hasProfile ? cleanProfile : undefined,
        session_id: sessionId || undefined,
      };

      const res = await api.search(payload);

      setResults(res);
      setSessionId(res.session_id || null);
      setTimeout(() => resultsRef.current?.scrollIntoView({ behavior: 'smooth', block: 'start' }), 300);
    } catch (err) {
      const msg = err.message || 'Something went wrong. Please try again.';
      setError(msg);
    } finally {
      setLoading(false);
      setLoadingStep(0);
    }
  }, [query, profile, sessionId]);

  const handleFollowUp = useCallback(async () => {
    if (!followUp.trim() || !sessionId) return;

    const currentMessage = followUp;
    setFollowUp('');
    setLoading(true);
    setLoadingStep(0);
    setError(null);

    try {
      const res = await api.chat({
        message: currentMessage,
        session_id: sessionId,
      });
      setResults(res);
    } catch (err) {
      const msg = err.message || 'Something went wrong.';
      setError(msg);
      setFollowUp(currentMessage);
    } finally {
      setLoading(false);
    }
  }, [followUp, sessionId]);

  const handleExampleClick = (example) => {
    setQuery(example);
    handleSearch(example);
  };

  const toggleTheme = () => setTheme(prev => prev === 'light' ? 'dark' : 'light');
  const toggleLang = () => setLang(prev => prev === 'en' ? 'hi' : 'en');

  // ─── HEADER ────────────────────────────────────────
  const Header = () => (
    <header className="sticky top-0 z-50 backdrop-blur-xl bg-white/70 dark:bg-slate-950/70 border-b border-slate-200/50 dark:border-slate-800/50 transition-colors duration-300">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          <button onClick={() => { setPage('home'); setResults(null); }} className="flex items-center gap-2.5 group">
            <div className="w-9 h-9 rounded-xl bg-gradient-to-br from-india-600 to-india-800 flex items-center justify-center shadow-lg shadow-india-500/20 group-hover:shadow-india-500/40 transition-shadow">
              <Landmark className="w-5 h-5 text-white" />
            </div>
            <div>
              <span className="text-lg font-bold text-slate-900 dark:text-white tracking-tight">{t('app.name', lang)}</span>
            </div>
          </button>

          <div className="flex items-center gap-2">
            <button
              onClick={() => setPage('about')}
              className="hidden sm:flex px-3 py-1.5 text-sm font-medium text-slate-600 dark:text-slate-300 hover:text-slate-900 dark:hover:text-white transition-colors"
            >
              {t('footer.about', lang)}
            </button>
            <button
              onClick={toggleLang}
              className="flex items-center gap-1.5 px-3 py-1.5 text-sm font-medium rounded-lg bg-slate-100 dark:bg-slate-800 text-slate-700 dark:text-slate-300 hover:bg-slate-200 dark:hover:bg-slate-700 transition-colors"
              aria-label="Switch language"
            >
              <Globe className="w-4 h-4" />
              <span>{lang === 'en' ? 'हि' : 'EN'}</span>
            </button>
            <button
              onClick={toggleTheme}
              className="p-2 rounded-lg bg-slate-100 dark:bg-slate-800 text-slate-700 dark:text-slate-300 hover:bg-slate-200 dark:hover:bg-slate-700 transition-colors"
              aria-label="Toggle theme"
            >
              {theme === 'light' ? <Moon className="w-4 h-4" /> : <Sun className="w-4 h-4" />}
            </button>
          </div>
        </div>
      </div>
    </header>
  );

  // ─── HERO ──────────────────────────────────────────
  const Hero = () => (
    <div className="relative pt-24 pb-16 sm:pt-32 sm:pb-24 overflow-hidden">
      <div className="absolute inset-0 -z-10 bg-[radial-gradient(ellipse_at_top,_var(--tw-gradient-stops))] from-india-100/40 via-white to-white dark:from-india-900/20 dark:via-slate-950 dark:to-slate-950 transition-colors duration-300"></div>
      
      <div className="text-center max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-white/60 dark:bg-slate-800/60 backdrop-blur-md border border-slate-200/60 dark:border-slate-700/60 text-sm font-medium text-slate-700 dark:text-slate-200 mb-8 shadow-sm animate-fade-in">
          <Sparkles className="w-4 h-4 text-saffron-500" />
          <span>{t('app.tagline', lang)}</span>
        </div>
        
        <h1 className="text-5xl sm:text-7xl font-extrabold text-slate-900 dark:text-white tracking-tight mb-6 leading-tight animate-slide-up" style={{ animationDelay: '100ms', animationFillMode: 'both' }}>
          {t('hero.title', lang)} <br className="hidden sm:block" />
          <span className="text-transparent bg-clip-text bg-gradient-to-r from-india-600 to-saffron-500 dark:from-india-400 dark:to-saffron-400">
            {t('hero.title.highlight', lang)}
          </span>
        </h1>
        
        <p className="mt-6 text-xl text-slate-600 dark:text-slate-400 max-w-2xl mx-auto leading-relaxed animate-slide-up" style={{ animationDelay: '200ms', animationFillMode: 'both' }}>
          {t('hero.subtitle', lang)}
        </p>

        {/* Trust indicators */}
        <div className="flex flex-wrap justify-center gap-4 sm:gap-6 pt-4">
          {[
            { icon: Shield, key: 'trust.official' },
            { icon: Sparkles, key: 'trust.ai' },
            { icon: FileCheck, key: 'trust.eligibility' },
            { icon: Link2, key: 'trust.sources' },
          ].map(({ icon: Icon, key }) => (
            <div key={key} className="flex items-center gap-2 text-sm text-slate-600 dark:text-slate-400">
              <Icon className="w-4 h-4 text-india-500" />
              <span>{t(key, lang)}</span>
            </div>
          ))}
        </div>
      </div>
    </div>
  );

  // ─── SEARCH BOX ────────────────────────────────────
  const SearchBox = () => (
    <section className="relative -mt-8 sm:-mt-12 z-10">
      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="bg-white/70 dark:bg-slate-900/70 backdrop-blur-xl rounded-3xl shadow-xl shadow-slate-200/50 dark:shadow-none border border-white/50 dark:border-slate-700/50 p-4 sm:p-6 space-y-4 transition-all duration-300">
          {/* Search input */}
          <div className="relative">
            <textarea
              ref={searchRef}
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              onKeyDown={(e) => { if (e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); handleSearch(); } }}
              placeholder={t('search.placeholder', lang)}
              rows={3}
              className="w-full px-4 py-3.5 pr-12 text-base rounded-xl border border-slate-200 dark:border-slate-600 bg-slate-50/50 dark:bg-slate-900/50 text-slate-900 dark:text-white placeholder:text-slate-400 dark:placeholder:text-slate-500 focus:outline-none focus:ring-2 focus:ring-india-500/40 focus:border-india-500 dark:focus:ring-india-400/40 dark:focus:border-india-400 resize-none transition-all"
              aria-label="Search query"
              id="search-input"
            />
            <button
              onClick={() => handleSearch()}
              disabled={!query.trim() || loading}
              className="absolute right-3 bottom-3 p-2.5 rounded-xl bg-gradient-to-r from-india-600 to-india-500 hover:from-india-500 hover:to-india-400 text-white disabled:opacity-50 disabled:cursor-not-allowed transition-all shadow-lg shadow-india-500/25 hover:shadow-india-500/40"
              aria-label="Search"
            >
              {loading ? <Loader2 className="w-5 h-5 animate-spin" /> : <Search className="w-5 h-5" />}
            </button>
          </div>

          {/* Profile toggle */}
          <div>
            <button
              onClick={() => setShowProfile(!showProfile)}
              className="flex items-center gap-2 text-sm font-medium text-india-600 dark:text-india-400 hover:text-india-700 dark:hover:text-india-300 transition-colors"
            >
              {showProfile ? <ChevronUp className="w-4 h-4" /> : <ChevronDown className="w-4 h-4" />}
              {t(showProfile ? 'profile.hide' : 'profile.toggle', lang)}
            </button>

            {showProfile && (
              <div className="mt-4 grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-3 animate-[slide-up_0.3s_ease-out]">
                <div>
                  <label htmlFor="age" className="block text-xs font-medium text-slate-500 dark:text-slate-400 mb-1">{t('profile.age', lang)}</label>
                  <input id="age" type="number" min={1} max={120} value={profile.age || ''} onChange={e => setProfile(p => ({ ...p, age: e.target.value ? parseInt(e.target.value) : undefined }))} className="w-full px-3 py-2 text-sm rounded-lg border border-slate-200 dark:border-slate-600 bg-white dark:bg-slate-900 text-slate-900 dark:text-white focus:ring-2 focus:ring-india-500/40" />
                </div>
                <div>
                  <label htmlFor="state" className="block text-xs font-medium text-slate-500 dark:text-slate-400 mb-1">{t('profile.state', lang)}</label>
                  <select id="state" value={profile.state || ''} onChange={e => setProfile(p => ({ ...p, state: e.target.value || undefined }))} className="w-full px-3 py-2 text-sm rounded-lg border border-slate-200 dark:border-slate-600 bg-white dark:bg-slate-900 text-slate-900 dark:text-white focus:ring-2 focus:ring-india-500/40">
                    <option value="">Select...</option>
                    {STATES.map(s => <option key={s} value={s}>{s}</option>)}
                  </select>
                </div>
                <div>
                  <label htmlFor="education" className="block text-xs font-medium text-slate-500 dark:text-slate-400 mb-1">{t('profile.education', lang)}</label>
                  <select id="education" value={profile.education || ''} onChange={e => setProfile(p => ({ ...p, education: e.target.value || undefined }))} className="w-full px-3 py-2 text-sm rounded-lg border border-slate-200 dark:border-slate-600 bg-white dark:bg-slate-900 text-slate-900 dark:text-white focus:ring-2 focus:ring-india-500/40">
                    <option value="">Select...</option>
                    {EDUS.map(e => <option key={e} value={e}>{e}</option>)}
                  </select>
                </div>
                <div>
                  <label htmlFor="occupation" className="block text-xs font-medium text-slate-500 dark:text-slate-400 mb-1">{t('profile.occupation', lang)}</label>
                  <select id="occupation" value={profile.occupation || ''} onChange={e => setProfile(p => ({ ...p, occupation: e.target.value || undefined }))} className="w-full px-3 py-2 text-sm rounded-lg border border-slate-200 dark:border-slate-600 bg-white dark:bg-slate-900 text-slate-900 dark:text-white focus:ring-2 focus:ring-india-500/40">
                    <option value="">Select...</option>
                    {OCCS.map(o => <option key={o} value={o}>{o}</option>)}
                  </select>
                </div>
                <div>
                  <label htmlFor="income" className="block text-xs font-medium text-slate-500 dark:text-slate-400 mb-1">{t('profile.income', lang)}</label>
                  <input id="income" type="number" min={0} value={profile.income || ''} onChange={e => setProfile(p => ({ ...p, income: e.target.value ? parseFloat(e.target.value) : undefined }))} className="w-full px-3 py-2 text-sm rounded-lg border border-slate-200 dark:border-slate-600 bg-white dark:bg-slate-900 text-slate-900 dark:text-white focus:ring-2 focus:ring-india-500/40" />
                </div>
                <div>
                  <label htmlFor="gender" className="block text-xs font-medium text-slate-500 dark:text-slate-400 mb-1">{t('profile.gender', lang)}</label>
                  <select id="gender" value={profile.gender || ''} onChange={e => setProfile(p => ({ ...p, gender: e.target.value || undefined }))} className="w-full px-3 py-2 text-sm rounded-lg border border-slate-200 dark:border-slate-600 bg-white dark:bg-slate-900 text-slate-900 dark:text-white focus:ring-2 focus:ring-india-500/40">
                    <option value="">Select...</option>
                    <option value="Male">Male</option>
                    <option value="Female">Female</option>
                    <option value="Other">Other</option>
                  </select>
                </div>
                <div>
                  <label htmlFor="category" className="block text-xs font-medium text-slate-500 dark:text-slate-400 mb-1">{t('profile.category', lang)}</label>
                  <select id="category" value={profile.category || ''} onChange={e => setProfile(p => ({ ...p, category: e.target.value || undefined }))} className="w-full px-3 py-2 text-sm rounded-lg border border-slate-200 dark:border-slate-600 bg-white dark:bg-slate-900 text-slate-900 dark:text-white focus:ring-2 focus:ring-india-500/40">
                    <option value="">Select...</option>
                    {CATS.map(c => <option key={c} value={c}>{c}</option>)}
                  </select>
                </div>
                <div>
                  <label htmlFor="disability" className="block text-xs font-medium text-slate-500 dark:text-slate-400 mb-1">{t('profile.disability', lang)}</label>
                  <select id="disability" value={profile.disability || ''} onChange={e => setProfile(p => ({ ...p, disability: e.target.value || undefined }))} className="w-full px-3 py-2 text-sm rounded-lg border border-slate-200 dark:border-slate-600 bg-white dark:bg-slate-900 text-slate-900 dark:text-white focus:ring-2 focus:ring-india-500/40">
                    <option value="">None</option>
                    <option value="Yes">Yes</option>
                  </select>
                </div>
              </div>
            )}
          </div>

          {/* Example queries */}
          <div className="space-y-2">
            <p className="text-xs font-medium text-slate-400 dark:text-slate-500 uppercase tracking-wider">{t('search.examples.title', lang)}</p>
            <div className="flex flex-wrap gap-2">
              {[1, 2, 3, 4].map(i => (
                <button
                  key={i}
                  onClick={() => handleExampleClick(t(`search.example.${i}`, lang))}
                  className="text-xs px-3 py-1.5 rounded-lg bg-slate-100 dark:bg-slate-700/50 text-slate-600 dark:text-slate-300 hover:bg-india-50 hover:text-india-700 dark:hover:bg-india-900/30 dark:hover:text-india-300 border border-transparent hover:border-india-200 dark:hover:border-india-700 transition-all truncate max-w-[280px]"
                >
                  {t(`search.example.${i}`, lang)}
                </button>
              ))}
            </div>
          </div>
        </div>
      </div>
    </section>
  );

  // ─── HOW IT WORKS ──────────────────────────────────
  const HowItWorks = () => (
    <section className="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 py-20" id="how-it-works">
      <h2 className="text-2xl sm:text-3xl font-bold text-center text-slate-900 dark:text-white mb-12">
        {t('how.title', lang)}
      </h2>
      <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
        {[
          { icon: MessageSquare, step: 1, color: 'from-india-500 to-india-600' },
          { icon: Search, step: 2, color: 'from-neem-500 to-neem-600' },
          { icon: FileCheck, step: 3, color: 'from-saffron-500 to-saffron-600' },
        ].map(({ icon: Icon, step, color }) => (
          <div key={step} className="relative flex flex-col items-center text-center space-y-4 group">
            <div className={`w-14 h-14 rounded-2xl bg-gradient-to-br ${color} flex items-center justify-center shadow-lg group-hover:scale-105 transition-transform`}>
              <Icon className="w-7 h-7 text-white" />
            </div>
            <div className="absolute -top-2 -right-2 w-7 h-7 rounded-full bg-white dark:bg-slate-800 border-2 border-slate-200 dark:border-slate-600 flex items-center justify-center text-xs font-bold text-slate-500 dark:text-slate-400 md:hidden">
              {step}
            </div>
            <h3 className="text-lg font-semibold text-slate-900 dark:text-white">
              {t(`how.step.${step}.title`, lang)}
            </h3>
            <p className="text-sm text-slate-600 dark:text-slate-400 leading-relaxed max-w-xs">
              {t(`how.step.${step}.desc`, lang)}
            </p>
            {step < 3 && (
              <ChevronRight className="hidden md:block absolute -right-6 top-7 w-5 h-5 text-slate-300 dark:text-slate-600" />
            )}
          </div>
        ))}
      </div>
    </section>
  );

  // ─── LOADING STATE ─────────────────────────────────
  const LoadingState = () => (
    <div className="py-24 flex justify-center animate-fade-in">
      <div className="max-w-md w-full bg-white/60 dark:bg-slate-900/60 backdrop-blur-md rounded-3xl p-8 border border-slate-200/60 dark:border-slate-700/60 shadow-xl text-center">
        <div className="relative w-20 h-20 mx-auto mb-6">
          <div className="absolute inset-0 border-4 border-slate-100 dark:border-slate-800 rounded-full"></div>
          <div className="absolute inset-0 border-4 border-india-500 rounded-full border-t-transparent animate-spin"></div>
          <div className="absolute inset-0 flex items-center justify-center">
            <Search className="w-8 h-8 text-india-600 dark:text-india-400 animate-pulse" />
          </div>
        </div>
        
        <h3 className="text-xl font-bold text-slate-900 dark:text-white mb-2">
          {t('loading.searching', lang)}
        </h3>
        
        <div className="mt-8 space-y-4 text-left">
          {LOADING_STEPS.map((step, idx) => (
            <div key={idx} className="flex items-center gap-4 transition-all duration-500">
              <div className={`w-6 h-6 rounded-full flex items-center justify-center shrink-0 transition-colors ${
                idx < loadingStep ? 'bg-emerald-100 dark:bg-emerald-900/30 text-emerald-600 dark:text-emerald-400' :
                  idx === loadingStep ? 'bg-india-100 dark:bg-india-900/30 text-india-600 dark:text-india-400' :
                    'bg-slate-100 dark:bg-slate-800 text-slate-400'
              }`}>
                {idx < loadingStep ? <CheckCircle2 className="w-4 h-4" /> :
                  idx === loadingStep ? <Loader2 className="w-4 h-4 animate-spin" /> :
                    <div className="w-2 h-2 rounded-full bg-current" />}
              </div>
              <span className={`text-sm font-medium ${
                idx <= loadingStep ? 'text-slate-700 dark:text-slate-200' : 'text-slate-400'
              }`}>
                {t(step, lang)}
              </span>
            </div>
          ))}
        </div>
      </div>
    </div>
  );

  // ─── STATUS BADGE ──────────────────────────────────
  const StatusBadge = ({ status }) => {
    const config = STATUS_CONFIG[status];
    const Icon = config.icon;
    return (
      <span className={`inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-semibold border ${config.color} ${config.darkColor}`}>
        <Icon className="w-3.5 h-3.5" />
        {t(config.label, lang)}
      </span>
    );
  };

  // ─── SCHEME CARD ───────────────────────────────────
  const SchemeCard = ({ scheme, index }) => {
    const isExpanded = expandedScheme === index;
    const status = STATUS_CONFIG[scheme.status] || STATUS_CONFIG.UNVERIFIED;
    const StatusIcon = status.icon;

    return (
      <div
        className={`group bg-white/80 dark:bg-slate-900/80 backdrop-blur-sm rounded-3xl overflow-hidden border transition-all duration-300 shadow-sm hover:shadow-xl ${
          isExpanded 
            ? 'border-india-300/50 dark:border-india-700/50 shadow-lg' 
            : 'border-slate-200/50 dark:border-slate-700/50'
        }`}
        style={{ animationDelay: `${index * 80}ms`, animationFillMode: 'backwards' }}
      >
        {/* Card Header */}
        <div 
          className="p-6 sm:p-8 cursor-pointer flex gap-4 sm:gap-6 items-start"
          onClick={() => setExpandedScheme(isExpanded ? null : index)}
        >
          <div className={`w-12 h-12 rounded-2xl shrink-0 flex items-center justify-center shadow-sm ${status.color} ${status.darkColor}`}>
            <StatusIcon className="w-6 h-6" />
          </div>
          
          <div className="flex-grow min-w-0 space-y-2">
            <div className="flex flex-wrap items-center gap-3">
              <span className={`inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-semibold ${status.color} ${status.darkColor}`}>
                {t(status.label, lang)}
              </span>
              {scheme.authority?.ministry && (
                <span className="text-xs font-medium text-slate-400 dark:text-slate-500 uppercase tracking-wider flex items-center gap-1 truncate">
                  <Building2 className="w-3 h-3 shrink-0" />
                  <span className="truncate">{scheme.authority.ministry}</span>
                </span>
              )}
            </div>
            
            <h3 className="text-xl font-bold text-slate-900 dark:text-white leading-tight group-hover:text-india-600 dark:group-hover:text-india-400 transition-colors">
              {scheme.name || 'Unknown Scheme'}
            </h3>
            {scheme.description && (
              <p className="text-sm text-slate-600 dark:text-slate-400 line-clamp-2 leading-relaxed">
                {scheme.description}
              </p>
            )}

            {/* Quick info */}
            <div className="flex flex-wrap gap-2 pt-1">
              {scheme.category && (
                <span className="text-xs px-2 py-0.5 rounded bg-slate-100 dark:bg-slate-700 text-slate-600 dark:text-slate-300">
                  {scheme.category}
                </span>
              )}
              {scheme.geographic_scope?.states?.map(s => (
                <span key={s} className="text-xs px-2 py-0.5 rounded bg-india-50 dark:bg-india-900/30 text-india-700 dark:text-india-300 flex items-center gap-1">
                  <MapPin className="w-3 h-3" />{s}
                </span>
              ))}
            </div>

            {/* Why it matches */}
            {scheme.why_it_matches && scheme.why_it_matches.length > 0 && (
              <div className="space-y-1 pt-1">
                <p className="text-xs font-semibold text-neem-700 dark:text-neem-400 flex items-center gap-1">
                  <CheckCircle2 className="w-3.5 h-3.5" />
                  {t('scheme.why.matches', lang)}
                </p>
                <ul className="space-y-0.5">
                  {scheme.why_it_matches.slice(0, 3).map((m, i) => (
                    <li key={i} className="text-xs text-slate-600 dark:text-slate-400 pl-5">• {m}</li>
                  ))}
                </ul>
              </div>
            )}
          </div>
          
          <div className="shrink-0 mt-2 bg-slate-50 dark:bg-slate-800 p-2 rounded-full text-slate-400 group-hover:bg-india-50 dark:group-hover:bg-india-900/30 group-hover:text-india-600 transition-colors">
            {isExpanded ? <ChevronUp className="w-5 h-5" /> : <ChevronDown className="w-5 h-5" />}
          </div>
        </div>

        {/* Expanded Details */}
        {isExpanded && (
          <div className="border-t border-slate-100 dark:border-slate-700 p-6 sm:p-8 space-y-6 animate-[slide-up_0.3s_ease-out]">
            {/* Unknown requirements */}
            {scheme.unknown_requirements && scheme.unknown_requirements.length > 0 && (
              <div className="p-4 rounded-2xl bg-amber-50/80 dark:bg-amber-900/20 border border-amber-200/60 dark:border-amber-800/40">
                <p className="text-xs font-semibold text-amber-700 dark:text-amber-400 flex items-center gap-1.5 mb-2">
                  <AlertCircle className="w-4 h-4" />
                  {t('scheme.unknown', lang)}
                </p>
                <ul className="space-y-1">
                  {scheme.unknown_requirements.map((u, i) => (
                    <li key={i} className="text-xs text-amber-700/80 dark:text-amber-300/80">• {u}</li>
                  ))}
                </ul>
              </div>
            )}

            {/* Not matched */}
            {scheme.not_matched && scheme.not_matched.length > 0 && (
              <div className="p-4 rounded-2xl bg-red-50/80 dark:bg-red-900/20 border border-red-200/60 dark:border-red-800/40">
                <p className="text-xs font-semibold text-red-700 dark:text-red-400 flex items-center gap-1.5 mb-2">
                  <XCircle className="w-4 h-4" />
                  {t('scheme.not.matched', lang)}
                </p>
                <ul className="space-y-1">
                  {scheme.not_matched.map((n, i) => (
                    <li key={i} className="text-xs text-red-700/80 dark:text-red-300/80">• {n}</li>
                  ))}
                </ul>
              </div>
            )}

            {/* Benefits */}
            {scheme.benefits && scheme.benefits.length > 0 && (
              <div>
                <h4 className="text-sm font-semibold text-slate-900 dark:text-white flex items-center gap-2 mb-3">
                  <Heart className="w-4 h-4 text-saffron-500" />
                  {t('scheme.benefits', lang)}
                </h4>
                <ul className="space-y-1.5">
                  {scheme.benefits.map((b, i) => (
                    <li key={i} className="text-sm text-slate-600 dark:text-slate-400">
                      • {b.description}{b.amount ? ` — ${b.amount}` : ''}{b.frequency ? ` (${b.frequency})` : ''}
                    </li>
                  ))}
                </ul>
              </div>
            )}

            {/* Documents */}
            {scheme.documents && scheme.documents.length > 0 && (
              <div>
                <h4 className="text-sm font-semibold text-slate-900 dark:text-white flex items-center gap-2 mb-3">
                  <FileText className="w-4 h-4 text-india-500" />
                  {t('scheme.documents', lang)}
                </h4>
                <ul className="space-y-1.5">
                  {scheme.documents.map((d, i) => (
                    <li key={i} className="text-sm text-slate-600 dark:text-slate-400 flex items-center gap-2">
                      <span className={`w-1.5 h-1.5 rounded-full ${d.mandatory ? 'bg-red-400' : 'bg-slate-300 dark:bg-slate-600'}`} />
                      {d.document}{d.mandatory === false ? ' (optional)' : ''}
                    </li>
                  ))}
                </ul>
              </div>
            )}

            {/* Application Steps */}
            {scheme.application_steps && scheme.application_steps.length > 0 && (
              <div>
                <h4 className="text-sm font-semibold text-slate-900 dark:text-white flex items-center gap-2 mb-3">
                  <ClipboardList className="w-4 h-4 text-neem-500" />
                  {t('scheme.application', lang)}
                </h4>
                <ol className="space-y-2">
                  {scheme.application_steps.map((s, i) => (
                    <li key={i} className="text-sm text-slate-600 dark:text-slate-400 flex gap-3">
                      <span className="flex-shrink-0 w-6 h-6 rounded-full bg-slate-100 dark:bg-slate-800 text-xs flex items-center justify-center font-medium text-slate-500 dark:text-slate-400">{s.step}</span>
                      {s.description}
                    </li>
                  ))}
                </ol>
              </div>
            )}

            {/* Source */}
            <div className="p-4 rounded-2xl bg-slate-50/80 dark:bg-slate-900/50 border border-slate-200/60 dark:border-slate-700/60">
              <h4 className="text-xs font-semibold text-slate-500 dark:text-slate-400 uppercase tracking-wider mb-2 flex items-center gap-1.5">
                <Link2 className="w-4 h-4" />
                {t('scheme.source', lang)}
              </h4>
              {scheme.sources?.map((src, i) => (
                <div key={i} className="space-y-1">
                  <span className={`inline-flex items-center gap-1 text-xs px-2 py-0.5 rounded ${
                    src.source_type === 'official_government'
                      ? 'bg-neem-100 text-neem-700 dark:bg-neem-900/30 dark:text-neem-400'
                      : 'bg-slate-200 text-slate-600 dark:bg-slate-700 dark:text-slate-300'
                  }`}>
                    <Shield className="w-3 h-3" />
                    {src.source_type === 'official_government' ? t('source.official', lang) : t('source.secondary', lang)}
                  </span>
                  {src.title && <p className="text-sm text-slate-700 dark:text-slate-300">{src.title}</p>}
                  {src.domain && <p className="text-xs text-slate-500 dark:text-slate-400">{src.domain}</p>}
                </div>
              ))}
              {scheme.official_url && (
                <a
                  href={scheme.official_url}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="inline-flex items-center gap-1.5 mt-3 text-sm font-medium text-india-600 dark:text-india-400 hover:text-india-700 dark:hover:text-india-300 transition-colors"
                >
                  <ExternalLink className="w-4 h-4" />
                  {t('source.view', lang)}
                </a>
              )}
            </div>

            {/* Verification reminder */}
            <p className="text-xs text-slate-400 dark:text-slate-500 italic text-center pt-2">
              {t('verify.reminder', lang)}
            </p>
          </div>
        )}
      </div>
    );
  };

  // ─── RESULTS ───────────────────────────────────────
  const Results = () => {
    if (loading) return <LoadingState />;
    if (!results) return null;

    return (
      <div ref={resultsRef} className="max-w-4xl mx-auto px-4 sm:px-6 py-8 space-y-6 animate-[fade-in_0.4s_ease-out]">
        {/* Search metadata */}
        <div className="flex flex-wrap items-center gap-3 text-xs text-slate-500 dark:text-slate-400">
          <span className="flex items-center gap-1">
            <Search className="w-3.5 h-3.5" />
            {t('results.sources.checked', lang)}: {results.search_metadata.sources_checked}
          </span>
          <span className="flex items-center gap-1">
            <Shield className="w-3.5 h-3.5 text-neem-500" />
            {t('results.sources.official', lang)}: {results.search_metadata.official_sources}
          </span>
        </div>

        {/* Summary */}
        {results.summary && (
          <div className="p-4 sm:p-5 rounded-xl bg-india-50/60 dark:bg-india-900/20 border border-india-200/50 dark:border-india-800/40">
            <h3 className="text-sm font-semibold text-india-800 dark:text-india-300 mb-2 flex items-center gap-1.5">
              <Sparkles className="w-4 h-4" />
              {t('results.summary', lang)}
            </h3>
            <p className="text-sm text-slate-700 dark:text-slate-300 leading-relaxed whitespace-pre-line">
              {results.summary}
            </p>
          </div>
        )}

        {/* Schemes */}
        {results.schemes.length > 0 ? (
          <div className="space-y-4">
            <h2 className="text-lg font-bold text-slate-900 dark:text-white">
              {t('results.found', lang, { count: results.schemes.length })}
            </h2>
            {results.schemes.map((scheme, index) => (
              <SchemeCard key={index} scheme={scheme} index={index} />
            ))}
          </div>
        ) : (
          <div className="text-center py-12 space-y-3">
            <div className="w-16 h-16 mx-auto rounded-full bg-slate-100 dark:bg-slate-800 flex items-center justify-center">
              <Search className="w-8 h-8 text-slate-400" />
            </div>
            <h3 className="text-lg font-semibold text-slate-700 dark:text-slate-300">{t('results.none', lang)}</h3>
            <p className="text-sm text-slate-500 dark:text-slate-400">{t('results.refine', lang)}</p>
          </div>
        )}

        {/* Follow-up */}
        {sessionId && (
          <div className="flex gap-2 items-end pt-4 border-t border-slate-200 dark:border-slate-700">
            <div className="flex-1">
              <input
                type="text"
                value={followUp}
                onChange={e => setFollowUp(e.target.value)}
                onKeyDown={e => { if (e.key === 'Enter') handleFollowUp(); }}
                placeholder={t('chat.placeholder', lang)}
                className="w-full px-4 py-3 text-sm rounded-xl border border-slate-200 dark:border-slate-600 bg-white dark:bg-slate-800 text-slate-900 dark:text-white placeholder:text-slate-400 focus:ring-2 focus:ring-india-500/40 focus:border-india-500"
                aria-label="Follow-up question"
                id="followup-input"
              />
            </div>
            <button
              onClick={handleFollowUp}
              disabled={!followUp.trim() || loading}
              className="p-3 rounded-xl bg-india-600 hover:bg-india-700 text-white disabled:opacity-50 transition-all shadow-lg shadow-india-500/25"
              aria-label="Send follow-up"
            >
              <Send className="w-5 h-5" />
            </button>
          </div>
        )}

        {/* Disclaimer */}
        {results.disclaimer && (
          <p className="text-xs text-slate-400 dark:text-slate-500 text-center leading-relaxed max-w-2xl mx-auto pt-4">
            {results.disclaimer}
          </p>
        )}
      </div>
    );
  };

  // ─── ABOUT PAGE ────────────────────────────────────
  const About = () => (
    <div className="max-w-3xl mx-auto px-4 sm:px-6 py-16 space-y-8 animate-[fade-in_0.4s_ease-out]">
      <h1 className="text-3xl font-bold text-slate-900 dark:text-white">{t('about.title', lang)}</h1>
      <p className="text-base text-slate-600 dark:text-slate-400 leading-relaxed">{t('about.desc', lang)}</p>
      
      <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
        {[
          { icon: Search, title: 'Dynamic Search', desc: 'Searches government sources in real-time instead of relying on a static database' },
          { icon: Shield, title: 'Source-Grounded', desc: 'Every result traces back to a source with clear authority labeling' },
          { icon: Users, title: 'Natural Language', desc: 'Ask in your own words — no need to know official scheme names' },
          { icon: BookOpen, title: 'Eligibility Analysis', desc: 'Deterministic eligibility checking with transparent reasoning' },
        ].map(({ icon: Icon, title, desc }) => (
          <div key={title} className="p-4 rounded-xl bg-white dark:bg-slate-800 border border-slate-200 dark:border-slate-700">
            <Icon className="w-6 h-6 text-india-500 mb-2" />
            <h3 className="text-sm font-semibold text-slate-900 dark:text-white mb-1">{title}</h3>
            <p className="text-xs text-slate-500 dark:text-slate-400 leading-relaxed">{desc}</p>
          </div>
        ))}
      </div>

      <div className="p-4 rounded-xl bg-amber-50/60 dark:bg-amber-900/20 border border-amber-200/50 dark:border-amber-800/40">
        <p className="text-xs text-amber-700 dark:text-amber-300 leading-relaxed">
          <strong>Note:</strong> MoneyFollows is an independent prototype built for Hackday 1.0. It is not an official government service. Always verify information on official government portals.
        </p>
      </div>
    </div>
  );

  // ─── FOOTER ────────────────────────────────────────
  const Footer = () => (
    <footer className="border-t border-slate-200/60 dark:border-slate-800/60 bg-slate-50/50 dark:bg-slate-900/50">
      <div className="max-w-5xl mx-auto px-4 sm:px-6 py-8 space-y-4">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-2">
            <Landmark className="w-5 h-5 text-india-500" />
            <span className="text-sm font-semibold text-slate-700 dark:text-slate-300">{t('app.name', lang)}</span>
          </div>
          <div className="flex gap-4 text-xs text-slate-500 dark:text-slate-400">
            <button onClick={() => setPage('about')} className="hover:text-india-600 dark:hover:text-india-400 transition-colors">{t('footer.about', lang)}</button>
          </div>
        </div>
        <p className="text-xs text-slate-400 dark:text-slate-500 leading-relaxed max-w-3xl">
          {t('footer.disclaimer', lang)}
        </p>
        <p className="text-xs text-slate-400 dark:text-slate-500">
          Built for Hackday 1.0 — Tech for a Better Tomorrow
        </p>
      </div>
    </footer>
  );

  // ─── ERROR DISPLAY ─────────────────────────────────
  const ErrorDisplay = () => {
    if (!error) return null;
    return (
      <div className="max-w-2xl mx-auto px-4 py-6">
        <div className="p-4 rounded-xl bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 flex items-start gap-3">
          <AlertCircle className="w-5 h-5 text-red-500 shrink-0 mt-0.5" />
          <div>
            <p className="text-sm font-medium text-red-800 dark:text-red-300">{error}</p>
            <button
              onClick={() => { setError(null); handleSearch(); }}
              className="mt-2 text-xs font-medium text-red-600 dark:text-red-400 hover:text-red-700 underline"
            >
              Try again
            </button>
          </div>
          <button onClick={() => setError(null)} className="ml-auto">
            <X className="w-4 h-4 text-red-400" />
          </button>
        </div>
      </div>
    );
  };

  // ─── MAIN RENDER ───────────────────────────────────
  return (
    <div className="min-h-screen bg-white dark:bg-slate-950 text-slate-900 dark:text-white flex flex-col">
      <Header />
      
      <main className="flex-1">
        {page === 'about' ? (
          <About />
        ) : (
          <>
            {(page === 'home' || !results) && <Hero />}
            <SearchBox />
            <ErrorDisplay />
            {page === 'results' && <Results />}
            {page === 'home' && !loading && !results && <HowItWorks />}
          </>
        )}
      </main>

      <Footer />
    </div>
  );
}

export default App;
