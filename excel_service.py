import React, { useState, useEffect } from 'react';
import { Camera, MessageSquare, BarChart3, Mic, Upload, Users, TrendingUp, X, Menu, LogIn, UserPlus, Home, Send, Plus, Edit3, Save } from 'lucide-react';

const SahaYOGI = () => {
  const [currentPage, setCurrentPage] = useState('home');
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [user, setUser] = useState(null);
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);
  const [chatHistory, setChatHistory] = useState([]);
  const [transactions, setTransactions] = useState([]);

  // Vespa.ai inspired color scheme
  const colors = {
    primary: '#2D2D2D',
    secondary: '#FF6B35',
    accent: '#4ECDC4',
    bg: '#F7F7F7',
    text: '#2D2D2D',
    textLight: '#666666'
  };

  // Navigation component
  const Navigation = () => (
    <nav style={{
      background: colors.primary,
      padding: '1rem 2rem',
      position: 'sticky',
      top: 0,
      zIndex: 1000,
      boxShadow: '0 2px 10px rgba(0,0,0,0.1)'
    }}>
      <div style={{ 
        maxWidth: '1400px', 
        margin: '0 auto', 
        display: 'flex', 
        justifyContent: 'space-between', 
        alignItems: 'center' 
      }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '1rem' }}>
          <h1 style={{ 
            color: 'white', 
            fontSize: '1.5rem', 
            fontWeight: '700',
            margin: 0,
            display: 'flex',
            alignItems: 'center',
            gap: '0.5rem'
          }}>
            <span style={{ color: colors.secondary }}>SahaYOGI</span>
          </h1>
        </div>

        {/* Desktop Menu */}
        <div style={{ 
          display: 'none', 
          gap: '2rem', 
          alignItems: 'center',
          '@media (min-width: 768px)': { display: 'flex' }
        }} className="desktop-menu">
          <NavLink icon={Home} label="Home" active={currentPage === 'home'} onClick={() => setCurrentPage('home')} />
          {isLoggedIn && (
            <>
              <NavLink icon={Upload} label="Upload Bill" active={currentPage === 'upload'} onClick={() => setCurrentPage('upload')} />
              <NavLink icon={Mic} label="Commands" active={currentPage === 'commands'} onClick={() => setCurrentPage('commands')} />
              <NavLink icon={BarChart3} label="Dashboard" active={currentPage === 'dashboard'} onClick={() => setCurrentPage('dashboard')} />
              <NavLink icon={MessageSquare} label="Chatbot" active={currentPage === 'chatbot'} onClick={() => setCurrentPage('chatbot')} />
            </>
          )}
          {!isLoggedIn ? (
            <>
              <button onClick={() => setCurrentPage('login')} style={{
                background: 'transparent',
                border: `2px solid ${colors.secondary}`,
                color: colors.secondary,
                padding: '0.5rem 1.5rem',
                borderRadius: '8px',
                cursor: 'pointer',
                fontWeight: '600',
                transition: 'all 0.3s'
              }}>Login</button>
              <button onClick={() => setCurrentPage('register')} style={{
                background: colors.secondary,
                border: 'none',
                color: 'white',
                padding: '0.5rem 1.5rem',
                borderRadius: '8px',
                cursor: 'pointer',
                fontWeight: '600',
                transition: 'all 0.3s'
              }}>Register</button>
            </>
          ) : (
            <button onClick={() => {
              setIsLoggedIn(false);
              setUser(null);
              setCurrentPage('home');
            }} style={{
              background: colors.accent,
              border: 'none',
              color: 'white',
              padding: '0.5rem 1.5rem',
              borderRadius: '8px',
              cursor: 'pointer',
              fontWeight: '600'
            }}>Logout</button>
          )}
        </div>

        {/* Mobile Menu Button */}
        <button 
          onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
          style={{
            background: 'transparent',
            border: 'none',
            color: 'white',
            cursor: 'pointer',
            display: 'block'
          }}
          className="mobile-menu-btn"
        >
          {mobileMenuOpen ? <X size={24} /> : <Menu size={24} />}
        </button>
      </div>

      {/* Mobile Menu */}
      {mobileMenuOpen && (
        <div style={{
          position: 'absolute',
          top: '100%',
          left: 0,
          right: 0,
          background: colors.primary,
          padding: '1rem',
          display: 'flex',
          flexDirection: 'column',
          gap: '0.5rem'
        }}>
          <MobileNavLink icon={Home} label="Home" onClick={() => { setCurrentPage('home'); setMobileMenuOpen(false); }} />
          {isLoggedIn && (
            <>
              <MobileNavLink icon={Upload} label="Upload Bill" onClick={() => { setCurrentPage('upload'); setMobileMenuOpen(false); }} />
              <MobileNavLink icon={Mic} label="Commands" onClick={() => { setCurrentPage('commands'); setMobileMenuOpen(false); }} />
              <MobileNavLink icon={BarChart3} label="Dashboard" onClick={() => { setCurrentPage('dashboard'); setMobileMenuOpen(false); }} />
              <MobileNavLink icon={MessageSquare} label="Chatbot" onClick={() => { setCurrentPage('chatbot'); setMobileMenuOpen(false); }} />
            </>
          )}
        </div>
      )}
    </nav>
  );

  const NavLink = ({ icon: Icon, label, active, onClick }) => (
    <button onClick={onClick} style={{
      background: 'transparent',
      border: 'none',
      color: active ? colors.secondary : 'white',
      cursor: 'pointer',
      display: 'flex',
      alignItems: 'center',
      gap: '0.5rem',
      fontWeight: active ? '600' : '400',
      fontSize: '0.95rem',
      padding: '0.5rem',
      transition: 'all 0.3s',
      borderBottom: active ? `2px solid ${colors.secondary}` : '2px solid transparent'
    }}>
      <Icon size={18} />
      {label}
    </button>
  );

  const MobileNavLink = ({ icon: Icon, label, onClick }) => (
    <button onClick={onClick} style={{
      background: 'rgba(255,255,255,0.1)',
      border: 'none',
      color: 'white',
      padding: '1rem',
      borderRadius: '8px',
      cursor: 'pointer',
      display: 'flex',
      alignItems: 'center',
      gap: '1rem',
      fontSize: '1rem',
      transition: 'all 0.3s'
    }}>
      <Icon size={20} />
      {label}
    </button>
  );

  // Home Page
  const HomePage = () => (
    <div>
      {/* Hero Section */}
      <section style={{
        background: `linear-gradient(135deg, ${colors.primary} 0%, #1a1a1a 100%)`,
        padding: '6rem 2rem',
        textAlign: 'center',
        color: 'white'
      }}>
        <h1 style={{ 
          fontSize: '3.5rem', 
          fontWeight: '800', 
          marginBottom: '1.5rem',
          lineHeight: '1.2'
        }}>
          Welcome to <span style={{ color: colors.secondary }}>SahaYOGI</span>
        </h1>
        <p style={{ 
          fontSize: '1.3rem', 
          color: '#cccccc', 
          maxWidth: '700px', 
          margin: '0 auto 3rem',
          lineHeight: '1.6'
        }}>
          Your Intelligent Shop Assistant - Making shop management easy, smart, and efficient for every shopkeeper
        </p>
        <div style={{ display: 'flex', gap: '1rem', justifyContent: 'center', flexWrap: 'wrap' }}>
          <button onClick={() => setCurrentPage('register')} style={{
            background: colors.secondary,
            border: 'none',
            color: 'white',
            padding: '1rem 2.5rem',
            borderRadius: '12px',
            fontSize: '1.1rem',
            fontWeight: '600',
            cursor: 'pointer',
            transition: 'all 0.3s',
            boxShadow: '0 4px 20px rgba(255,107,53,0.3)'
          }}>Get Started</button>
          <button onClick={() => setCurrentPage('login')} style={{
            background: 'transparent',
            border: '2px solid white',
            color: 'white',
            padding: '1rem 2.5rem',
            borderRadius: '12px',
            fontSize: '1.1rem',
            fontWeight: '600',
            cursor: 'pointer',
            transition: 'all 0.3s'
          }}>Login</button>
        </div>
      </section>

      {/* Features Section */}
      <section style={{ padding: '5rem 2rem', maxWidth: '1400px', margin: '0 auto' }}>
        <h2 style={{ 
          textAlign: 'center', 
          fontSize: '2.5rem', 
          fontWeight: '700', 
          marginBottom: '3rem',
          color: colors.text
        }}>
          Powerful Features
        </h2>
        <div style={{ 
          display: 'grid', 
          gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))', 
          gap: '2rem' 
        }}>
          <FeatureCard 
            icon={Camera}
            title="Smart OCR Scanning"
            description="Upload bills and let AI extract items automatically with high accuracy"
            color={colors.secondary}
          />
          <FeatureCard 
            icon={Mic}
            title="Voice Commands"
            description="Manage udhaar and transactions with simple voice or text commands"
            color={colors.accent}
          />
          <FeatureCard 
            icon={BarChart3}
            title="Live Dashboard"
            description="Real-time insights and analytics to track your business performance"
            color="#9B59B6"
          />
          <FeatureCard 
            icon={MessageSquare}
            title="AI Chatbot"
            description="Get instant answers about your shop, inventory, and finances"
            color="#3498DB"
          />
          <FeatureCard 
            icon={Users}
            title="Customer Management"
            description="Track customer udhaars and repayments effortlessly"
            color="#E74C3C"
          />
          <FeatureCard 
            icon={TrendingUp}
            title="Profit Analytics"
            description="Monitor daily, weekly, and monthly profit/loss reports"
            color="#27AE60"
          />
        </div>
      </section>
    </div>
  );

  const FeatureCard = ({ icon: Icon, title, description, color }) => (
    <div style={{
      background: 'white',
      padding: '2.5rem',
      borderRadius: '16px',
      boxShadow: '0 4px 20px rgba(0,0,0,0.08)',
      transition: 'all 0.3s',
      cursor: 'pointer',
      border: '1px solid #f0f0f0'
    }}
    onMouseEnter={(e) => {
      e.currentTarget.style.transform = 'translateY(-8px)';
      e.currentTarget.style.boxShadow = '0 12px 40px rgba(0,0,0,0.12)';
    }}
    onMouseLeave={(e) => {
      e.currentTarget.style.transform = 'translateY(0)';
      e.currentTarget.style.boxShadow = '0 4px 20px rgba(0,0,0,0.08)';
    }}>
      <div style={{
        width: '60px',
        height: '60px',
        background: `${color}15`,
        borderRadius: '12px',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        marginBottom: '1.5rem'
      }}>
        <Icon size={30} color={color} />
      </div>
      <h3 style={{ 
        fontSize: '1.4rem', 
        fontWeight: '700', 
        marginBottom: '1rem',
        color: colors.text
      }}>{title}</h3>
      <p style={{ 
        color: colors.textLight, 
        lineHeight: '1.6',
        fontSize: '1rem'
      }}>{description}</p>
    </div>
  );

  // Login Page
  const LoginPage = () => {
    const [email, setEmail] = useState('');
    const [otp, setOtp] = useState('');
    const [otpSent, setOtpSent] = useState(false);

    return (
      <div style={{ 
        minHeight: 'calc(100vh - 80px)', 
        display: 'flex', 
        alignItems: 'center', 
        justifyContent: 'center',
        padding: '2rem',
        background: colors.bg
      }}>
        <div style={{
          background: 'white',
          padding: '3rem',
          borderRadius: '20px',
          boxShadow: '0 8px 40px rgba(0,0,0,0.1)',
          maxWidth: '500px',
          width: '100%'
        }}>
          <h2 style={{ 
            fontSize: '2rem', 
            fontWeight: '700', 
            marginBottom: '0.5rem',
            color: colors.text
          }}>Login to SahaYOGI</h2>
          <p style={{ color: colors.textLight, marginBottom: '2rem' }}>
            Enter your email to receive an OTP
          </p>

          <input
            type="email"
            placeholder="your.email@example.com"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            style={{
              width: '100%',
              padding: '1rem',
              borderRadius: '10px',
              border: '2px solid #e0e0e0',
              fontSize: '1rem',
              marginBottom: '1rem',
              boxSizing: 'border-box'
            }}
          />

          {!otpSent ? (
            <button onClick={() => {
              if (email) {
                setOtpSent(true);
                alert('OTP sent to ' + email);
              }
            }} style={{
              width: '100%',
              background: colors.secondary,
              border: 'none',
              color: 'white',
              padding: '1rem',
              borderRadius: '10px',
              fontSize: '1rem',
              fontWeight: '600',
              cursor: 'pointer',
              transition: 'all 0.3s'
            }}>Send OTP</button>
          ) : (
            <>
              <input
                type="text"
                placeholder="Enter 6-digit OTP"
                value={otp}
                onChange={(e) => setOtp(e.target.value)}
                maxLength={6}
                style={{
                  width: '100%',
                  padding: '1rem',
                  borderRadius: '10px',
                  border: '2px solid #e0e0e0',
                  fontSize: '1rem',
                  marginBottom: '1rem',
                  boxSizing: 'border-box',
                  textAlign: 'center',
                  letterSpacing: '0.5rem'
                }}
              />
              <button onClick={() => {
                if (otp.length === 6) {
                  setIsLoggedIn(true);
                  setUser({ email });
                  setCurrentPage('dashboard');
                }
              }} style={{
                width: '100%',
                background: colors.accent,
                border: 'none',
                color: 'white',
                padding: '1rem',
                borderRadius: '10px',
                fontSize: '1rem',
                fontWeight: '600',
                cursor: 'pointer',
                transition: 'all 0.3s'
              }}>Verify & Login</button>
            </>
          )}

          <p style={{ 
            textAlign: 'center', 
            marginTop: '2rem',
            color: colors.textLight
          }}>
            Don't have an account? {' '}
            <span onClick={() => setCurrentPage('register')} style={{
              color: colors.secondary,
              cursor: 'pointer',
              fontWeight: '600'
            }}>Register here</span>
          </p>
        </div>
      </div>
    );
  };

  // Register Page
  const RegisterPage = () => {
    const [name, setName] = useState('');
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');

    return (
      <div style={{ 
        minHeight: 'calc(100vh - 80px)', 
        display: 'flex', 
        alignItems: 'center', 
        justifyContent: 'center',
        padding: '2rem',
        background: colors.bg
      }}>
        <div style={{
          background: 'white',
          padding: '3rem',
          borderRadius: '20px',
          boxShadow: '0 8px 40px rgba(0,0,0,0.1)',
          maxWidth: '500px',
          width: '100%'
        }}>
          <h2 style={{ 
            fontSize: '2rem', 
            fontWeight: '700', 
            marginBottom: '0.5rem',
            color: colors.text
          }}>Create Account</h2>
          <p style={{ color: colors.textLight, marginBottom: '2rem' }}>
            Join SahaYOGI and start managing your shop smartly
          </p>

          <input
            type="text"
            placeholder="Full Name"
            value={name}
            onChange={(e) => setName(e.target.value)}
            style={{
              width: '100%',
              padding: '1rem',
              borderRadius: '10px',
              border: '2px solid #e0e0e0',
              fontSize: '1rem',
              marginBottom: '1rem',
              boxSizing: 'border-box'
            }}
          />

          <input
            type="email"
            placeholder="Email Address"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            style={{
              width: '100%',
              padding: '1rem',
              borderRadius: '10px',
              border: '2px solid #e0e0e0',
              fontSize: '1rem',
              marginBottom: '1rem',
              boxSizing: 'border-box'
            }}
          />

          <input
            type="password"
            placeholder="Password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            style={{
              width: '100%',
              padding: '1rem',
              borderRadius: '10px',
              border: '2px solid #e0e0e0',
              fontSize: '1rem',
              marginBottom: '1.5rem',
              boxSizing: 'border-box'
            }}
          />

          <button onClick={() => {
            if (name && email && password) {
              alert('Account created successfully!');
              setCurrentPage('login');
            }
          }} style={{
            width: '100%',
            background: colors.secondary,
            border: 'none',
            color: 'white',
            padding: '1rem',
            borderRadius: '10px',
            fontSize: '1rem',
            fontWeight: '600',
            cursor: 'pointer',
            transition: 'all 0.3s'
          }}>Create Account</button>

          <p style={{ 
            textAlign: 'center', 
            marginTop: '2rem',
            color: colors.textLight
          }}>
            Already have an account? {' '}
            <span onClick={() => setCurrentPage('login')} style={{
              color: colors.secondary,
              cursor: 'pointer',
              fontWeight: '600'
            }}>Login here</span>
          </p>
        </div>
      </div>
    );
  };

  // Dashboard Page
  const DashboardPage = () => {
    const stats = [
      { label: 'Total Sales', value: '₹45,230', icon: TrendingUp, color: colors.secondary },
      { label: 'Total Udhaars', value: '₹8,450', icon: Users, color: colors.accent },
      { label: 'Customers', value: '156', icon: Users, color: '#9B59B6' },
      { label: 'Today\'s Revenue', value: '₹2,340', icon: BarChart3, color: '#27AE60' }
    ];

    return (
      <div style={{ padding: '2rem', maxWidth: '1400px', margin: '0 auto' }}>
        <h1 style={{ 
          fontSize: '2.5rem', 
          fontWeight: '700', 
          marginBottom: '2rem',
          color: colors.text
        }}>Dashboard</h1>

        <div style={{ 
          display: 'grid', 
          gridTemplateColumns: 'repeat(auto-fit, minmax(250px, 1fr))', 
          gap: '1.5rem',
          marginBottom: '3rem'
        }}>
          {stats.map((stat, idx) => (
            <div key={idx} style={{
              background: 'white',
              padding: '2rem',
              borderRadius: '16px',
              boxShadow: '0 4px 20px rgba(0,0,0,0.08)',
              display: 'flex',
              alignItems: 'center',
              gap: '1.5rem'
            }}>
              <div style={{
                width: '60px',
                height: '60px',
                background: `${stat.color}15`,
                borderRadius: '12px',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center'
              }}>
                <stat.icon size={28} color={stat.color} />
              </div>
              <div>
                <p style={{ color: colors.textLight, fontSize: '0.9rem', marginBottom: '0.25rem' }}>
                  {stat.label}
                </p>
                <h3 style={{ fontSize: '1.8rem', fontWeight: '700', color: colors.text }}>
                  {stat.value}
                </h3>
              </div>
            </div>
          ))}
        </div>

        <div style={{
          background: 'white',
          padding: '2rem',
          borderRadius: '16px',
          boxShadow: '0 4px 20px rgba(0,0,0,0.08)'
        }}>
          <h2 style={{ fontSize: '1.5rem', fontWeight: '700', marginBottom: '1.5rem', color: colors.text }}>
            Recent Transactions
          </h2>
          <p style={{ color: colors.textLight }}>No transactions yet. Start by uploading a bill!</p>
        </div>
      </div>
    );
  };

  // Chatbot Page
  const ChatbotPage = () => {
    const [message, setMessage] = useState('');

    const sendMessage = () => {
      if (message.trim()) {
        setChatHistory([...chatHistory, 
          { sender: 'user', text: message },
          { sender: 'bot', text: 'Thanks for your message! This is a demo response.' }
        ]);
        setMessage('');
      }
    };

    return (
      <div style={{ padding: '2rem', maxWidth: '1000px', margin: '0 auto' }}>
        <h1 style={{ 
          fontSize: '2.5rem', 
          fontWeight: '700', 
          marginBottom: '2rem',
          color: colors.text
        }}>AI Chatbot</h1>

        <div style={{
          background: 'white',
          borderRadius: '16px',
          boxShadow: '0 4px 20px rgba(0,0,0,0.08)',
          height: '600px',
          display: 'flex',
          flexDirection: 'column'
        }}>
          <div style={{
            flex: 1,
            padding: '2rem',
            overflowY: 'auto'
          }}>
            {chatHistory.length === 0 ? (
              <div style={{ 
                textAlign: 'center', 
                padding: '4rem 2rem',
                color: colors.textLight
              }}>
                <MessageSquare size={64} color={colors.accent} style={{ marginBottom: '1rem' }} />
                <h3 style={{ fontSize: '1.5rem', marginBottom: '0.5rem', color: colors.text }}>
                  Start a Conversation
                </h3>
                <p>Ask me anything about your shop, inventory, or finances!</p>
              </div>
            ) : (
              chatHistory.map((msg, idx) => (
                <div key={idx} style={{
                  display: 'flex',
                  justifyContent: msg.sender === 'user' ? 'flex-end' : 'flex-start',
                  marginBottom: '1rem'
                }}>
                  <div style={{
                    background: msg.sender === 'user' ? colors.secondary : colors.bg,
                    color: msg.sender === 'user' ? 'white' : colors.text,
                    padding: '1rem 1.5rem',
                    borderRadius: '16px',
                    maxWidth: '70%'
                  }}>
                    {msg.text}
                  </div>
                </div>
              ))
            )}
          </div>

          <div style={{
            padding: '1.5rem',
            borderTop: '1px solid #e0e0e0',
            display: 'flex',
            gap: '1rem'
          }}>
            <input
              type="text"
              placeholder="Type your message..."
              value={message}
              onChange={(e) => setMessage(e.target.value)}
              onKeyPress={(e) => e.key === 'Enter' && sendMessage()}
              style={{
                flex: 1,
                padding: '1rem',
                borderRadius: '10px',
                border: '2px solid #e0e0e0',
                fontSize: '1rem'
              }}
            />
            <button onClick={sendMessage} style={{
              background: colors.secondary,
              border: 'none',
              color: 'white',
              padding: '1rem 2rem',
              borderRadius: '10px',
              cursor: 'pointer',
              display: 'flex',
              alignItems: 'center',
              gap: '0.5rem',
              fontWeight: '600'
            }}>
              <Send size={20} />
              Send
            </button>
          </div>
        </div>
      </div>
    );
  };

  // Upload Bill Page
  const UploadBillPage = () => {
    const [file, setFile] = useState(null);

    return (
      <div style={{ padding: '2rem', maxWidth: '800px', margin: '0 auto' }}>
        <h1 style={{ 
          fontSize: '2.5rem', 
          fontWeight: '700', 
          marginBottom: '2rem',
          color: colors.text
        }}>Smart Bill Scanner</h1>

        <div style={{
          background: 'white',
          padding: '3rem',
          borderRadius: '16px',
          boxShadow: '0 4px 20px rgba(0,0,0,0.08)',
          textAlign: 'center'
        }}>
          <div style={{
            border: `3px dashed ${colors.secondary}`,
            borderRadius: '16px',
            padding: '4rem 2rem',
            marginBottom: '2rem',
            background: `${colors.secondary}05`
          }}>
            <Camera size={64} color={colors.secondary} style={{ marginBottom: '1rem' }} />
            <h3 style={{ fontSize: '1.5rem', marginBottom: '0.5rem', color: colors.text }}>
              Upload Bill Image
            </h3>
            <p style={{ color: colors.textLight, marginBottom: '2rem' }}>
              Drag and drop or click to select
            </p>
            <input
              type="file"
              accept="image/*"
              onChange={(e) => setFile(e.target.files[0])}
              style={{ display: 'none' }}
              id="file-upload"
            />
            <label htmlFor="file-upload" style={{
              background: colors.secondary,
              color: 'white',
              padding: '1rem 2rem',
              borderRadius: '10px',
              cursor: 'pointer',
              display: 'inline-block',
              fontWeight: '600'
            }}>
              Choose File
            </label>
          </div>

          {file && (
            <button style={{
              background: colors.accent,
              border: 'none',
              color: 'white',
              padding: '1rem 2rem',
              borderRadius: '10px',
              fontSize: '1rem',
              fontWeight: '600',
              cursor: 'pointer'
            }}>
              Extract Items
            </button>
          )}
        </div>
      </div>
    );
  };

  // Commands Page
  const CommandsPage = () => {
    const [command, setCommand] = useState('');

    return (
      <div style={{ padding: '2rem', maxWidth: '800px', margin: '0 auto' }}>
        <h1 style={{ 
          fontSize: '2.5rem', 
          fontWeight: '700', 
          marginBottom: '2rem',
          color: colors.text
        }}>Voice & Text Commands</h1>

        <div style={{
          background: 'white',
          padding: '2rem',
          borderRadius: '16px',
          boxShadow: '0 4px 20px rgba(0,0,0,0.08)',
          marginBottom: '2rem'
        }}>
          <h3 style={{ fontSize: '1.3rem', fontWeight: '700', marginBottom: '1rem', color: colors.text }}>
            Try these commands:
          </h3>
          <ul style={{ textAlign: 'left', color: colors.textLight, lineHeight: '2' }}>
            <li><code>add udhaar Ramesh sugar 50</code></li>
            <li><code>repayment Ramesh 100</code></li>
            <li><code>add sale CustomerName item price</code></li>
          </ul>
        </div>

        <div style={{
          background: 'white',
          padding: '2rem',
          borderRadius: '16px',
          boxShadow: '0 4px 20px rgba(0,0,0,0.08)'
        }}>
          <textarea
            placeholder="Type your command here..."
            value={command}
            onChange={(e) => setCommand(e.target.value)}
            style={{
              width: '100%',
              padding: '1rem',
              borderRadius: '10px',
              border: '2px solid #e0e0e0',
              fontSize: '1rem',
              minHeight: '150px',
              resize: 'vertical',
              boxSizing: 'border-box',
              marginBottom: '1rem'
            }}
          />
          <button onClick={() => {
            if (command.trim()) {
              alert('Command executed: ' + command);
              setCommand('');
            }
          }} style={{
            background: colors.secondary,
            border: 'none',
            color: 'white',
            padding: '1rem 2rem',
            borderRadius: '10px',
            fontSize: '1rem',
            fontWeight: '600',
            cursor: 'pointer',
            width: '100%'
          }}>
            Execute Command
          </button>
        </div>
      </div>
    );
  };

  return (
    <div style={{ 
      minHeight: '100vh', 
      background: colors.bg,
      fontFamily: '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif'
    }}>
      <style>{`
        .desktop-menu { display: none; }
        @media (min-width: 768px) {
          .desktop-menu { display: flex !important; }
          .mobile-menu-btn { display: none !important; }
        }
        * { margin: 0; padding: 0; box-sizing: border-box; }
      `}</style>
      
      <Navigation />
      
      {currentPage === 'home' && <HomePage />}
      {currentPage === 'login' && <LoginPage />}
      {currentPage === 'register' && <RegisterPage />}
      {currentPage === 'dashboard' && <DashboardPage />}
      {currentPage === 'chatbot' && <ChatbotPage />}
      {currentPage === 'upload' && <UploadBillPage />}
      {currentPage === 'commands' && <CommandsPage />}

      {/* Footer */}
      <footer style={{
        background: colors.primary,
        color: 'white',
        padding: '3rem 2rem',
        marginTop: '5rem',
        textAlign: 'center'
      }}>
        <h3 style={{ fontSize: '1.5rem', marginBottom: '1rem' }}>SahaYOGI</h3>
        <p style={{ color: '#cccccc', marginBottom: '1rem' }}>
          Your Intelligent Shop Assistant
        </p>
        <p style={{ color: '#999999', fontSize: '0.9rem' }}>
          © 2024 SahaYOGI. All rights reserved.
        </p>
      </footer>
    </div>
  );
};

export default SahaYOGI;