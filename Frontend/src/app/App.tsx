import { useState } from 'react';
import { Navigation } from './components/Navigation';
import { OutputCard } from './components/OutputCard';
import { FeatureCard } from './components/FeatureCard';
import { ArrowRight, X, Sparkles, Globe, Type, Languages, Zap, Shield, Target } from 'lucide-react';
import { motion } from 'motion/react';

export default function App() {
  const [inputText, setInputText] = useState('');
  const [outputs, setOutputs] = useState({
    hindi: '',
    finglish: '',
    english: ''
  });
  const [isLoading, setIsLoading] = useState(false);

  const exampleText = "kal meeting hai office me, please jaldi aana";

  const handleTryExample = () => {
    setInputText(exampleText);
  };

  const handleClear = () => {
    setInputText('');
    setOutputs({ hindi: '', finglish: '', english: '' });
  };

  const handleConvert = async () => {
    if (!inputText.trim()) return;

    setIsLoading(true);
    
    try {
      // Call the FastAPI backend
      const response = await fetch('http://localhost:8000/convert', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ text: inputText }),
      });

      if (!response.ok) {
        throw new Error(`API error: ${response.status}`);
      }

      const data = await response.json();
      
      setOutputs({
        hindi: data.hindi,
        finglish: data.finglish,
        english: data.english,
      });
    } catch (error) {
      console.error('Conversion error:', error);
      // Show error to user
      setOutputs({
        hindi: '❌ Error: Could not connect to backend',
        finglish: 'Please make sure the FastAPI server is running on port 8000',
        english: 'Run: uvicorn main:app --reload',
      });
    } finally {
      setIsLoading(false);
    }
  };

  const charCount = inputText.length;

  return (
    <div className="min-h-screen bg-background" style={{ fontFamily: 'Inter, sans-serif' }}>
      <Navigation />

      {/* Hero Section */}
      <section id="home" className="relative pt-24 pb-16 px-4 overflow-hidden">
        {/* Decorative Background Pattern */}
        <div className="absolute inset-0 opacity-[0.03]">
          <div className="absolute top-20 left-10 w-64 h-64 bg-primary rounded-full blur-3xl"></div>
          <div className="absolute top-40 right-20 w-96 h-96 bg-accent rounded-full blur-3xl"></div>
          <div className="absolute bottom-20 left-1/2 w-72 h-72 bg-primary rounded-full blur-3xl"></div>
        </div>

        <div className="max-w-5xl mx-auto relative z-10">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6 }}
            className="text-center mb-12"
          >
            <h1 
              className="text-5xl md:text-6xl lg:text-7xl font-bold mb-4 bg-gradient-to-r from-[#FF6B35] via-[#F7931E] to-[#FF6B35] bg-clip-text text-transparent"
              style={{ fontFamily: 'Poppins, sans-serif' }}
            >
              Indian Language Converter
            </h1>
            <p className="text-xl md:text-2xl text-muted-foreground max-w-3xl mx-auto">
              Transform Hinglish into Hindi, Finglish & English instantly
            </p>
          </motion.div>

          {/* Input Area */}
          <motion.div
            initial={{ opacity: 0, y: 30 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, delay: 0.2 }}
            className="relative mb-8"
          >
            <div className="relative">
              <textarea
                value={inputText}
                onChange={(e) => setInputText(e.target.value)}
                placeholder="Type your Hinglish text here... (e.g., 'kal meeting hai office me')"
                className="w-full h-48 px-6 py-4 rounded-2xl bg-card border-2 border-border focus:border-primary focus:ring-4 focus:ring-primary/20 outline-none transition-all duration-300 resize-none text-lg shadow-lg"
                style={{ fontFamily: 'Inter, sans-serif' }}
              />
              {inputText && (
                <button
                  onClick={handleClear}
                  className="absolute top-4 right-4 p-2 rounded-lg bg-muted/50 hover:bg-muted transition-all duration-200"
                  aria-label="Clear text"
                >
                  <X className="w-5 h-5" />
                </button>
              )}
              <div className="absolute bottom-4 right-4 text-sm text-muted-foreground">
                {charCount} characters
              </div>
            </div>

            <div className="flex flex-col sm:flex-row gap-3 mt-4 items-center justify-center">
              <button
                onClick={handleTryExample}
                className="px-6 py-2 rounded-lg border-2 border-primary text-primary hover:bg-primary hover:text-white transition-all duration-300 font-medium"
              >
                Try Example
              </button>
              
              <button
                onClick={handleConvert}
                disabled={!inputText.trim() || isLoading}
                className="group relative px-8 py-3 rounded-xl bg-gradient-to-r from-[#FF6B35] to-[#F7931E] text-white font-semibold shadow-lg hover:shadow-xl hover:scale-105 transition-all duration-300 disabled:opacity-50 disabled:cursor-not-allowed disabled:hover:scale-100 min-w-[200px]"
              >
                {isLoading ? (
                  <span className="flex items-center gap-2">
                    <div className="w-5 h-5 border-2 border-white/30 border-t-white rounded-full animate-spin"></div>
                    Converting...
                  </span>
                ) : (
                  <span className="flex items-center gap-2">
                    Convert
                    <ArrowRight className="w-5 h-5 group-hover:translate-x-1 transition-transform" />
                  </span>
                )}
              </button>
            </div>
          </motion.div>

          {/* Output Cards */}
          {(outputs.hindi || outputs.finglish || outputs.english) && (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mt-12">
              <OutputCard
                title="Hindi"
                nativeTitle="हिंदी"
                content={outputs.hindi}
                gradient="bg-gradient-to-br from-[#FFF8F3] to-white"
                icon={<Languages className="w-6 h-6 text-[#FF6B35]" />}
                fontClass="font-['Noto_Sans_Devanagari']"
                delay={0.1}
              />
              <OutputCard
                title="Finglish"
                nativeTitle="Roman Hindi"
                content={outputs.finglish}
                gradient="bg-gradient-to-br from-blue-50 to-white"
                icon={<Type className="w-6 h-6 text-blue-600" />}
                delay={0.2}
              />
              <OutputCard
                title="English"
                nativeTitle="Translation"
                content={outputs.english}
                gradient="bg-gradient-to-br from-green-50 to-white"
                icon={<Globe className="w-6 h-6 text-green-600" />}
                delay={0.3}
              />
            </div>
          )}
        </div>
      </section>

      {/* How It Works Section */}
      <section className="py-16 px-4 bg-card/30">
        <div className="max-w-5xl mx-auto">
          <motion.h2
            initial={{ opacity: 0 }}
            whileInView={{ opacity: 1 }}
            viewport={{ once: true }}
            className="text-4xl font-bold text-center mb-12"
            style={{ fontFamily: 'Poppins, sans-serif' }}
          >
            How It Works
          </motion.h2>
          
          <div className="flex flex-col md:flex-row items-center justify-center gap-8 md:gap-4">
            <motion.div
              initial={{ opacity: 0, x: -20 }}
              whileInView={{ opacity: 1, x: 0 }}
              viewport={{ once: true }}
              transition={{ delay: 0.1 }}
              className="flex flex-col items-center text-center"
            >
              <div className="w-16 h-16 rounded-full bg-gradient-to-br from-[#FF6B35] to-[#F7931E] flex items-center justify-center text-white font-bold text-2xl mb-4">
                1
              </div>
              <h3 className="font-semibold text-lg mb-2">Input Hinglish</h3>
              <p className="text-muted-foreground text-sm max-w-[200px]">
                Type or paste your mixed Hindi-English text
              </p>
            </motion.div>

            <div className="hidden md:block">
              <ArrowRight className="w-8 h-8 text-primary" />
            </div>

            <motion.div
              initial={{ opacity: 0, x: -20 }}
              whileInView={{ opacity: 1, x: 0 }}
              viewport={{ once: true }}
              transition={{ delay: 0.2 }}
              className="flex flex-col items-center text-center"
            >
              <div className="w-16 h-16 rounded-full bg-gradient-to-br from-purple-500 to-purple-600 flex items-center justify-center text-white font-bold text-2xl mb-4">
                2
              </div>
              <h3 className="font-semibold text-lg mb-2">AI Processing</h3>
              <p className="text-muted-foreground text-sm max-w-[200px]">
                Advanced NLP algorithms analyze and convert
              </p>
            </motion.div>

            <div className="hidden md:block">
              <ArrowRight className="w-8 h-8 text-primary" />
            </div>

            <motion.div
              initial={{ opacity: 0, x: -20 }}
              whileInView={{ opacity: 1, x: 0 }}
              viewport={{ once: true }}
              transition={{ delay: 0.3 }}
              className="flex flex-col items-center text-center"
            >
              <div className="w-16 h-16 rounded-full bg-gradient-to-br from-[#10B981] to-green-600 flex items-center justify-center text-white font-bold text-2xl mb-4">
                3
              </div>
              <h3 className="font-semibold text-lg mb-2">Three Outputs</h3>
              <p className="text-muted-foreground text-sm max-w-[200px]">
                Get Hindi, Finglish, and English versions
              </p>
            </motion.div>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section id="features" className="py-16 px-4">
        <div className="max-w-6xl mx-auto">
          <motion.h2
            initial={{ opacity: 0 }}
            whileInView={{ opacity: 1 }}
            viewport={{ once: true }}
            className="text-4xl font-bold text-center mb-12"
            style={{ fontFamily: 'Poppins, sans-serif' }}
          >
            Why Choose Us?
          </motion.h2>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            <FeatureCard
              icon="🚀"
              title="Instant Conversion"
              description="Lightning-fast NLP processing delivers results in seconds. No waiting, just instant transformations."
              delay={0.1}
            />
            <FeatureCard
              icon="🎯"
              title="Accurate Results"
              description="ML-powered transliteration and translation ensure high accuracy for both formal and casual text."
              delay={0.2}
            />
            <FeatureCard
              icon="🔒"
              title="Privacy First"
              description="Your data stays private. We process everything securely without storing your personal information."
              delay={0.3}
            />
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="bg-card border-t border-border py-8 px-4 mt-16">
        <div className="max-w-6xl mx-auto">
          <div className="flex flex-col md:flex-row items-center justify-between gap-4">
            <div className="flex items-center gap-2">
              <div className="w-8 h-8 rounded-lg bg-gradient-to-br from-[#FF6B35] to-[#F7931E] flex items-center justify-center">
                <span className="text-white font-bold">LC</span>
              </div>
              <span className="text-sm text-muted-foreground">
                Built with React & Tailwind CSS
              </span>
            </div>

            <div className="flex gap-6 text-sm text-muted-foreground">
              <a href="#" className="hover:text-primary transition-colors">Privacy</a>
              <a href="#" className="hover:text-primary transition-colors">Terms</a>
              <a href="#" className="hover:text-primary transition-colors">Contact</a>
            </div>

            <div className="text-sm text-muted-foreground">
              © 2026 Language Converter
            </div>
          </div>
        </div>
      </footer>
    </div>
  );
}
