# mood-import { useState, useRef, useEffect } from 'react';
import { Button } from "./components/ui/button";
import { Card, CardContent, CardHeader, CardTitle, CardFooter } from "./components/ui/card";
import { Textarea } from "./components/ui/textarea";
import { Heart } from "lucide-react";

type Message = {
  id: string;
  text: string;
  sender: 'user' | 'bot';
  timestamp: Date;
};

const BOT_PROFILE = {
  name: "Hope",
  responses: {
    greeting: "Hello friend. I'm here to listen without judgment. How are you feeling today?",
    happy: [
      "That's wonderful to hear! 😊 What's bringing you joy today?",
      "Your happiness makes me smile! Would you like to share more?"
    ],
    sad: [
      "I'm sorry you're feeling this way. You're not alone in this. 💙",
      "It's okay to feel sad sometimes. I'm here to listen if you want to talk more."
    ],
    stressed: [
      "Stress can feel overwhelming. Try taking a deep breath with me... 🌬️",
      "Let's take this one moment at a time. What's weighing on you most right now?"
    ],
    default: [
      "Thank you for sharing that with me.",
      "I'm listening carefully. Please continue when you're ready.",
      "Would you like to talk more about what's on your mind?"
    ]
  },
  helpResources: [
    "National Suicide Prevention Lifeline: 988",
    "Crisis Text Line: Text HOME to 741741",
    "For immediate help, please contact a professional"
  ]
};

export default function MentalSupportChat() {
  const [messages, setMessages] = useState<Message[]>([{
    id: crypto.randomUUID(),
    text: BOT_PROFILE.responses.greeting,
    sender: 'bot',
    timestamp: new Date()
  }]);
  const [input, setInput] = useState('');
  const [isTyping, setIsTyping] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const getRandomResponse = (category: keyof typeof BOT_PROFILE.responses) => {
    const options = BOT_PROFILE.responses[category];
    return options[Math.floor(Math.random() * options.length)];
  };

  const handleSend = () => {
    if (!input.trim() || isTyping) return;
    
    // Add user message
    const userMessage: Message = {
      id: crypto.randomUUID(),
      text: input,
      sender: 'user',
      timestamp: new Date()
    };
    setMessages(prev => [...prev, userMessage]);
    setInput('');
    setIsTyping(true);

    // Determine bot response
    setTimeout(() => {
      let responseCategory: keyof typeof BOT_PROFILE.responses = 'default';
      const lowerInput = input.toLowerCase();
      
      if (lowerInput.includes('happy') || lowerInput.includes('good') || lowerInput.includes('great')) {
        responseCategory = 'happy';
      } else if (lowerInput.includes('sad') || lowerInput.includes('bad') || lowerInput.includes('depressed')) {
        responseCategory = 'sad';
      } else if (lowerInput.includes('stress') || lowerInput.includes('overwhelm') || lowerInput.includes('anxious')) {
        responseCategory = 'stressed';
      }

      const botMessage: Message = {
        id: crypto.randomUUID(),
        text: getRandomResponse(responseCategory),
        sender: 'bot',
        timestamp: new Date()
      };
      
      setMessages(prev => [...prev, botMessage]);
      setIsTyping(false);
    }, 800 + Math.random() * 800); // Variable delay for natural feel
  };

  const showHelpResources = () => {
    if (isTyping) return;
    
    setIsTyping(true);
    setTimeout(() => {
      setMessages(prev => [
        ...prev,
        ...BOT_PROFILE.helpResources.map(text => ({
          id: crypto.randomUUID(),
          text,
          sender: 'bot' as const,
          timestamp: new Date()
        }))
      ]);
      setIsTyping(false);
    }, 500);
  };

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  return (
    <div className="min-h-screen bg-gradient-to-b from-blue-50 to-purple-50 flex items-center justify-center p-4">
      <Card className="w-full max-w-md h-[550px] flex flex-col shadow-lg">
        <CardHeader className="border-b bg-white/80 backdrop-blur-sm">
          <div className="flex items-center gap-3">
            <div className="bg-pink-100 p-2 rounded-full">
              <Heart className="text-pink-500" size={20} />
            </div>
            <div>
              <CardTitle className="text-lg">{BOT_PROFILE.name}</CardTitle>
              <p className="text-xs text-muted-foreground">
                {isTyping ? 'Typing...' : 'Online'}
              </p>
            </div>
          </div>
        </CardHeader>

        <CardContent className="flex-1 overflow-y-auto p-4 space-y-3">
          {messages.map((msg) => (
            <div 
              key={msg.id}
              className={`flex ${msg.sender === 'user' ? 'justify-end' : 'justify-start'}`}
            >
              <div 
                className={`max-w-[85%] rounded-2xl px-4 py-2 text-sm ${
                  msg.sender === 'user' 
                    ? 'bg-blue-500 text-white rounded-br-none'
                    : 'bg-white border rounded-bl-none'
                }`}
              >
                {msg.text}
                <div className="text-xs opacity-70 mt-1 text-right">
                  {msg.timestamp.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                </div>
              </div>
            </div>
          ))}
          {isTyping && (
            <div className="flex justify-start">
              <div className="bg-white border rounded-2xl px-4 py-2 text-sm">
                <div className="flex space-x-1">
                  <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce"></div>
                  <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0.2s' }}></div>
                  <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0.4s' }}></div>
                </div>
              </div>
            </div>
          )}
          <div ref={messagesEndRef} />
        </CardContent>

        <CardFooter className="border-t bg-white/80 backdrop-blur-sm p-3">
          <div className="flex flex-col w-full gap-2">
            <div className="flex w-full gap-2">
              <Textarea
                value={input}
                onChange={(e) => setInput(e.target.value)}
                placeholder="Share how you're feeling..."
                className="flex-1 min-h-[40px] resize-none"
                onKeyDown={(e) => e.key === 'Enter' && !e.shiftKey && handleSend()}
                rows={1}
              />
              <Button 
                onClick={handleSend}
                disabled={!input.trim() || isTyping}
                className="h-[40px]"
              >
                Send
              </Button>
            </div>
            <Button 
              variant="ghost" 
              size="sm" 
              onClick={showHelpResources}
              disabled={isTyping}
              className="text-xs text-blue-600 hover:text-blue-800 self-start h-8 px-2"
            >
              Need immediate help?
            </Button>
          </div>
        </CardFooter>
      </Card>
    </div>
  );
}
