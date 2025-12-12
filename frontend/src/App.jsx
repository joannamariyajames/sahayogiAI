import VoiceRecorder from "./components/VoiceRecorder";
// import React, { useState } from 'react'
// import './App.css'

// function Sidebar({ currentPage, setCurrentPage, userId, logout }) {
//   const menuOptions = [
//     { label: '🏠 Home', value: 'Home' },
//     { label: '🔐 Login', value: 'Login' },
//     { label: '📝 Register', value: 'Register' },
//     { label: '🧾 Upload Bill', value: 'Upload Bill' },
//     { label: '🎤 Command', value: 'Command' },
//     { label: '📊 Dashboard', value: 'Dashboard' }
//   ]

//   return (
//     <aside className="sidebar">
//       <div className="sidebar-header">
//         <h1>🏪 SahaYOGI</h1>
//         <p>Intelligent Shop Assistant</p>
//       </div>

//       <nav>
//         {menuOptions.map((opt) => (
//           <button
//             key={opt.value}
//             className={`nav-btn ${currentPage === opt.value ? 'active' : ''}`}
//             onClick={() => setCurrentPage(opt.value)}
//           >
//             {opt.label}
//           </button>
//         ))}
//       </nav>

//       <div className="sidebar-bottom">
//         {userId ? (
//           <>
//             <div className="quick-stats">
//               <h3>📈 Your Stats</h3>
//               <div className="stats-row">
//                 <div>
//                   <div className="stat-number">₹12,450</div>
//                   <div className="stat-label">Sales</div>
//                 </div>
//                 <div>
//                   <div className="stat-number">24</div>
//                   <div className="stat-label">Customers</div>
//                 </div>
//               </div>
//             </div>
//             <button className="logout-btn" onClick={logout}>🚪 Logout</button>
//           </>
//         ) : (
//           <p className="not-logged">Not logged in</p>
//         )}
//       </div>
//     </aside>
//   )
// }

// function Home({ goTo }) {
//   return (
//     <div className="main-container">
//       <h1 className="page-title">SahaYOGI</h1>
//       <p className="page-subtitle">
//         An intelligent assistant designed to modernize shop management with AI-powered tools,
//         helping small businesses thrive in the digital age.
//       </p>

//       <div className="stats-container">
//         <div className="stat-item">
//           <span className="stat-number">99%</span>
//           <span className="stat-label">Accuracy</span>
//         </div>
//         <div className="stat-item">
//           <span className="stat-number">24/7</span>
//           <span className="stat-label">Availability</span>
//         </div>
//         <div className="stat-item">
//           <span className="stat-number">1000+</span>
//           <span className="stat-label">Shops Empowered</span>
//         </div>
//       </div>

//       <div className="features-grid">
//         <div className="feature-card">
//           <span className="feature-icon">🧾</span>
//           <h3 className="feature-title">Intelligent Bill Scanning</h3>
//           <p className="feature-desc">Automatically extract item details from any bill or receipt with our advanced OCR technology. Save hours of manual data entry.</p>
//         </div>

//         <div className="feature-card">
//           <span className="feature-icon">📊</span>
//           <h3 className="feature-title">Smart Analytics Dashboard</h3>
//           <p className="feature-desc">Gain real-time insights into your sales, inventory, and customer trends with beautifully visualized data and reports.</p>
//         </div>

//         <div className="feature-card">
//           <span className="feature-icon">🎙️</span>
//           <h3 className="feature-title">Voice-Activated Commands</h3>
//           <p className="feature-desc">Manage transactions, check stock, or update records using simple voice commands. Hands-free operation for busy shopkeepers.</p>
//         </div>

//         <div className="feature-card">
//           <span className="feature-icon">🤝</span>
//           <h3 className="feature-title">Customer Credit Management</h3>
//           <p className="feature-desc">Effortlessly track udhaar, send payment reminders, and maintain customer relationships with our integrated credit system.</p>
//         </div>
//       </div>

//       <div className="cta-section">
//         <h2 className="cta-title">Ready to Transform Your Shop?</h2>
//         <p className="cta-subtitle">Join thousands of shopkeepers who have modernized their businesses with SahaYOGI. Start your 14-day free trial with no credit card required.</p>

//         <div className="action-buttons">
//           <button className="action-btn btn-primary" onClick={() => goTo('Register')}>🚀 Get Started Free</button>
//           <button className="action-btn btn-secondary" onClick={() => goTo('Login')}>📞 Schedule Demo</button>
//         </div>
//         <p className="mini">No installation required • Works on any device • 24/7 support</p>
//       </div>
//     </div>
//   )
// }

