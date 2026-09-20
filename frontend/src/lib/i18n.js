// Internationalization - English and Hindi translations

const translations = {
  en: {
    // Header
    'app.name': 'MoneyFollows',
    'app.tagline': 'Find the government benefits you may be eligible for',
    
    // Hero
    'hero.title': 'Find Government Schemes',
    'hero.title.highlight': 'You May Be Eligible For',
    'hero.subtitle': 'Describe your situation in plain language. MoneyFollows searches government sources and helps you understand relevant schemes, eligibility, documents, and application steps.',
    'hero.cta': 'Find My Schemes',
    'hero.cta.secondary': 'How It Works',
    
    // Trust indicators
    'trust.official': 'Official-source focused',
    'trust.ai': 'AI-assisted discovery',
    'trust.eligibility': 'Eligibility explained',
    'trust.sources': 'Source links provided',
    
    // Search
    'search.placeholder': 'Tell us what you are looking for...',
    'search.button': 'Search Schemes',
    'search.examples.title': 'Try asking:',
    'search.example.1': 'I am a B.Tech student from UP. What scholarships can I apply for?',
    'search.example.2': 'My family income is 2 lakh. What government benefits can I get?',
    'search.example.3': 'I am a farmer in Uttar Pradesh. What schemes may help me?',
    'search.example.4': 'What government schemes are available for women entrepreneurs?',
    
    // Profile
    'profile.title': 'Your Profile',
    'profile.subtitle': 'Optional — helps us find more relevant schemes',
    'profile.age': 'Age',
    'profile.state': 'State',
    'profile.education': 'Education',
    'profile.occupation': 'Occupation',
    'profile.income': 'Annual Family Income (₹)',
    'profile.gender': 'Gender',
    'profile.category': 'Category',
    'profile.disability': 'Disability',
    'profile.toggle': 'Add Profile Details',
    'profile.hide': 'Hide Profile',
    
    // Loading states
    'loading.understanding': 'Understanding your question...',
    'loading.searching': 'Searching government sources...',
    'loading.reading': 'Reading relevant information...',
    'loading.checking': 'Checking eligibility...',
    'loading.preparing': 'Preparing results...',
    
    // Results
    'results.found': 'We found {count} potentially relevant scheme(s)',
    'results.none': "We couldn't find a sufficiently relevant match from the sources we checked.",
    'results.refine': 'Try refining your question or adding more details.',
    'results.summary': 'Summary',
    'results.sources.checked': 'Sources checked',
    'results.sources.official': 'Official sources',
    
    // Scheme card
    'scheme.benefits': 'Benefits',
    'scheme.eligibility': 'Eligibility',
    'scheme.documents': 'Required Documents',
    'scheme.application': 'How to Apply',
    'scheme.source': 'Official Source',
    'scheme.details': 'View Details',
    'scheme.why.matches': 'Why this may match',
    'scheme.unknown': 'Needs verification',
    'scheme.not.matched': "Doesn't match",
    
    // Status
    'status.LIKELY_ELIGIBLE': 'Likely Eligible',
    'status.POSSIBLY_ELIGIBLE': 'Possibly Eligible',
    'status.NEEDS_MORE_INFORMATION': 'Needs More Info',
    'status.LIKELY_NOT_ELIGIBLE': 'Likely Not Eligible',
    'status.UNVERIFIED': 'Unverified',
    
    // Chat
    'chat.placeholder': 'Ask a follow-up question...',
    'chat.send': 'Send',
    
    // How it works
    'how.title': 'How It Works',
    'how.step.1.title': 'Describe Your Situation',
    'how.step.1.desc': 'Enter your question in plain language — no need to know official scheme names.',
    'how.step.2.title': 'We Search Government Sources',
    'how.step.2.desc': 'AI searches across government portals and prioritizes official sources.',
    'how.step.3.title': 'Get Personalized Results',
    'how.step.3.desc': 'See schemes that match your profile, with eligibility analysis and source links.',
    
    // Footer
    'footer.disclaimer': 'MoneyFollows is an independent AI-powered discovery prototype. Information is retrieved from available sources and may change. Always verify eligibility, documents, deadlines, and application requirements on the official government portal before applying.',
    'footer.about': 'About',
    'footer.how': 'How It Works',
    'footer.privacy': 'Privacy',
    
    // About
    'about.title': 'About MoneyFollows',
    'about.desc': 'MoneyFollows is an AI-powered government scheme discovery and eligibility assistant built to help citizens find relevant government benefits. It uses web search to dynamically retrieve information from government sources, extract scheme details, and check eligibility.',
    
    // Misc
    'theme.light': 'Light',
    'theme.dark': 'Dark',
    'lang.en': 'English',
    'lang.hi': 'हिन्दी',
    'verify.reminder': 'Always verify the latest requirements on the official government source before applying.',
    'source.official': 'Official Source',
    'source.secondary': 'Secondary Source',
    'source.view': 'View official source',
  },
  hi: {
    // Header
    'app.name': 'MoneyFollows',
    'app.tagline': 'जानें कि आप किन सरकारी योजनाओं के लिए पात्र हो सकते हैं',
    
    // Hero
    'hero.title': 'सरकारी योजनाएं खोजें',
    'hero.title.highlight': 'जिनके लिए आप पात्र हो सकते हैं',
    'hero.subtitle': 'अपनी स्थिति सरल भाषा में बताएं। MoneyFollows सरकारी स्रोतों में खोज करता है और आपको संबंधित योजनाओं, पात्रता, दस्तावेज़ों और आवेदन प्रक्रिया को समझने में मदद करता है।',
    'hero.cta': 'योजनाएं खोजें',
    'hero.cta.secondary': 'कैसे काम करता है',
    
    // Trust indicators
    'trust.official': 'सरकारी स्रोत आधारित',
    'trust.ai': 'AI-सहायता प्राप्त',
    'trust.eligibility': 'पात्रता स्पष्टीकरण',
    'trust.sources': 'स्रोत लिंक उपलब्ध',
    
    // Search
    'search.placeholder': 'बताएं कि आप क्या खोज रहे हैं...',
    'search.button': 'योजनाएं खोजें',
    'search.examples.title': 'यह पूछ कर देखें:',
    'search.example.1': 'मैं UP से B.Tech छात्र हूं। मुझे कौन सी छात्रवृत्ति मिल सकती है?',
    'search.example.2': 'मेरी पारिवारिक आय 2 लाख है। सरकारी लाभ क्या मिल सकते हैं?',
    'search.example.3': 'मैं उत्तर प्रदेश में किसान हूं। कौन सी योजनाएं मदद कर सकती हैं?',
    'search.example.4': 'महिला उद्यमियों के लिए कौन सी सरकारी योजनाएं हैं?',
    
    // Profile
    'profile.title': 'आपकी जानकारी',
    'profile.subtitle': 'वैकल्पिक — बेहतर योजनाएं खोजने में मदद करता है',
    'profile.age': 'आयु',
    'profile.state': 'राज्य',
    'profile.education': 'शिक्षा',
    'profile.occupation': 'पेशा',
    'profile.income': 'वार्षिक पारिवारिक आय (₹)',
    'profile.gender': 'लिंग',
    'profile.category': 'वर्ग',
    'profile.disability': 'विकलांगता',
    'profile.toggle': 'प्रोफ़ाइल जोड़ें',
    'profile.hide': 'प्रोफ़ाइल छुपाएं',
    
    // Loading states
    'loading.understanding': 'आपका प्रश्न समझ रहे हैं...',
    'loading.searching': 'सरकारी स्रोतों में खोज रहे हैं...',
    'loading.reading': 'संबंधित जानकारी पढ़ रहे हैं...',
    'loading.checking': 'पात्रता जांच रहे हैं...',
    'loading.preparing': 'परिणाम तैयार कर रहे हैं...',
    
    // Results
    'results.found': '{count} संभावित प्रासंगिक योजना(एं) मिलीं',
    'results.none': 'हम जिन स्रोतों की जांच कर पाए उनसे पर्याप्त प्रासंगिक योजना नहीं मिली।',
    'results.refine': 'अपना प्रश्न विस्तार से लिखें या अधिक विवरण जोड़ें।',
    'results.summary': 'सारांश',
    'results.sources.checked': 'जांचे गए स्रोत',
    'results.sources.official': 'सरकारी स्रोत',
    
    // Scheme card
    'scheme.benefits': 'लाभ',
    'scheme.eligibility': 'पात्रता',
    'scheme.documents': 'आवश्यक दस्तावेज़',
    'scheme.application': 'आवेदन कैसे करें',
    'scheme.source': 'आधिकारिक स्रोत',
    'scheme.details': 'विवरण देखें',
    'scheme.why.matches': 'यह क्यों मेल खाता है',
    'scheme.unknown': 'सत्यापन आवश्यक',
    'scheme.not.matched': 'मेल नहीं खाता',
    
    // Status
    'status.LIKELY_ELIGIBLE': 'पात्र हो सकते हैं',
    'status.POSSIBLY_ELIGIBLE': 'संभावित पात्र',
    'status.NEEDS_MORE_INFORMATION': 'और जानकारी चाहिए',
    'status.LIKELY_NOT_ELIGIBLE': 'पात्र नहीं लगता',
    'status.UNVERIFIED': 'असत्यापित',
    
    // Chat
    'chat.placeholder': 'अनुवर्ती प्रश्न पूछें...',
    'chat.send': 'भेजें',
    
    // How it works
    'how.title': 'कैसे काम करता है',
    'how.step.1.title': 'अपनी स्थिति बताएं',
    'how.step.1.desc': 'सरल भाषा में प्रश्न लिखें — योजना का आधिकारिक नाम जानने की ज़रूरत नहीं।',
    'how.step.2.title': 'हम सरकारी स्रोत खोजते हैं',
    'how.step.2.desc': 'AI सरकारी पोर्टलों पर खोज करता है और आधिकारिक स्रोतों को प्राथमिकता देता है।',
    'how.step.3.title': 'व्यक्तिगत परिणाम पाएं',
    'how.step.3.desc': 'अपनी प्रोफ़ाइल से मेल खाती योजनाएं देखें, पात्रता विश्लेषण और स्रोत लिंक के साथ।',
    
    // Footer
    'footer.disclaimer': 'MoneyFollows एक स्वतंत्र AI-संचालित खोज प्रोटोटाइप है। जानकारी उपलब्ध स्रोतों से प्राप्त होती है और बदल सकती है। आवेदन करने से पहले हमेशा आधिकारिक सरकारी पोर्टल पर पात्रता, दस्तावेज़, समय सीमा और आवेदन आवश्यकताओं की पुष्टि करें।',
    'footer.about': 'बारे में',
    'footer.how': 'कैसे काम करता है',
    'footer.privacy': 'गोपनीयता',
    
    // About
    'about.title': 'MoneyFollows के बारे में',
    'about.desc': 'MoneyFollows एक AI-संचालित सरकारी योजना खोज और पात्रता सहायक है जो नागरिकों को संबंधित सरकारी लाभ खोजने में मदद करने के लिए बनाया गया है।',
    
    // Misc
    'theme.light': 'लाइट',
    'theme.dark': 'डार्क',
    'lang.en': 'English',
    'lang.hi': 'हिन्दी',
    'verify.reminder': 'आवेदन करने से पहले हमेशा आधिकारिक सरकारी स्रोत पर नवीनतम आवश्यकताओं की पुष्टि करें।',
    'source.official': 'आधिकारिक स्रोत',
    'source.secondary': 'द्वितीयक स्रोत',
    'source.view': 'आधिकारिक स्रोत देखें',
  },
};

export function t(key, lang, params) {
  let text = translations[lang]?.[key] || translations['en'][key] || key;
  if (params) {
    Object.entries(params).forEach(([k, v]) => {
      text = text.replace(`{${k}}`, String(v));
    });
  }
  return text;
}

export default translations;
