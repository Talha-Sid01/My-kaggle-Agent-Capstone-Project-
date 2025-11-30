import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import {
  Stethoscope,
  AlertCircle,
  Home,
  Activity,
  Search,
  ChevronRight,
  ShieldCheck,
  Loader2,
  Send
} from 'lucide-react';

const STEPS = [
  { id: 'extract', text: 'Extracting Symptoms...' },
  { id: 'analyze', text: 'Analyzing Severity...' },
  { id: 'fetch', text: 'Fetching Trusted Info...' },
];

export default function App() {
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const [currentStep, setCurrentStep] = useState(0);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!input.trim()) return;

    setLoading(true);
    setResult(null);
    setError(null);
    setCurrentStep(0);

    // Simulate steps visualizer
    const stepInterval = setInterval(() => {
      setCurrentStep((prev) => (prev < STEPS.length - 1 ? prev + 1 : prev));
    }, 1500);

    try {
      const response = await fetch('http://localhost:8000/api/triage', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: input }),
      });

      if (!response.ok) {
        throw new Error('Failed to process request');
      }

      const data = await response.json();
      clearInterval(stepInterval);
      setCurrentStep(STEPS.length); // Done

      // Small delay to show the last step
      setTimeout(() => {
        setResult(data);
        setLoading(false);
      }, 800);

    } catch (err) {
      clearInterval(stepInterval);
      setError(err.message);
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-slate-50 text-slate-900 font-sans selection:bg-emerald-100">
      {/* Hero Section */}
      <header className="bg-white border-b border-slate-200 sticky top-0 z-10">
        <div className="max-w-4xl mx-auto px-4 py-4 flex items-center gap-2">
          <div className="bg-emerald-600 p-2 rounded-lg">
            <Activity className="w-6 h-6 text-white" />
          </div>
          <h1 className="text-xl font-bold tracking-tight text-slate-800">Healthage: AI Symptom Triage</h1>
        </div>
      </header>

      <main className="max-w-3xl mx-auto px-4 py-12 space-y-8">

        {/* Chat Interface */}
        <section className="text-center space-y-6">
          <h2 className="text-3xl font-extrabold text-slate-800 tracking-tight">
            How are you feeling today?
          </h2>
          <p className="text-slate-500 max-w-lg mx-auto">
            Describe your symptoms in detail. Our AI agents will analyze them and guide you to the right care.
          </p>

          <form onSubmit={handleSubmit} className="relative max-w-xl mx-auto">
            <input
              type="text"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              placeholder="e.g., I have a headache and a mild fever..."
              className="w-full pl-6 pr-14 py-4 rounded-2xl border border-slate-200 shadow-sm focus:ring-4 focus:ring-emerald-100 focus:border-emerald-500 outline-none transition-all text-lg"
              disabled={loading}
            />
            <button
              type="submit"
              disabled={loading || !input.trim()}
              className="absolute right-2 top-2 bottom-2 bg-emerald-600 hover:bg-emerald-700 text-white p-3 rounded-xl transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {loading ? <Loader2 className="w-5 h-5 animate-spin" /> : <Send className="w-5 h-5" />}
            </button>
          </form>
        </section>

        {/* Process Visualizer */}
        <AnimatePresence mode="wait">
          {loading && (
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -20 }}
              className="max-w-xl mx-auto bg-white rounded-2xl p-6 shadow-lg border border-slate-100"
            >
              <div className="space-y-4">
                {STEPS.map((step, index) => (
                  <motion.div
                    key={step.id}
                    initial={{ opacity: 0.5 }}
                    animate={{
                      opacity: index === currentStep ? 1 : 0.4,
                      scale: index === currentStep ? 1.02 : 1
                    }}
                    className="flex items-center gap-3"
                  >
                    <div className={`w-8 h-8 rounded-full flex items-center justify-center ${index < currentStep ? 'bg-emerald-100 text-emerald-600' :
                      index === currentStep ? 'bg-blue-100 text-blue-600 animate-pulse' :
                        'bg-slate-100 text-slate-400'
                      }`}>
                      {index < currentStep ? <ShieldCheck className="w-4 h-4" /> :
                        index === currentStep ? <Activity className="w-4 h-4" /> :
                          <div className="w-2 h-2 rounded-full bg-current" />}
                    </div>
                    <span className={`font-medium ${index === currentStep ? 'text-slate-800' : 'text-slate-400'
                      }`}>
                      {step.text}
                    </span>
                  </motion.div>
                ))}
              </div>
            </motion.div>
          )}
        </AnimatePresence>

        {/* Results */}
        <AnimatePresence>
          {result && !loading && (
            <motion.div
              initial={{ opacity: 0, scale: 0.95 }}
              animate={{ opacity: 1, scale: 1 }}
              className="space-y-6"
            >
              {/* Triage Card */}
              <TriageCard result={result.triage_result} />

              {/* Symptom Summary */}
              <div className="bg-white rounded-2xl p-6 shadow-sm border border-slate-200">
                <h3 className="text-sm font-semibold text-slate-400 uppercase tracking-wider mb-4">Analyzed Symptoms</h3>
                <div className="flex flex-wrap gap-2">
                  {result.symptom_analysis.symptoms.map((s, i) => (
                    <span key={i} className="px-3 py-1 bg-slate-100 text-slate-700 rounded-full text-sm font-medium">
                      {s}
                    </span>
                  ))}
                </div>
                {result.symptom_analysis.severity && (
                  <p className="mt-4 text-sm text-slate-600">
                    <span className="font-medium">Detected Severity:</span> {result.symptom_analysis.severity}
                  </p>
                )}
              </div>

              {/* Info Cards */}
              {result.trusted_info.length > 0 && (
                <div className="grid md:grid-cols-2 gap-4">
                  {result.trusted_info.map((info, i) => (
                    <a
                      key={i}
                      href={info.url}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="block bg-white p-6 rounded-2xl border border-slate-200 hover:border-emerald-500 hover:shadow-md transition-all group"
                    >
                      <div className="flex items-start justify-between mb-2">
                        <h4 className="font-semibold text-slate-800 group-hover:text-emerald-600 transition-colors">
                          {info.title}
                        </h4>
                        <Search className="w-4 h-4 text-slate-400" />
                      </div>
                      <p className="text-sm text-slate-500 line-clamp-3">
                        {info.summary}
                      </p>
                    </a>
                  ))}
                </div>
              )}
            </motion.div>
          )}
        </AnimatePresence>

        {error && (
          <div className="p-4 bg-rose-50 text-rose-600 rounded-xl text-center">
            {error}
          </div>
        )}

      </main>
    </div>
  );
}

