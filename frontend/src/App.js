import React, { useState, useEffect } from 'react';
import './App.css';

const App = () => {
  const [currentView, setCurrentView] = useState('dashboard');
  const [meetings, setMeetings] = useState([]);
  const [dashboardData, setDashboardData] = useState({});
  const [bunnyStats, setBunnyStats] = useState({});
  const [dailyContent, setDailyContent] = useState({});
  const [loading, setLoading] = useState(false);
  const [notification, setNotification] = useState('');

  const API_BASE = process.env.REACT_APP_BACKEND_URL || 'http://localhost:8001';

  // Initialize app
  useEffect(() => {
    fetchDashboardData();
    fetchBunnyStats();
    fetchDailyContent();
  }, []);

  const fetchDashboardData = async () => {
    try {
      const response = await fetch(`${API_BASE}/api/dashboard`);
      const data = await response.json();
      setDashboardData(data);
    } catch (error) {
      console.error('Error fetching dashboard data:', error);
    }
  };

  const fetchBunnyStats = async () => {
    try {
      const response = await fetch(`${API_BASE}/api/bunny/stats/default`);
      const data = await response.json();
      setBunnyStats(data);
    } catch (error) {
      console.error('Error fetching bunny stats:', error);
    }
  };

  const fetchDailyContent = async () => {
    try {
      const [jokeRes, factRes, mindfulRes] = await Promise.all([
        fetch(`${API_BASE}/api/ai/joke`),
        fetch(`${API_BASE}/api/ai/fluffy-fact`),
        fetch(`${API_BASE}/api/ai/mindful-moment`)
      ]);
      
      const [joke, fact, mindful] = await Promise.all([
        jokeRes.json(),
        factRes.json(),
        mindfulRes.json()
      ]);
      
      setDailyContent({ joke, fact, mindful });
    } catch (error) {
      console.error('Error fetching daily content:', error);
    }
  };

  const interactWithBunny = async (type) => {
    try {
      const response = await fetch(`${API_BASE}/api/bunny/interact?interaction_type=${type}&user_id=default`, {
        method: 'POST'
      });
      const data = await response.json();
      
      showNotification(`🐰 ${data.response} (+${data.gems_earned} gem!)`);
      fetchBunnyStats();
    } catch (error) {
      console.error('Error interacting with bunny:', error);
    }
  };

  const showNotification = (message) => {
    setNotification(message);
    setTimeout(() => setNotification(''), 4000);
  };

  const MeetingScheduler = () => {
    const [formData, setFormData] = useState({
      title: '',
      date: '',
      time: '',
      timezone: 'UTC',
      platform: 'zoom',
      meeting_link: '',
      meeting_id: '',
      passcode: '',
      host_name: '',
      agenda: '',
      duration: 60,
      rsvp_status: 'pending',
      mic_muted: true,
      camera_off: true,
      recurrence: 'none',
      reminder_times: [5],
      backup_link: '',
      join_method: 'browser',
      waiting_room_message: '',
      attachments: []
    });

    const handleSubmit = async (e) => {
      e.preventDefault();
      setLoading(true);
      
      try {
        const response = await fetch(`${API_BASE}/api/meetings`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify(formData)
        });
        
        const data = await response.json();
        showNotification('✨ Meeting scheduled successfully! Your royal decree has been recorded! 📜');
        
        // Reset form
        setFormData({
          title: '',
          date: '',
          time: '',
          timezone: 'UTC',
          platform: 'zoom',
          meeting_link: '',
          meeting_id: '',
          passcode: '',
          host_name: '',
          agenda: '',
          duration: 60,
          rsvp_status: 'pending',
          mic_muted: true,
          camera_off: true,
          recurrence: 'none',
          reminder_times: [5],
          backup_link: '',
          join_method: 'browser',
          waiting_room_message: '',
          attachments: []
        });
        
        fetchDashboardData();
      } catch (error) {
        showNotification('❌ Error scheduling meeting. Please try again.');
      } finally {
        setLoading(false);
      }
    };

    return (
      <div className="royal-scroll">
        <h2 className="royal-title">📜 Royal Decree - Meeting Scheduler</h2>
        <form onSubmit={handleSubmit} className="royal-form">
          <div className="form-grid">
            <div className="form-group">
              <label className="royal-label">✨ Meeting Title</label>
              <input
                type="text"
                value={formData.title}
                onChange={(e) => setFormData({...formData, title: e.target.value})}
                className="royal-input"
                required
                placeholder="Enter your royal gathering title..."
              />
            </div>
            
            <div className="form-group">
              <label className="royal-label">📅 Date</label>
              <input
                type="date"
                value={formData.date}
                onChange={(e) => setFormData({...formData, date: e.target.value})}
                className="royal-input"
                required
              />
            </div>
            
            <div className="form-group">
              <label className="royal-label">🕐 Time</label>
              <input
                type="time"
                value={formData.time}
                onChange={(e) => setFormData({...formData, time: e.target.value})}
                className="royal-input"
                required
              />
            </div>
            
            <div className="form-group">
              <label className="royal-label">🌍 Platform</label>
              <select
                value={formData.platform}
                onChange={(e) => setFormData({...formData, platform: e.target.value})}
                className="royal-select"
              >
                <option value="zoom">Zoom</option>
                <option value="google-meet">Google Meet</option>
                <option value="teams">Microsoft Teams</option>
                <option value="other">Other</option>
              </select>
            </div>
            
            <div className="form-group full-width">
              <label className="royal-label">🔗 Meeting Link</label>
              <input
                type="url"
                value={formData.meeting_link}
                onChange={(e) => setFormData({...formData, meeting_link: e.target.value})}
                className="royal-input"
                placeholder="https://zoom.us/j/..."
                required
              />
            </div>
            
            <div className="form-group">
              <label className="royal-label">🆔 Meeting ID</label>
              <input
                type="text"
                value={formData.meeting_id}
                onChange={(e) => setFormData({...formData, meeting_id: e.target.value})}
                className="royal-input"
                placeholder="123 456 7890"
              />
            </div>
            
            <div className="form-group">
              <label className="royal-label">🔒 Passcode</label>
              <input
                type="password"
                value={formData.passcode}
                onChange={(e) => setFormData({...formData, passcode: e.target.value})}
                className="royal-input"
                placeholder="Enter passcode..."
              />
            </div>
            
            <div className="form-group">
              <label className="royal-label">👤 Host Name</label>
              <input
                type="text"
                value={formData.host_name}
                onChange={(e) => setFormData({...formData, host_name: e.target.value})}
                className="royal-input"
                placeholder="Joseph Onyango"
                required
              />
            </div>
            
            <div className="form-group">
              <label className="royal-label">⏱️ Duration (minutes)</label>
              <input
                type="number"
                value={formData.duration}
                onChange={(e) => setFormData({...formData, duration: parseInt(e.target.value)})}
                className="royal-input"
                min="15"
                max="480"
              />
            </div>
            
            <div className="form-group full-width">
              <label className="royal-label">📝 Agenda</label>
              <textarea
                value={formData.agenda}
                onChange={(e) => setFormData({...formData, agenda: e.target.value})}
                className="royal-textarea"
                rows="3"
                placeholder="What shall we discuss in this royal gathering?"
              />
            </div>
            
            <div className="form-group">
              <label className="royal-label">🔄 Recurrence</label>
              <select
                value={formData.recurrence}
                onChange={(e) => setFormData({...formData, recurrence: e.target.value})}
                className="royal-select"
              >
                <option value="none">One-time</option>
                <option value="daily">Daily</option>
                <option value="weekly">Weekly</option>
                <option value="monthly">Monthly</option>
              </select>
            </div>
            
            <div className="form-group">
              <label className="royal-label">🔔 Reminder (minutes before)</label>
              <input
                type="number"
                value={formData.reminder_times[0]}
                onChange={(e) => setFormData({...formData, reminder_times: [parseInt(e.target.value)]})}
                className="royal-input"
                min="1"
                max="60"
              />
            </div>
            
            <div className="form-group checkbox-group">
              <label className="royal-checkbox">
                <input
                  type="checkbox"
                  checked={formData.mic_muted}
                  onChange={(e) => setFormData({...formData, mic_muted: e.target.checked})}
                />
                <span className="checkmark"></span>
                🎤 Join with mic muted
              </label>
            </div>
            
            <div className="form-group checkbox-group">
              <label className="royal-checkbox">
                <input
                  type="checkbox"
                  checked={formData.camera_off}
                  onChange={(e) => setFormData({...formData, camera_off: e.target.checked})}
                />
                <span className="checkmark"></span>
                📹 Join with camera off
              </label>
            </div>
          </div>
          
          <button type="submit" className="royal-button" disabled={loading}>
            {loading ? '✨ Scheduling...' : '📜 Schedule Royal Meeting'}
          </button>
        </form>
      </div>
    );
  };

  const Dashboard = () => (
    <div className="dashboard">
      <div className="greeting-banner">
        <h1>👑 Good Day, Joseph Onyango! ✨</h1>
        <p>Welcome to your magical productivity palace</p>
      </div>
      
      <div className="dashboard-grid">
        <div className="royal-card">
          <h3>📅 Today's Royal Gatherings</h3>
          <div className="meetings-list">
            {dashboardData.todays_meetings?.length > 0 ? (
              dashboardData.todays_meetings.map((meeting) => (
                <div key={meeting.id} className="meeting-card">
                  <h4>{meeting.title}</h4>
                  <p>🕐 {meeting.time} | 🌐 {meeting.platform}</p>
                  <p>👤 {meeting.host_name}</p>
                </div>
              ))
            ) : (
              <p className="no-meetings">🌟 No meetings scheduled for today!</p>
            )}
          </div>
        </div>
        
        <div className="royal-card">
          <h3>🔮 Upcoming Royal Quests</h3>
          <div className="meetings-list">
            {dashboardData.upcoming_meetings?.length > 0 ? (
              dashboardData.upcoming_meetings.slice(0, 3).map((meeting) => (
                <div key={meeting.id} className="meeting-card">
                  <h4>{meeting.title}</h4>
                  <p>📅 {meeting.date} at {meeting.time}</p>
                  <p>🌐 {meeting.platform}</p>
                </div>
              ))
            ) : (
              <p className="no-meetings">✨ Your calendar is clear ahead!</p>
            )}
          </div>
        </div>
        
        <div className="royal-card">
          <h3>😄 Daily Delight</h3>
          <div className="daily-content">
            <div className="content-item">
              <h4>🎭 Royal Joke</h4>
              <p>{dailyContent.joke?.joke || 'Loading magical humor...'}</p>
            </div>
            <div className="content-item">
              <h4>🐰 Fluffy Fact</h4>
              <p>{dailyContent.fact?.fact || 'Loading adorable wisdom...'}</p>
            </div>
          </div>
        </div>
        
        <div className="royal-card">
          <h3>🧘‍♀️ Mindful Moment</h3>
          <div className="mindful-content">
            <p>{dailyContent.mindful?.suggestion || 'Loading peaceful inspiration...'}</p>
            <button 
              className="mini-button"
              onClick={() => interactWithBunny('wisdom')}
            >
              ✨ More Wisdom
            </button>
          </div>
        </div>
      </div>
    </div>
  );

  const BunnyCompanion = () => (
    <div className="bunny-section">
      <div className="bunny-container">
        <div className="bunny-avatar">
          <div className="bunny-character">🐰</div>
          <div className="bunny-crown">👑</div>
        </div>
        <div className="bunny-info">
          <h3>Lailan's Helper</h3>
          <div className="bunny-stats">
            <p>💎 Gems: {bunnyStats.total_gems || 0}</p>
            <p>⭐ Level: {bunnyStats.level || 1}</p>
            <p>🏆 Interactions: {bunnyStats.total_interactions || 0}</p>
          </div>
        </div>
      </div>
      
      <div className="bunny-actions">
        <button className="bunny-button" onClick={() => interactWithBunny('joke')}>
          😄 Tell me a joke!
        </button>
        <button className="bunny-button" onClick={() => interactWithBunny('fact')}>
          🧠 Share a fact!
        </button>
        <button className="bunny-button" onClick={() => interactWithBunny('trick')}>
          🎩 Show me a trick!
        </button>
        <button className="bunny-button" onClick={() => interactWithBunny('wisdom')}>
          💫 Give me wisdom!
        </button>
      </div>
    </div>
  );

  return (
    <div className="App">
      <div className="royal-background">
        <div className="sparkles"></div>
        <div className="sparkles sparkles-2"></div>
        <div className="sparkles sparkles-3"></div>
      </div>
      
      <nav className="royal-nav">
        <h1 className="app-title">🏰 Prince Lailan Royal Attendant</h1>
        <div className="nav-buttons">
          <button 
            className={`nav-button ${currentView === 'dashboard' ? 'active' : ''}`}
            onClick={() => setCurrentView('dashboard')}
          >
            🏰 Royal Ballroom
          </button>
          <button 
            className={`nav-button ${currentView === 'scheduler' ? 'active' : ''}`}
            onClick={() => setCurrentView('scheduler')}
          >
            📜 Royal Decree
          </button>
        </div>
      </nav>
      
      <main className="main-content">
        {currentView === 'dashboard' && <Dashboard />}
        {currentView === 'scheduler' && <MeetingScheduler />}
      </main>
      
      <BunnyCompanion />
      
      {notification && (
        <div className="notification">
          {notification}
        </div>
      )}
      
      <footer className="royal-footer">
        <p>✨ A Joseph Onyango Creation - Where meetings become magical ✨</p>
      </footer>
    </div>
  );
};

export default App;