// function Login({ onLogin, goHome }) {
//   const [email, setEmail] = useState('')
//   const [password, setPassword] = useState('')

//   const submit = (e) => {
//     e.preventDefault()
//     if (email && password) {
//       onLogin({ id: 'demo_user_123', email })
//       alert('✅ Login successful!')
//     } else {
//       alert('❌ Please fill all fields')
//     }
//   }

//   return (
//     <div className="auth-container">
//       <h1 className="auth-title">🔐 Login to SahaYOGI</h1>
//       <form className="auth-form" onSubmit={submit}>
//         <input value={email} onChange={(e)=>setEmail(e.target.value)} placeholder="shopkeeper@example.com" />
//         <input value={password} onChange={(e)=>setPassword(e.target.value)} type="password" placeholder="Enter your password" />
//         <div className="auth-actions">
//           <button type="submit" className="action-btn btn-primary">🚀 Login</button>
//           <button type="button" className="action-btn btn-secondary" onClick={goHome}>⬅️ Back to Home</button>
//         </div>
//       </form>
//     </div>
//   )
// }

// function Register({ onRegister, goHome }) {
//   const [name, setName] = useState('')
//   const [email, setEmail] = useState('')
//   const [password, setPassword] = useState('')
//   const [confirmPassword, setConfirmPassword] = useState('')

//   const submit = (e) => {
//     e.preventDefault()
//     if (!name || !email || !password || !confirmPassword) {
//       alert('❌ Please fill all fields')
//       return
//     }
//     if (password !== confirmPassword) {
//       alert("❌ Passwords don't match!")
//       return
//     }
//     onRegister({ id: 'new_user_' + email.split('@')[0], email })
//     alert(`✅ Account created for ${name}!`)
//   }

//   return (
//     <div className="auth-container">
//       <h1 className="auth-title">📝 Create Your Account</h1>
//       <form className="auth-form" onSubmit={submit}>
//         <input value={name} onChange={(e)=>setName(e.target.value)} placeholder="Enter your full name" />
//         <input value={email} onChange={(e)=>setEmail(e.target.value)} placeholder="shopkeeper@example.com" />
//         <input value={password} onChange={(e)=>setPassword(e.target.value)} type="password" placeholder="Create a strong password" />
//         <input value={confirmPassword} onChange={(e)=>setConfirmPassword(e.target.value)} type="password" placeholder="Re-enter your password" />

//         <div className="auth-actions">
//           <button type="submit" className="action-btn btn-primary">✨ Create Account</button>
//           <button type="button" className="action-btn btn-secondary" onClick={goHome}>⬅️ Back to Home</button>
//         </div>
//       </form>
//     </div>
//   )
// }

// function UploadBill({ userId, goDashboard }) {
//   const [file, setFile] = useState(null)
//   const [customerName, setCustomerName] = useState('Walk-in Customer')

//   const upload = () => {
//     if (!userId) {
//       alert('⚠️ Please login first!')
//       return
//     }
//     if (!file) {
//       alert('❌ Please select a file')
//       return
//     }
//     alert(`✅ Bill uploaded for ${customerName}! (demo)`) 
//   }

//   return (
//     <div className="upload-container">
//       <h1>🧾 Upload Bill</h1>
//       {!userId ? (
//         <div className="login-warning">
//           <p>⚠️ Please login first!</p>
//         </div>
//       ) : (
//         <>
//           <p className="info">Upload a bill image and our AI will extract items automatically</p>
//           <input type="file" accept="image/*" onChange={(e)=>setFile(e.target.files[0])} />
//           <input value={customerName} onChange={(e)=>setCustomerName(e.target.value)} />
//           <div className="auth-actions">
//             <button className="action-btn btn-primary" onClick={upload}>📤 Upload & Process</button>
//             <button className="action-btn btn-secondary" onClick={goDashboard}>⬅️ Back to Dashboard</button>
//           </div>
//         </>
//       )}
//     </div>
//   )
// }

// function Command({ userId, goDashboard }) {
//   const [command, setCommand] = useState('')

//   const execute = () => {
//     if (!userId) {
//       alert('⚠️ Please login first!')
//       return
//     }
//     if (!command) {
//       alert('❌ Please enter a command')
//       return
//     }
//     alert(`✅ Command executed: ${command}`)
//   }