function TriageCard({ result }) {
  const { triage, reason } = result;

  const config = {
    EMERGENCY: {
      color: 'bg-rose-600',
      lightColor: 'bg-rose-50',
      textColor: 'text-rose-700',
      icon: AlertCircle,
      title: 'Emergency Care Needed',
      animation: 'animate-pulse'
    },
    SEE_DOCTOR: {
      color: 'bg-amber-500',
      lightColor: 'bg-amber-50',
      textColor: 'text-amber-700',
      icon: Stethoscope,
      title: 'Consult a Doctor',
      animation: ''
    },
    SELF_CARE: {
      color: 'bg-emerald-500',
      lightColor: 'bg-emerald-50',
      textColor: 'text-emerald-700',
      icon: Home,
      title: 'Self-Care Recommended',
      animation: ''
    }
  };

  const theme = config[triage] || config.SEE_DOCTOR;
  const Icon = theme.icon;

  return (
    <div className={`${theme.lightColor} border border-transparent rounded-3xl p-8 text-center relative overflow-hidden shadow-sm`}>
      <div className={`mx-auto w-16 h-16 ${theme.color} rounded-full flex items-center justify-center mb-6 shadow-lg ${theme.animation}`}>
        <Icon className="w-8 h-8 text-white" />
      </div>
      <h2 className={`text-2xl font-bold ${theme.textColor} mb-2`}>
        {theme.title}
      </h2>
      <p className="text-slate-600 max-w-lg mx-auto leading-relaxed">
        {reason}
      </p>
    </div>
  );
}
