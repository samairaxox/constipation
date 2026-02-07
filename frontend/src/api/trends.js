import { CONFIG } from '../config';
import axios from 'axios';

// --- DUMMY DATA ---
const DUMMY_TRENDS = [
    { id: 1, name: 'Minimalist UX', platform: 'Web Design', stage: 'Early Decline', health: 65, probability: 'High', eta: '120 days' },
    { id: 2, name: 'Short-form Video', platform: 'TikTok/Reels', stage: 'Peak', health: 88, probability: 'Low', eta: '365+ days' },
    { id: 3, name: 'NFT Collectibles', platform: 'Crypto', stage: 'Dead', health: 12, probability: 'Critical', eta: 'Expired' },
    { id: 4, name: 'Flat Design', platform: 'UI', stage: 'Collapse', health: 34, probability: 'Very High', eta: '45 days' },
    { id: 5, name: 'Neumorphism', platform: 'Dribbble', stage: 'Collapse', health: 28, probability: 'High', eta: '60 days' },
    { id: 6, name: 'Voice Search', platform: 'SEO', stage: 'Growth', health: 92, probability: 'Low', eta: 'Unknown' },
    { id: 7, name: 'Metaverse Real Estate', platform: 'VR', stage: 'Dead', health: 15, probability: 'Critical', eta: 'Expired' },
    { id: 8, name: 'Generative AI Art', platform: 'Digital Art', stage: 'Peak', health: 85, probability: 'Medium', eta: '200 days' },
];

const DUMMY_DETAILS = {
    name: 'Minimalist UX',
    stage: 'Early Decline',
    probability: '78%',
    eta: '6 days',
    confidence: 'High',
    kpi: {
        engagement: '-14.2%',
        influencers: '-28%',
        sentiment: 'Neutral → Neg',
        saturation: '92/100'
    },
    drivers: [
        { name: 'Engagement Drop', impact: 'High', evidence: ['Avg likes down 40%', 'Comments per post down 25%'] },
        { name: 'Influencer Disengagement', impact: 'High', evidence: ['Top 3 creators stopped posting', 'Sponsored content ROI -50%'] },
        { name: 'Sentiment Fatigue', impact: 'Medium', evidence: ['"Boring" keyword up 300%', 'Increase in negative memes'] },
        { name: 'Content Saturation', impact: 'Medium', evidence: ['Post volume up 20%', 'Engagement per post down 60%'] },
        { name: 'Algorithmic Boost Drop', impact: 'Low', evidence: ['Discover page visibility -15%', 'Video completion rate down'] },
    ],
    narrative: 'Minimalist UX is experiencing a critical **Engagement Drop** driven primarily by audience fatigue and influencer abandonment. Our analysis detects a rapid shift in sentiment from "aspirational" to "repetitive," suggesting the trend has reached **Point of Saturation**. The algorithm has already begun deprecating this content in favor of fresher alternatives.',
};

// --- API ADAPTER ---

export const getTrends = async () => {
    if (CONFIG.DEMO_MODE) {
        return new Promise((resolve) => setTimeout(() => resolve(DUMMY_TRENDS), 500));
    }
    const response = await axios.get(`${CONFIG.API_BASE_URL}/trend-data`);
    return response.data;
};

export const getTrendDetails = async (id) => {
    if (CONFIG.DEMO_MODE) {
        // Return standard dummy details but override name based on ID if available in list
        const basicInfo = DUMMY_TRENDS.find(t => t.id == id);
        const details = { ...DUMMY_DETAILS };
        if (basicInfo) details.name = basicInfo.name;
        return new Promise((resolve) => setTimeout(() => resolve(details), 600));
    }
    const response = await axios.get(`${CONFIG.API_BASE_URL}/trend-data/${id}`);
    return response.data;
};

export const sendChatMessage = async (payload) => {
    if (CONFIG.DEMO_MODE) {
        // We already have a dummy generator in the Chat UI, but if you want to centralize it:
        return new Promise((resolve) => {
            setTimeout(() => resolve({
                answer: "Simulated backend response for: " + payload.message,
                drivers: ["Simulated Driver 1", "Simulated Driver 2"],
                evidence: ["Evidence A", "Evidence B"],
                actions: ["Action 1", "Action 2"]
            }), 1000);
        });
    }
    const response = await axios.post(`${CONFIG.API_BASE_URL}/chat-analysis`, payload);
    return response.data;
};

export const simulateWhatIf = async (payload) => {
    if (CONFIG.DEMO_MODE) {
        return new Promise((resolve) => setTimeout(() => resolve({ result: "Simulation Complete", impact: "High" }), 800));
    }
    const response = await axios.post(`${CONFIG.API_BASE_URL}/what-if-simulate`, payload);
    return response.data;
};