//   return (
//     <div className="command-container">
//       <h1>🎤 Voice Commands</h1>
//       {!userId ? (
//         <div className="login-warning">
//           <p>⚠️ Please login first!</p>
//         </div>
//       ) : (
//         <>
//           <p className="info">Type or speak commands to manage your shop</p>
//           <textarea value={command} onChange={(e)=>setCommand(e.target.value)} placeholder="Example: 'add udhaar Ramesh sugar 50' or 'show today sales'" rows={6} />
//           <div className="auth-actions">
//             <button className="action-btn btn-secondary" onClick={()=>alert('🎤 Listening... (Demo mode)')}>🎙️ Start Listening</button>
//             <button className="action-btn btn-primary" onClick={execute}>🚀 Execute</button>
//             <button className="action-btn" onClick={goDashboard}>⬅️ Back</button>
//           </div>
//         </>
//       )}
//     </div>
//   )
// }

// function Dashboard({ userEmail, goHome, goUpload, goCommand }) {
//   const sampleData = [
//     { Customer: 'Ramesh', Item: 'Sugar 5kg', Amount: 250, Type: 'Sale', Time: '10:30 AM' },
//     { Customer: 'Suresh', Item: 'Rice 10kg', Amount: 450, Type: 'Udhaar', Time: '11:15 AM' },
//     { Customer: 'Priya', Item: 'Oil 1L', Amount: 180, Type: 'Sale', Time: '12:45 PM' },
//     { Customer: 'Mohan', Item: 'Flour 5kg', Amount: 120, Type: 'Udhaar', Time: '2:20 PM' },
//     { Customer: 'Ankit', Item: 'Tea 500g', Amount: 150, Type: 'Sale', Time: '4:10 PM' }
//   ]

//   return (
//     <div className="dashboard-container">
//       <h1>📊 Dashboard</h1>
//       {!userEmail ? (
//         <div className="login-warning"><p>⚠️ Please login first!</p></div>
//       ) : (
//         <>
//           <p className="welcome">Welcome, {userEmail}</p>

//           <div className="metrics-row">
//             <div className="metric">
//               <div className="metric-title">Today's Sales</div>
//               <div className="metric-value">₹12,450</div>
//               <div className="metric-diff">+8.5%</div>
//             </div>
//             <div className="metric">
//               <div className="metric-title">Total Udhaar</div>
//               <div className="metric-value">₹8,920</div>
//               <div className="metric-diff">3 customers</div>
//             </div>
//             <div className="metric">
//               <div className="metric-title">Bills Today</div>
//               <div className="metric-value">12</div>
//               <div className="metric-diff">+2</div>
//             </div>
//             <div className="metric">
//               <div className="metric-title">Customers</div>
//               <div className="metric-value">24</div>
//               <div className="metric-diff">+3</div>
//             </div>
//           </div>

//           <h3>🚀 Quick Actions</h3>
//           <div className="quick-actions">
//             <button className="action-btn" onClick={goUpload}>🧾 Upload Bill</button>
//             <button className="action-btn" onClick={goCommand}>🎤 Voice Command</button>
//             <button className="action-btn" onClick={()=>alert('Feature coming soon!')}>👥 Add Customer</button>
//             <button className="action-btn" onClick={()=>alert('Feature coming soon!')}>📈 View Reports</button>
//           </div>

//           <h3>📋 Recent Transactions</h3>
//           <table className="transactions">
//             <thead>
//               <tr><th>Customer</th><th>Item</th><th>Amount</th><th>Type</th><th>Time</th></tr>
//             </thead>
//             <tbody>
//               {sampleData.map((row, i) => (
//                 <tr key={i}>
//                   <td>{row.Customer}</td>
//                   <td>{row.Item}</td>
//                   <td>₹{row.Amount}</td>
//                   <td>{row.Type}</td>
//                   <td>{row.Time}</td>
//                 </tr>
//               ))}
//             </tbody>
//           </table>

//           <div style={{marginTop:20}}>
//             <button className="action-btn btn-secondary" onClick={goHome}>🏠 Back to Home</button>
//           </div>
//         </>
//       )}
//     </div>
//   )
// }

// function App() {
//   const [currentPage, setCurrentPage] = useState('Home')
//   const [userId, setUserId] = useState(null)
//   const [userEmail, setUserEmail] = useState(null)

//   const handleLogin = ({ id, email }) => {
//     setUserId(id)
//     setUserEmail(email)
//     setCurrentPage('Dashboard')
//   }

