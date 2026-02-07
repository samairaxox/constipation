import React, { useState, useRef, useEffect } from 'react';
import { Send, User, Bot, Sparkles, TrendingUp, AlertCircle, ArrowRight } from 'lucide-react';
import { sendChatMessage } from '../api/trends';

const SUGGESTED_QUESTIONS = [
    "Why is 'Minimalist UX' declining?",
    "What is the saturation point for 'Short-form Video'?",
    "Compare 'NFTs' vs 'Generative Art' lifecycles.",
    "Which influencers are abandoning 'Flat Design'?"
];

const ChatAnalyst = () => {
    const [messages, setMessages] = useState([
        {
            id: 1,
            sender: 'ai',
            text: "Hello. I am your Trend Collapse Analyst. I track 150+ signals to predict when a trend will die. What would you like to investigate today?",
            type: 'text'
        }
    ]);
    const [input, setInput] = useState('');
    const [isTyping, setIsTyping] = useState(false);
    const messagesEndRef = useRef(null);

    const scrollToBottom = () => {
        messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
    };

    useEffect(() => {
        scrollToBottom();
    }, [messages]);

    const handleSend = async (text = input) => {
        if (!text.trim()) return;

        // 1. Add User Message
        const userMsg = { id: Date.now(), sender: 'user', text: text, type: 'text' };
        setMessages(prev => [...prev, userMsg]);
        setInput('');
        setIsTyping(true);

        // 2. Simulate AI Response
        try {
            const responseData = await sendChatMessage({ message: text });

            const aiMsg = {
                id: Date.now() + 1,
                sender: 'ai',
                text: responseData.answer,
                type: 'analysis',
                data: responseData // structured data
            };

            setMessages(prev => [...prev, aiMsg]);
        } catch (error) {
            setMessages(prev => [...prev, { id: Date.now() + 1, sender: 'ai', text: "System Error: Unable to access predictive models.", type: 'text' }]);
        } finally {
            setIsTyping(false);
        }
    };

    return (
        <div className="flex h-[calc(100vh-8rem)] gap-6">
            {/* Main Chat Area */}
            <div className="flex-1 flex flex-col bg-white rounded-xl shadow-sm border border-slate-200 overflow-hidden">

                {/* Chat History */}
                <div className="flex-1 overflow-y-auto p-6 space-y-6 bg-slate-50">
                    {messages.map((msg) => (
                        <div key={msg.id} className={`flex gap-4 ${msg.sender === 'user' ? 'flex-row-reverse' : ''}`}>

                            {/* Avatar */}
                            <div className={`w-10 h-10 flex-shrink-0 flex items-center justify-center rounded-full border ${msg.sender === 'ai'
                                    ? 'bg-indigo-100 border-indigo-200 text-indigo-600'
                                    : 'bg-white border-slate-200 text-slate-600'
                                }`}>
                                {msg.sender === 'ai' ? <Bot size={20} /> : <User size={20} />}
                            </div>

                            {/* Message content */}
                            <div className={`max-w-[80%] space-y-4`}>

                                {/* Bubble */}
                                <div className={`p-4 rounded-2xl text-sm leading-relaxed shadow-sm ${msg.sender === 'user'
                                        ? 'bg-indigo-600 text-white rounded-tr-none'
                                        : 'bg-white border border-slate-200 text-slate-700 rounded-tl-none'
                                    }`}>
                                    {msg.text}
                                </div>

                                {/* Structured Analysis View (Only for AI) */}
                                {msg.type === 'analysis' && msg.data && (
                                    <div className="bg-white rounded-xl border border-slate-200 overflow-hidden shadow-sm animate-in fade-in slide-in-from-bottom-2 duration-500">
                                        {/* Header */}
                                        <div className="bg-slate-50 px-4 py-2 border-b border-slate-100 flex items-center gap-2">
                                            <Sparkles size={14} className="text-indigo-600" />
                                            <span className="text-xs font-bold uppercase tracking-widest text-slate-500">Analysis Report</span>
                                        </div>

                                        <div className="p-5 grid gap-6">
                                            {/* Top Drivers */}
                                            <div>
                                                <h4 className="text-slate-800 text-xs font-bold uppercase mb-3 flex items-center gap-2">
                                                    <TrendingUp size={14} /> Top Decline Drivers
                                                </h4>
                                                <div className="flex flex-wrap gap-2">
                                                    {msg.data.drivers.map((driver, i) => (
                                                        <span key={i} className="px-2 py-1 bg-red-50 text-red-700 rounded text-xs font-medium border border-red-100">
                                                            {driver}
                                                        </span>
                                                    ))}
                                                </div>
                                            </div>

                                            {/* Evidence */}
                                            <div>
                                                <h4 className="text-slate-800 text-xs font-bold uppercase mb-3 flex items-center gap-2">
                                                    <AlertCircle size={14} /> Key Evidence
                                                </h4>
                                                <ul className="space-y-1">
                                                    {msg.data.evidence.map((item, i) => (
                                                        <li key={i} className="text-xs text-slate-600 flex items-start gap-2">
                                                            <span className="text-slate-400 mt-1">●</span> {item}
                                                        </li>
                                                    ))}
                                                </ul>
                                            </div>

                                            {/* Actions */}
                                            <div>
                                                <h4 className="text-slate-800 text-xs font-bold uppercase mb-3 flex items-center gap-2">
                                                    <ArrowRight size={14} /> Recommended Actions
                                                </h4>
                                                <div className="flex flex-wrap gap-2">
                                                    {msg.data.actions.map((action, i) => (
                                                        <span key={i} className="px-3 py-1 bg-green-50 text-green-700 rounded-full text-xs font-medium border border-green-100">
                                                            {action}
                                                        </span>
                                                    ))}
                                                </div>
                                            </div>
                                        </div>
                                    </div>
                                )}
                            </div>
                        </div>
                    ))}
                    {isTyping && (
                        <div className="flex gap-4">
                            <div className="w-10 h-10 bg-indigo-50 border border-indigo-100 rounded-full flex items-center justify-center text-indigo-400 animate-pulse">
                                <Bot size={20} />
                            </div>
                            <div className="p-4 bg-white border border-slate-100 rounded-2xl rounded-tl-none text-slate-400 text-xs font-medium flex items-center gap-2 shadow-sm">
                                Analyzing data streams...
                            </div>
                        </div>
                    )}
                    <div ref={messagesEndRef} />
                </div>

                {/* Input Area */}
                <div className="p-4 bg-white border-t border-slate-200">
                    {/* Chips */}
                    <div className="flex gap-2 mb-4 overflow-x-auto pb-2 scrollbar-hide">
                        {SUGGESTED_QUESTIONS.map((q, i) => (
                            <button
                                key={i}
                                onClick={() => handleSend(q)}
                                className="whitespace-nowrap px-3 py-1.5 bg-slate-50 border border-slate-200 rounded-full text-xs text-slate-600 hover:bg-slate-100 hover:border-slate-300 transition-colors"
                            >
                                {q}
                            </button>
                        ))}
                    </div>

                    <div className="relative">
                        <input
                            type="text"
                            value={input}
                            onChange={(e) => setInput(e.target.value)}
                            onKeyPress={(e) => e.key === 'Enter' && handleSend()}
                            placeholder="Ask about a trend..."
                            className="w-full pl-4 pr-12 py-3 bg-slate-50 border border-slate-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-indigo-500/20 focus:border-indigo-500 transition-all text-sm"
                        />
                        <button
                            onClick={() => handleSend()}
                            disabled={!input.trim()}
                            className="absolute right-2 top-2 p-1.5 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
                        >
                            <Send size={16} />
                        </button>
                    </div>
                </div>
            </div>

            {/* Side Panel: Signals Used */}
            <div className="w-80 bg-white rounded-xl shadow-sm border border-slate-200 hidden lg:flex flex-col overflow-hidden">
                <div className="p-4 border-b border-slate-100 bg-slate-50">
                    <h3 className="font-semibold text-slate-800 text-sm">Active Signals</h3>
                    <p className="text-xs text-slate-500 mt-1">Cross-referencing 4 data sources</p>
                </div>
                <div className="p-4 space-y-3 overflow-y-auto">
                    {[
                        { name: 'TikTok API', status: 'Live', latency: '24ms', color: 'text-green-600 bg-green-50 border-green-100' },
                        { name: 'Google Trends', status: 'Live', latency: '110ms', color: 'text-green-600 bg-green-50 border-green-100' },
                        { name: 'X / Twitter Sentiment', status: 'Degraded', latency: '400ms', color: 'text-yellow-600 bg-yellow-50 border-yellow-100' },
                        { name: 'Instagram Engagement', status: 'Live', latency: '32ms', color: 'text-green-600 bg-green-50 border-green-100' }
                    ].map((signal, i) => (
                        <div key={i} className="flex items-center justify-between p-3 border border-slate-100 rounded-lg bg-white shadow-sm hover:shadow-md transition-shadow">
                            <div>
                                <div className="text-xs font-semibold text-slate-700">{signal.name}</div>
                                <div className="text-[10px] text-slate-400 mt-1">Latency: {signal.latency}</div>
                            </div>
                            <div className={`text-[10px] font-bold px-2 py-0.5 rounded border ${signal.color}`}>
                                {signal.status}
                            </div>
                        </div>
                    ))}

                    <div className="mt-8 pt-6 border-t border-slate-100 text-center">
                        <div className="text-[10px] text-slate-400 font-medium uppercase tracking-widest mb-2">System Status</div>
                        <div className="inline-flex items-center gap-2 px-3 py-1 bg-indigo-50 text-indigo-600 text-xs font-semibold rounded-full border border-indigo-100">
                            <span className="w-1.5 h-1.5 bg-indigo-500 rounded-full animate-pulse"></span>
                            Operational
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default ChatAnalyst;
