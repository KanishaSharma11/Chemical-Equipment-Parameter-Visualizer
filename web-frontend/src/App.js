import React, { useState, useEffect } from "react";
import ReactMarkdown from "react-markdown";
import { uploadCSV, getHistory, getPDF } from "./api";
import { Bar, Pie } from "react-chartjs-2";
import "chart.js/auto";
import "./App.css";



function App() {
  const [file, setFile] = useState(null);
  const [user, setUser] = useState("");
  const [passw, setPassw] = useState("");
  const [history, setHistory] = useState([]);
  const [loading, setLoading] = useState(false);
  const [uploading, setUploading] = useState(false);
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [showPassword, setShowPassword] = useState(false);
  const [expandedCard, setExpandedCard] = useState(null);
  const [currentView, setCurrentView] = useState("upload"); // 'upload' or 'history'
  const [currentAnalysis, setCurrentAnalysis] = useState(null);
  const [insights, setInsights] = useState("");
  const [loadingInsights, setLoadingInsights] = useState(false);

  const fetchHistory = async () => {
    try {
      setLoading(true);
      const res = await getHistory(user, passw);
      setHistory(res.data.history || []);
    } catch (e) {
      console.error(e);
      setHistory([]);
    } finally {
      setLoading(false);
    }
  };

  const handleLogin = async () => {
    try {
      setLoading(true);
      await fetchHistory();
      setIsLoggedIn(true);
    } catch (e) {
      alert("Invalid username or password");
      setIsLoggedIn(false);
    } finally {
      setLoading(false);
    }
  };

  const handleUpload = async () => {
    if (!file) return alert("Please select a CSV file");
    try {
      setUploading(true);
      await uploadCSV(file, user, passw);
      alert("File uploaded successfully!");
      setFile(null);
      document.querySelector('input[type="file"]').value = "";
      await fetchHistory();
      
      // Show the most recent upload as current analysis
      const res = await getHistory(user, passw);
      if (res.data.history && res.data.history.length > 0) {
        setCurrentAnalysis(res.data.history[0]);
        setCurrentView("upload");
      }
    } catch (e) {
      alert(e.response?.data?.error || e.message);
    } finally {
      setUploading(false);
    }
  };

  const handleLogout = () => {
    setIsLoggedIn(false);
    setUser("");
    setPassw("");
    setHistory([]);
    setCurrentAnalysis(null);
    setCurrentView("upload");
  };

  const toggleCard = (id) => {
    setExpandedCard(expandedCard === id ? null : id);
  };

  const fetchAIInsights = async (analysisData) => {
  try {
    setLoadingInsights(true);

    const GEMINI_API_KEY = GEMINI_API;

    if (!GEMINI_API_KEY) {
      setInsights("AI key missing. Please configure your Gemini API key.");
      setLoadingInsights(false);
      return;
    }

    const prompt = `
You are an expert AI system that analyzes chemical equipment operational data.  
Format your response ONLY using clean markdown bullet points, headings, and short explanations.

### Input Data
${JSON.stringify(analysisData, null, 2)}

### REQUIRED OUTPUT FORMAT
Respond EXACTLY in the structure below:

## 🔍 Key Observations
- Point 1
- Point 2
- Point 3

## ⚠️ Anomalies or Unusual Readings
- Point 1
- Point 2
- Point 3

## 🛠 Recommended Operational Actions
1. Step-by-step actionable recommendation
2. Another step
3. Another step

## 🚨 Potential Risks or Warnings
- Risk 1
- Risk 2
- Risk 3

## 📝 Summary
1. Summary step 1
2. Summary step 2
3. Summary step 3

Rules:
- DO NOT return paragraphs.
- DO NOT include unnecessary explanation.
- MUST use bullet points, numbering, and headings.
- Keep each point short, crisp, and professional.
`;

    const response = await fetch(
      `https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-pro:generateContent?key=${GEMINI_API_KEY}`,
      {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          contents: [{ parts: [{ text: prompt }] }],
        }),
      }
    );

    const result = await response.json();
    console.log("GEMINI RAW RESPONSE:", result);

    // ✅ Extract Gemini output safely
    const aiText =
      result?.candidates?.[0]?.content?.parts?.[0]?.text ||
      "No insights generated.";

    setInsights(aiText);
  } catch (err) {
    console.error("Gemini Error:", err);
    setInsights("Failed to generate insights.");
  } finally {
    setLoadingInsights(false);
  }
};


  // Fetch insights when current analysis changes
  useEffect(() => {
    if (currentAnalysis) {
      fetchAIInsights(currentAnalysis);
    }
  }, [currentAnalysis]);

  const renderAnalysisCharts = (data) => {
    if (!data || !data.summary_json) return null;

    return (
      <div className="charts-container">
        <div className="chart-wrapper">
          <h4 className="chart-title">Average Values</h4>
          <Bar
            data={{
              labels: Object.keys(data.summary_json?.averages || {}),
              datasets: [
                {
                  label: "Averages",
                  data: Object.values(data.summary_json?.averages || {}),
                  backgroundColor: "rgba(99, 102, 241, 0.7)",
                  borderColor: "rgba(99, 102, 241, 1)",
                  borderWidth: 2,
                },
              ],
            }}
            options={{
              responsive: true,
              maintainAspectRatio: true,
              plugins: {
                legend: { display: false },
              },
            }}
          />
        </div>
        <div className="chart-wrapper">
          <h4 className="chart-title">Type Distribution</h4>
          <Pie
            data={{
              labels: Object.keys(data.summary_json?.type_distribution || {}),
              datasets: [
                {
                  data: Object.values(data.summary_json?.type_distribution || {}),
                  backgroundColor: [
                    "rgba(239, 68, 68, 0.7)",
                    "rgba(59, 130, 246, 0.7)",
                    "rgba(34, 197, 94, 0.7)",
                    "rgba(234, 179, 8, 0.7)",
                    "rgba(168, 85, 247, 0.7)",
                    "rgba(236, 72, 153, 0.7)",
                  ],
                  borderColor: "#fff",
                  borderWidth: 2,
                },
              ],
            }}
            options={{
              responsive: true,
              maintainAspectRatio: true,
              plugins: {
                legend: { position: "bottom" },
              },
            }}
          />
        </div>
      </div>
    );
  };

  // Login Screen
  if (!isLoggedIn) {
    return (
      <div className="app-container">
        <div className="header">
          <div className="header-content">
            <h1 className="title">
              <span className="icon">⚗️</span>
              Chemical Equipment Visualizer
            </h1>
            <p className="subtitle">Analyze and visualize your chemical equipment data</p>
          </div>
        </div>

        <div className="main-content">
          <video
            className="background-video"
            autoPlay
            loop
            muted
            playsInline
          >
            <source src="./7565445-hd_1920_1080_25fps.mp4" type="video/mp4" />
          </video>

          <div className="auth-section">
            <div className="card auth-card">
              <h2 className="card-title">🔐 Login</h2>

              <div className="input-group">
                <div className="input-wrapper">
                  <label>Username</label>
                  <input
                    className="input"
                    placeholder="Enter username"
                    value={user}
                    onChange={(e) => setUser(e.target.value)}
                  />
                </div>

                <div className="input-wrapper">
                  <label>Password</label>
                  <div className="password-field">
                    <input
                      className="input"
                      placeholder="Enter password"
                      type={showPassword ? "text" : "password"}
                      value={passw}
                      onChange={(e) => setPassw(e.target.value)}
                    />
                    <button
                      className="toggle-password"
                      onClick={() => setShowPassword(!showPassword)}
                    >
                      {showPassword ? "👁️" : "👁️‍🗨️"}
                    </button>
                  </div>
                </div>
              </div>

              <button
                className="btn btn-primary"
                onClick={handleLogin}
                disabled={!user || !passw || loading}
                style={{ marginTop: "15px", width: "100%" }}
              >
                {loading ? "Checking..." : "Login"}
              </button>
            </div>
          </div>
        </div>
      </div>
    );
  }

  // Main App with Navigation
  return (
    <div className="app-container">
      <video
            className="background-video"
            autoPlay
            loop
            muted
            playsInline
          >
            <source src="./7565445-hd_1920_1080_25fps.mp4" type="video/mp4" />
          </video>
      {/* Navigation Bar */}
      <nav className="navbar">
        <div className="navbar-content">
          <div className="navbar-left">
            <h1 className="navbar-title">
              <span className="icon">⚗️</span>
              Chemical Equipment Visualizer
            </h1>
          </div>
          <div className="navbar-center">
            <button
              className={`nav-btn ${currentView === "upload" ? "active" : ""}`}
              onClick={() => setCurrentView("upload")}
            >
              📤 Upload & Analyze
            </button>
            <button
              className={`nav-btn ${currentView === "history" ? "active" : ""}`}
              onClick={() => setCurrentView("history")}
            >
              📊 Analysis History
            </button>
          </div>
          <div className="navbar-right">
            <span className="user-greeting">Hey, {user}!</span>
            <button className="btn-logout" onClick={handleLogout}>
              Logout
            </button>
          </div>
        </div>
      </nav>

      <div className="main-content">
        {/* Upload & Analysis View */}
        {currentView === "upload" && (
          <>
            <div className="upload-section">
              <div className="card upload-card">
                <h2 className="card-title">📤 Upload CSV File</h2>
                <div className="upload-area">
                  <input
                    type="file"
                    accept=".csv"
                    onChange={(e) => setFile(e.target.files[0])}
                    className="file-input"
                    id="file-input"
                  />
                  <label htmlFor="file-input" className="file-label">
                    <span className="file-icon">📁</span>
                    <span className="file-text">
                      {file ? file.name : "Choose a CSV file"}
                    </span>
                  </label>
                  <button
                    onClick={handleUpload}
                    className={`btn btn-primary ${uploading ? "loading" : ""}`}
                    disabled={!file || uploading}
                  >
                    {uploading ? "Uploading..." : "Upload & Analyze"}
                  </button>
                </div>
              </div>
            </div>

            {/* Current Analysis Results */}
            {currentAnalysis && (
              <div className="current-analysis-section">
                <div className="section-header">
                  <h2 className="section-title">📈 Current Analysis</h2>
                </div>

                <div className="card analysis-card">
                  <div className="analysis-header">
                    <h3 className="analysis-filename">{currentAnalysis.original_filename}</h3>
                    <p className="analysis-date">
                      {new Date(currentAnalysis.uploaded_at).toLocaleString()}
                    </p>
                    <div className="stat-badge">
                      <span className="stat-label">Total Count</span>
                      <span className="stat-value">{currentAnalysis.summary_json?.total_count || 0}</span>
                    </div>
                  </div>

                  {renderAnalysisCharts(currentAnalysis)}
                </div>

                {/* AI Insights Section */}
                <div className="insights-section">
                  <div className="card insights-card">
                    <h2 className="card-title">🤖 AI-Powered Insights</h2>
                    {loadingInsights ? (
                      <div className="loading-state">
                        <div className="spinner-large"></div>
                        <p>Generating insights...</p>
                      </div>
                    ) : (
                      <div className="insights-content">

                        <div className="insights-markdown">
                          <ReactMarkdown>{insights}</ReactMarkdown>
                        </div>

                        <button
                          className="btn btn-secondary"
                          onClick={() => fetchAIInsights(currentAnalysis)}
                          style={{ marginTop: "15px" }}
                        >
                          🔄 Refresh Insights
                        </button>
                      </div>
                    )}
                  </div>
                </div>
              </div>
            )}
          </>
        )}

        {/* History View */}
        {currentView === "history" && (
          <div className="history-section">
            <div className="section-header">
              <h2 className="section-title">📊 Analysis History</h2>
              {loading && <div className="spinner"></div>}
            </div>

            {loading && history.length === 0 ? (
              <div className="loading-state">
                <div className="spinner-large"></div>
                <p>Loading your history...</p>
              </div>
            ) : history.length === 0 ? (
              <div className="empty-state">
                <span className="empty-icon">📭</span>
                <h3>No uploads yet</h3>
                <p>Upload your first CSV file to see analysis results</p>
              </div>
            ) : (
              <div className="history-grid">
                {history.map((h) => (
                  <div
                    key={h.id}
                    className={`history-card ${expandedCard === h.id ? "expanded" : ""}`}
                  >
                    <div className="history-header" onClick={() => toggleCard(h.id)}>
                      <div className="history-info">
                        <h3 className="history-filename">{h.original_filename}</h3>
                        <p className="history-date">
                          {new Date(h.uploaded_at).toLocaleString()}
                        </p>
                      </div>
                      <div className="history-stats">
                        <div className="stat-badge">
                          <span className="stat-label">Total</span>
                          <span className="stat-value">{h.summary_json?.total_count || 0}</span>
                        </div>
                        <button className="expand-btn">
                          {expandedCard === h.id ? "▼" : "▶"}
                        </button>
                      </div>
                    </div>

                    {expandedCard === h.id && (
                      <div className="history-details">
                        {renderAnalysisCharts(h)}
                      </div>
                    )}
                  </div>
                ))}
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
}

export default App;