//   const handleRegister = ({ id, email }) => {
//     setUserId(id)
//     setUserEmail(email)
//     setCurrentPage('Dashboard')
//   }

//   const logout = () => {
//     setUserId(null)
//     setUserEmail(null)
//     setCurrentPage('Home')
//     alert('Logged out successfully!')
//   }

//   const go = (page) => setCurrentPage(page)

//   return (
//     <div className="app-root">
//       <Sidebar currentPage={currentPage} setCurrentPage={setCurrentPage} userId={userId} logout={logout} />
//       <main className="main-content">
//         {currentPage === 'Home' && <Home goTo={go} />}
//         {currentPage === 'Login' && <Login onLogin={handleLogin} goHome={()=>go('Home')} />}
//         {currentPage === 'Register' && <Register onRegister={handleRegister} goHome={()=>go('Home')} />}
//         {currentPage === 'Upload Bill' && <UploadBill userId={userId} goDashboard={()=>go('Dashboard')} />}
//         {currentPage === 'Command' && <Command userId={userId} goDashboard={()=>go('Dashboard')} />}
//         {currentPage === 'Dashboard' && <Dashboard userEmail={userEmail} goHome={()=>go('Home')} goUpload={()=>go('Upload Bill')} goCommand={()=>go('Command')} />}
//       </main>
//     </div>
//   )
// }

// export default App


import React, { useEffect, useState } from "react";
import "./App.css"
// Single-file React component to mirror the provided Streamlit UI
// - Uses Tailwind CSS for styling (assumes Tailwind is configured in the project)
// - Keeps backend unchanged: replace fetch URLs with your existing endpoints
// - Uses localStorage to persist session (similar to st.session_state)

export default function App() {
  const [currentPage, setCurrentPage] = useState(() => {
    return localStorage.getItem("sahayogi_current_page") || "Home";
  });
  const [userId, setUserId] = useState(() => {
    return localStorage.getItem("sahayogi_user_id") || null;
  });
  const [userEmail, setUserEmail] = useState(() => {
    return localStorage.getItem("sahayogi_user_email") || null;
  });

  useEffect(() => {
    localStorage.setItem("sahayogi_current_page", currentPage);
  }, [currentPage]);

  useEffect(() => {
    if (userId) localStorage.setItem("sahayogi_user_id", userId);
    else localStorage.removeItem("sahayogi_user_id");
  }, [userId]);

  useEffect(() => {
    if (userEmail) localStorage.setItem("sahayogi_user_email", userEmail);
    else localStorage.removeItem("sahayogi_user_email");
  }, [userEmail]);

  // Small helper for API calls — replace endpoints as needed
  const api = async (path, options = {}) => {
    const base = process.env.REACT_APP_API_BASE || ""; // set in .env if needed
    try {
      const res = await fetch(base + path, options);
      const json = await res.json();
      return { ok: res.ok, json };
    } catch (err) {
      return { ok: false, error: err.message };
    }
  };

  const logout = () => {
    setUserId(null);
    setUserEmail(null);
    setCurrentPage("Home");
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-indigo-500 to-purple-700 text-gray-900">
      <div className="max-w-7xl mx-auto px-4 py-8">
        <div className="grid grid-cols-12 gap-6">
          {/* SIDEBAR */}
          <aside className="col-span-12 md:col-span-3 lg:col-span-2 bg-transparent">
            <div className="bg-white/6 rounded-2xl p-4 backdrop-blur-sm border border-white/10">
              <h2 className="text-center text-white text-xl">🏪 SahaYOGI</h2>
              <p className="text-center text-gray-200 text-sm">Intelligent Shop Assistant</p>

              <div className="my-4 border-t border-white/10 pt-4">
                <label className="sr-only">Navigation</label>
                <select
                  value={currentPage}
                  onChange={(e) => setCurrentPage(e.target.value)}
                  className="w-full bg-white/5 p-2 rounded-md text-white"
                >
                  <option value="Home">🏠 Home</option>
                  <option value="Login">🔐 Login</option>
                  <option value="Register">📝 Register</option>
                  <option value="Upload Bill">🧾 Upload Bill</option>
                  <option value="Command">🎤 Command</option>
                  <option value="Dashboard">📊 Dashboard</option>
                </select>
              </div>

              <div className="my-4">
                {userId ? (
                  <div>
                    <h3 className="text-sm text-gray-200">📈 Your Stats</h3>
                    <div className="grid grid-cols-2 gap-2 mt-2">
                      <div className="bg-white/6 p-2 rounded">
                        <div className="text-xs text-gray-300">Sales</div>
                        <div className="font-bold text-white">₹12,450</div>
                      </div>
                      <div className="bg-white/6 p-2 rounded">
                        <div className="text-xs text-gray-300">Customers</div>
                        <div className="font-bold text-white">24</div>
                      </div>
                    </div>
                    <button
                      onClick={logout}
                      className="mt-4 w-full bg-white text-indigo-600 font-semibold py-2 rounded-lg"
                    >
                      🚪 Logout
                    </button>
                  </div>
                ) : (
                  <p className="text-center text-gray-300">Not logged in</p>
                )}
              </div>
            </div>
          </aside>

          {/* MAIN AREA */}
          <main className="col-span-12 md:col-span-9 lg:col-span-10">
            <div className="main-container bg-transparent">
              {currentPage === "Home" && (
                <Home
                  goTo={(page) => setCurrentPage(page)}
                  setUserId={setUserId}
                  setUserEmail={setUserEmail}
                />
              )}

              {currentPage === "Login" && (
                <Login
                  onLogin={(id, email) => {
                    setUserId(id);
                    setUserEmail(email);
                    setCurrentPage("Dashboard");
                  }}
                  goBack={() => setCurrentPage("Home")}
                  api={api}
                />
              )}

              {currentPage === "Register" && (
                <Register
                  onRegister={(id, email) => {
                    setUserId(id);
                    setUserEmail(email);
                    setCurrentPage("Dashboard");
                  }}
                  goBack={() => setCurrentPage("Home")}
                  api={api}
                />
              )}

              {currentPage === "Upload Bill" && (
                <UploadBill
                  userId={userId}
                  goBack={() => setCurrentPage("Dashboard")}
                  api={api}
                />
              )}

              {currentPage === "Command" && (
                <Command
                  userId={userId}
                  goBack={() => setCurrentPage("Dashboard")}
                  api={api}
                />
              )}

              {currentPage === "Dashboard" && (
                <Dashboard
                  userEmail={userEmail}
                  goHome={() => setCurrentPage("Home")}
                  goPage={(p) => setCurrentPage(p)}
                />
              )}
            </div>
          </main>
        </div>
      </div>
    </div>
  );
}

