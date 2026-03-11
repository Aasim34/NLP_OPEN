import { useState } from 'react';
import { Copy, Check } from 'lucide-react';
import { motion } from 'motion/react';

interface OutputCardProps {
  title: string;
  nativeTitle: string;
  content: string;
  gradient: string;
  icon: React.ReactNode;
  fontClass?: string;
  delay?: number;
}

export function OutputCard({ 
  title, 
  nativeTitle, 
  content, 
  gradient, 
  icon, 
  fontClass = '',
  delay = 0
}: OutputCardProps) {
  const [copied, setCopied] = useState(false);

  const handleCopy = () => {
    navigator.clipboard.writeText(content);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <motion.div
      initial={{ opacity: 0, y: 30 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5, delay }}
      className={`relative rounded-2xl p-6 shadow-lg hover:shadow-xl transition-all duration-300 hover:-translate-y-1 ${gradient} min-h-[200px] flex flex-col`}
    >
      <div className="flex items-start justify-between mb-4">
        <div className="flex items-center gap-3">
          <div className="text-2xl">{icon}</div>
          <div>
            <h3 className="text-xl font-semibold text-foreground">{title}</h3>
            <p className="text-sm text-muted-foreground">{nativeTitle}</p>
          </div>
        </div>
        <button
          onClick={handleCopy}
          className="p-2 rounded-lg bg-white/50 hover:bg-white/80 transition-all duration-200 hover:scale-105"
          aria-label="Copy text"
        >
          {copied ? (
            <Check className="w-5 h-5 text-accent" />
          ) : (
            <Copy className="w-5 h-5 text-secondary" />
          )}
        </button>
      </div>
      
      {content ? (
        <div className={`flex-1 ${fontClass}`}>
          <p className="text-lg leading-relaxed text-foreground whitespace-pre-wrap">
            {content}
          </p>
        </div>
      ) : (
        <div className="flex-1 flex items-center justify-center">
          <p className="text-muted-foreground italic">Waiting for conversion...</p>
        </div>
      )}
    </motion.div>
  );
}