// ---------------------------
// Subcomponents
// ---------------------------

function Home({ goTo, setUserId, setUserEmail }) {
  return (
    <div className="p-8 rounded-2xl">
      <h1 className="text-5xl font-extrabold text-white text-center">SahaYOGI</h1>
      <p className="text-center text-gray-200 max-w-2xl mx-auto mt-4">
        An intelligent assistant designed to modernize shop management with AI-powered tools, helping
        small businesses thrive in the digital age.
      </p>

      <div className="stats-container flex justify-center gap-6 mt-8 flex-wrap">
        <Stat number="99%" label="Accuracy" />
        <Stat number="24/7" label="Availability" />
        <Stat number="1000+" label="Shops Empowered" />
      </div>

      <div className="features-grid grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mt-10">
        <Feature icon="🧾" title="Intelligent Bill Scanning" desc="Automatically extract item details from any bill or receipt with our advanced OCR technology. Save hours of manual data entry." />
        <Feature icon="📊" title="Smart Analytics Dashboard" desc="Gain real-time insights into your sales, inventory, and customer trends with beautifully visualized data and reports." />
        <Feature icon="🎙️" title="Voice-Activated Commands" desc="Manage transactions, check stock, or update records using simple voice commands. Hands-free operation for busy shopkeepers." />
        <Feature icon="🤝" title="Customer Credit Management" desc="Effortlessly track udhaar, send payment reminders, and maintain customer relationships with our integrated credit system." />
      </div>

      <div className="cta-section bg-white/6 backdrop-blur-sm rounded-2xl p-10 mt-12 border border-white/10 text-center">
        <h2 className="text-3xl font-bold text-white">Ready to Transform Your Shop?</h2>
        <p className="text-gray-200 max-w-2xl mx-auto mt-4">Join thousands of shopkeepers who have modernized their businesses with SahaYOGI. Start your 14-day free trial with no credit card required.</p>

        <div className="mt-6 flex justify-center gap-4">
          <button
            onClick={() => goTo("Register")}
            className="px-8 py-3 rounded-lg font-semibold bg-white text-indigo-600"
          >
            🚀 Get Started Free
          </button>
          <button
            onClick={() => goTo("Login")}
            className="px-6 py-3 rounded-lg font-semibold border border-white/30 text-white bg-transparent"
          >
            📞 Schedule Demo
          </button>
        </div>

        <p className="text-sm text-gray-300 mt-6">No installation required • Works on any device • 24/7 support</p>
      </div>
    </div>
  );
}

function Stat({ number, label }) {
  return (
    <div className="stat-item bg-white/6 rounded-xl px-6 py-6 text-center min-w-[160px] border border-white/20">
      <div className="stat-number text-4xl font-extrabold text-white">{number}</div>
      <div className="stat-label text-gray-200 mt-2">{label}</div>
    </div>
  );
}

function Feature({ icon, title, desc }) {
  return (
    <div className="feature-card bg-white p-6 rounded-2xl shadow-lg hover:translate-y-[-6px] transition-transform">
      <div className="feature-icon text-3xl mb-3">{icon}</div>
      <h3 className="feature-title text-lg font-bold text-gray-800">{title}</h3>
      <p className="feature-desc text-gray-500 mt-2">{desc}</p>
    </div>
  );
}

// ---------------------------
// Login
// ---------------------------
function Login({ onLogin, goBack, api }) {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const submit = async (e) => {
    e.preventDefault();
    setError(null);
    if (!email || !password) return setError("Please fill all fields");
    setLoading(true);

    // Replace with your login endpoint. Below is demo logic similar to Streamlit's "simulate login"
    // const res = await api('/auth/login', { method: 'POST', body: JSON.stringify({email, password}) });
    setTimeout(() => {
      setLoading(false);
      // simulate success
      const id = "demo_user_123";
      onLogin(id, email);
    }, 800);
  };

  return (
    <div className="bg-transparent p-6 rounded-2xl">
      <h1 className="text-center text-white text-2xl">🔐 Login to SahaYOGI</h1>

      <form onSubmit={submit} className="max-w-xl mx-auto mt-6 bg-white/6 p-6 rounded-lg border border-white/10">
        <label className="block text-gray-200">📧 Email Address</label>
        <input value={email} onChange={(e) => setEmail(e.target.value)} placeholder="shopkeeper@example.com" className="w-full mt-2 p-2 rounded bg-white/5 text-white" />

        <label className="block text-gray-200 mt-4">🔒 Password</label>
        <input value={password} onChange={(e) => setPassword(e.target.value)} type="password" placeholder="Enter your password" className="w-full mt-2 p-2 rounded bg-white/5 text-white" />

        {error && <div className="text-red-400 mt-3">❌ {error}</div>}

        <div className="mt-6 grid grid-cols-2 gap-4">
          <button type="submit" className="py-2 bg-white text-indigo-600 rounded font-semibold">🚀 Login</button>
          <button type="button" onClick={goBack} className="py-2 border border-white/30 rounded text-white">⬅️ Back to Home</button>
        </div>
      </form>
    </div>
  );
}

// ---------------------------
// Register
// ---------------------------
function Register({ onRegister, goBack, api }) {
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [error, setError] = useState(null);

  const submit = async (e) => {
    e.preventDefault();
    setError(null);
    if (!name || !email || !password || !confirmPassword) return setError("Please fill all fields");
    if (password !== confirmPassword) return setError("Passwords don't match!");

    // Replace with actual register API call
    setTimeout(() => {
      const id = "new_user_" + email.split("@")[0];
      onRegister(id, email);
    }, 600);
  };

  return (
    <div className="p-6">
      <h1 className="text-center text-white text-2xl">📝 Create Your Account</h1>

      <form onSubmit={submit} className="max-w-xl mx-auto mt-6 bg-white/6 p-6 rounded-lg border border-white/10">
        <label className="block text-gray-200">👤 Full Name</label>
        <input value={name} onChange={(e) => setName(e.target.value)} placeholder="Enter your full name" className="w-full mt-2 p-2 rounded bg-white/5 text-white" />

        <label className="block text-gray-200 mt-4">📧 Email Address</label>
        <input value={email} onChange={(e) => setEmail(e.target.value)} placeholder="shopkeeper@example.com" className="w-full mt-2 p-2 rounded bg-white/5 text-white" />

        <label className="block text-gray-200 mt-4">🔒 Password</label>
        <input value={password} onChange={(e) => setPassword(e.target.value)} type="password" placeholder="Create a strong password" className="w-full mt-2 p-2 rounded bg-white/5 text-white" />

        <label className="block text-gray-200 mt-4">✓ Confirm Password</label>
        <input value={confirmPassword} onChange={(e) => setConfirmPassword(e.target.value)} type="password" placeholder="Re-enter your password" className="w-full mt-2 p-2 rounded bg-white/5 text-white" />

        {error && <div className="text-red-400 mt-3">❌ {error}</div>}

        <div className="mt-6 grid grid-cols-2 gap-4">
          <button type="submit" className="py-2 bg-white text-indigo-600 rounded font-semibold">✨ Create Account</button>
          <button type="button" onClick={goBack} className="py-2 border border-white/30 rounded text-white">⬅️ Back to Home</button>
        </div>
      </form>
    </div>
  );
}

// ---------------------------
// Upload Bill
// ---------------------------
function UploadBill({ userId, goBack, api }) {
  const [file, setFile] = useState(null);
  const [customerName, setCustomerName] = useState("Walk-in Customer");
  const [msg, setMsg] = useState(null);

  const upload = async () => {
    if (!userId) return setMsg({ type: "warn", text: "Please login first!" });
    if (!file) return setMsg({ type: "error", text: "Please select a file" });

    // Example using FormData to send file to backend
    const form = new FormData();
    form.append("file", file);
    form.append("customer_name", customerName);
    form.append("user_id", userId);

    // Replace '/api/process-bill' with your OCR endpoint
    try {
      // const res = await fetch('/api/process-bill', { method: 'POST', body: form });
      // const json = await res.json();
      // demo success
      setMsg({ type: "success", text: `✅ Bill uploaded for ${customerName}!` });
    } catch (err) {
      setMsg({ type: "error", text: "Upload failed" });
    }
  };

  return (
    <div className="p-6">
      <h1 className="text-center text-white text-2xl">🧾 Upload Bill</h1>

      {!userId ? (
        <div className="mt-6 text-center">
          <p className="text-yellow-200">⚠️ Please login first!</p>
          <div className="mt-4">
            <button onClick={() => window.scrollTo(0, 0)} className="py-2 px-4 bg-white text-indigo-600 rounded">Go to Login</button>
          </div>
        </div>
      ) : (
        <div className="max-w-2xl mx-auto mt-6 bg-white/6 p-6 rounded-lg border border-white/10">
          <p className="text-gray-200">Upload a bill image and our AI will extract items automatically</p>

          <div className="mt-4">
            <input type="file" accept="image/*" onChange={(e) => setFile(e.target.files[0])} className="text-sm text-gray-200" />
          </div>

          <div className="mt-4">
            <label className="text-gray-200">Customer Name</label>
            <input value={customerName} onChange={(e) => setCustomerName(e.target.value)} className="w-full mt-2 p-2 rounded bg-white/5 text-white" />
          </div>

          <div className="mt-6 grid grid-cols-2 gap-4">
            <button onClick={upload} className="py-2 bg-white text-indigo-600 rounded font-semibold">📤 Upload & Process</button>
            <button onClick={goBack} className="py-2 border border-white/30 rounded text-white">⬅️ Back to Dashboard</button>
          </div>

          {msg && (
            <div className={`mt-4 ${msg.type === "success" ? "text-green-400" : msg.type === "error" ? "text-red-400" : "text-yellow-200"}`}>{msg.text}</div>
          )}
        </div>
      )}
    </div>
  );
}

// ---------------------------
// Command (voice/text)
// ---------------------------
function Command({ userId, goBack, api }) {
  const [command, setCommand] = useState("");
  const [message, setMessage] = useState(null);

  const execute = async () => {
    if (!userId) return setMessage({ type: "warn", text: "Please login first!" });
    if (!command) return setMessage({ type: "error", text: "Please enter a command" });

    // Replace with your command endpoint
    try {
      // const res = await api('/api/execute-command', { method: 'POST', body: JSON.stringify({ userId, command }) });
      setMessage({ type: "success", text: `✅ Command executed: ${command}` });
      setCommand("");
    } catch (err) {
      setMessage({ type: "error", text: "Command failed" });
    }
  };

  return (
    <div className="p-6">
      <h1 className="text-center text-white text-2xl">🎤 Voice Commands</h1>

      {!userId ? (
        <div className="mt-6 text-center">
          <p className="text-yellow-200">⚠️ Please login first!</p>
          <div className="mt-4">
            <button onClick={() => window.scrollTo(0, 0)} className="py-2 px-4 bg-white text-indigo-600 rounded">Go to Login</button>
          </div>
        </div>
      ) : (
        <div className="max-w-2xl mx-auto mt-6 bg-white/6 p-6 rounded-lg border border-white/10">
          <p className="text-gray-200">Type or speak commands to manage your shop</p>

          <textarea
            value={command}
            onChange={(e) => setCommand(e.target.value)}
            placeholder="Example: 'add udhaar Ramesh sugar 50' or 'show today sales'"
            className="w-full mt-4 p-3 rounded bg-white/5 text-white h-28"
          />

          <div className="mt-4">
  <VoiceRecorder />

  <div className="grid grid-cols-2 gap-3 mt-4">
    <button onClick={execute} className="py-2 rounded bg-white text-indigo-600">
      🚀 Execute
    </button>

    <button onClick={goBack} className="py-2 rounded border border-white/30 text-white">
      ⬅️ Back
    </button>
  </div>
</div>

          {message && <div className={`mt-4 ${message.type === "success" ? "text-green-400" : message.type === "error" ? "text-red-400" : "text-yellow-200"}`}>{message.text}</div>}
        </div>
      )}
    </div>
  );
}

// ---------------------------
// Dashboard
// ---------------------------
function Dashboard({ userEmail, goHome, goPage }) {
  // sample data hard-coded same as Streamlit example
  const data = [
    { Customer: "Ramesh", Item: "Sugar 5kg", Amount: 250, Type: "Sale", Time: "10:30 AM" },
    { Customer: "Suresh", Item: "Rice 10kg", Amount: 450, Type: "Udhaar", Time: "11:15 AM" },
    { Customer: "Priya", Item: "Oil 1L", Amount: 180, Type: "Sale", Time: "12:45 PM" },
    { Customer: "Mohan", Item: "Flour 5kg", Amount: 120, Type: "Udhaar", Time: "2:20 PM" },
    { Customer: "Ankit", Item: "Tea 500g", Amount: 150, Type: "Sale", Time: "4:10 PM" }
  ];

  return (
    <div className="p-6">
      <h1 className="text-center text-white text-2xl">📊 Dashboard</h1>

      <div className="mt-4 text-center text-gray-200">Welcome, {userEmail || "Guest"}</div>

      <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mt-6">
        <Metric title="Today's Sales" value="₹12,450" delta="+8.5%" />
        <Metric title="Total Udhaar" value="₹8,920" delta="3 customers" />
        <Metric title="Bills Today" value="12" delta="+2" />
        <Metric title="Customers" value="24" delta="+3" />
      </div>

      <h3 className="text-white mt-8">🚀 Quick Actions</h3>
      <div className="grid grid-cols-1 sm:grid-cols-4 gap-4 mt-3">
        <button onClick={() => goPage("Upload Bill")} className="py-3 rounded bg-white text-indigo-600">🧾 Upload Bill</button>
        <button onClick={() => goPage("Command")} className="py-3 rounded bg-white text-indigo-600">🎤 Voice Command</button>
        <button onClick={() => alert("Feature coming soon!")} className="py-3 rounded border border-white/30 text-white">👥 Add Customer</button>
        <button onClick={() => alert("Feature coming soon!")} className="py-3 rounded border border-white/30 text-white">📈 View Reports</button>
      </div>

      <h3 className="text-white mt-8">📋 Recent Transactions</h3>

      <div className="mt-4 overflow-x-auto bg-white/6 rounded-lg p-4 border border-white/10">
        <table className="min-w-full text-left">
          <thead>
            <tr className="text-gray-200 text-sm">
              <th className="p-2">Customer</th>
              <th className="p-2">Item</th>
              <th className="p-2">Amount</th>
              <th className="p-2">Type</th>
              <th className="p-2">Time</th>
            </tr>
          </thead>
          <tbody>
            {data.map((row, i) => (
              <tr key={i} className="border-t border-white/10 text-white/90">
                <td className="p-2">{row.Customer}</td>
                <td className="p-2">{row.Item}</td>
                <td className="p-2">₹{row.Amount}</td>
                <td className="p-2">{row.Type}</td>
                <td className="p-2">{row.Time}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      <div className="mt-6">
        <button onClick={goHome} className="py-2 px-4 bg-white text-indigo-600 rounded">🏠 Back to Home</button>
      </div>
    </div>
  );
}

function Metric({ title, value, delta }) {
  return (
    <div className="bg-white/6 p-4 rounded-lg border border-white/10 text-white">
      <div className="text-sm text-gray-300">{title}</div>
      <div className="text-2xl font-bold mt-2">{value}</div>
      <div className="text-sm text-gray-300">{delta}</div>
    </div>
  );
}
