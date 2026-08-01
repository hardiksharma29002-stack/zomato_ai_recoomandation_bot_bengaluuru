import { useState, useEffect } from 'react'
import './App.css'

function App() {
  const [locations, setLocations] = useState([
    "Banashankari", "Indiranagar", "Koramangala", "BTM", "Jayanagar", "MG Road", "Whitefield", "HSR"
  ]);
  const [cuisines, setCuisines] = useState(["Any", "North Indian", "South Indian", "Chinese", "Italian", "Fast Food"]);
  const [budgetMeta, setBudgetMeta] = useState({ low_max: 500, medium_max: 1500 });
  const [formData, setFormData] = useState({
    location: 'Banashankari',
    budget: 'medium',
    cuisine: 'Any',
    min_rating: 4.0,
    num_results: 5
  });
  const [results, setResults] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  useEffect(() => {
    fetch('/api/v1/meta')
      .then(res => res.json())
      .then(data => {
        if (data.locations && data.locations.length > 0) {
          setLocations(data.locations);
          setFormData(prev => ({ ...prev, location: prev.location || data.locations[0] }));
        }
        if (data.cuisines && data.cuisines.length > 0) {
          setCuisines(data.cuisines);
          setFormData(prev => ({ ...prev, cuisine: prev.cuisine || data.cuisines[0] }));
        }
        if (data.budget) {
          setBudgetMeta(data.budget);
        }
      })
      .catch(err => console.error("Error fetching meta from API:", err));
  }, []);

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: name === 'min_rating' ? parseFloat(value) : name === 'num_results' ? parseInt(value, 10) : value
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    setResults(null);
    try {
      const response = await fetch('/api/v1/recommend', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData),
      });
      if (!response.ok) {
        throw new Error('Failed to get recommendations. Please try again.');
      }
      const data = await response.json();
      setResults(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="app-container">
      <header className="header">
        <h1>Zomato AI Recommendations</h1>
        <p>Find your next favorite spot with the power of AI</p>
      </header>
      
      <main className="main-content">
        <section className="form-section">
          <form className="preference-form glass-panel" onSubmit={handleSubmit}>
            <div className="form-group">
              <label htmlFor="location">Location</label>
              <select 
                id="location" 
                name="location" 
                value={formData.location} 
                onChange={handleInputChange}
                required
              >
                {locations.map(loc => (
                  <option key={loc} value={loc}>{loc}</option>
                ))}
              </select>
            </div>

            <div className="form-group">
              <label>Budget (Cost for Two)</label>
              <div className="budget-segmented-control">
                {[
                  { level: 'low', label: `Low (₹0-${budgetMeta.low_max})` },
                  { level: 'medium', label: `Medium (₹${budgetMeta.low_max}-${budgetMeta.medium_max})` },
                  { level: 'high', label: `High (₹${budgetMeta.medium_max}+)` }
                ].map(({ level, label }) => (
                  <label key={level} className={`budget-option ${formData.budget === level ? 'selected' : ''}`}>
                    <input 
                      type="radio" 
                      name="budget" 
                      value={level} 
                      checked={formData.budget === level} 
                      onChange={handleInputChange} 
                    />
                    {label}
                  </label>
                ))}
              </div>
            </div>

            <div className="form-group">
              <label htmlFor="cuisine">Preferred Cuisine</label>
              <select 
                id="cuisine" 
                name="cuisine" 
                value={formData.cuisine} 
                onChange={handleInputChange}
                required
              >
                {cuisines.map(c => (
                  <option key={c} value={c}>{c}</option>
                ))}
              </select>
            </div>
            <div className="form-group">
              <label htmlFor="min_rating">Minimum Rating: <span className="rating-value">{formData.min_rating.toFixed(1)}</span></label>
              <input 
                type="range" 
                id="min_rating" 
                name="min_rating" 
                min="0" 
                max="5" 
                step="0.1" 
                value={formData.min_rating} 
                onChange={handleInputChange}
              />
            </div>

            <div className="form-group">
              <label htmlFor="num_results">Number of Results: <span className="rating-value">{formData.num_results}</span></label>
              <input 
                type="range" 
                id="num_results" 
                name="num_results" 
                min="0" 
                max="20" 
                step="1" 
                value={formData.num_results} 
                onChange={handleInputChange}
              />
            </div>



            <button type="submit" className="submit-btn" disabled={loading}>
              {loading ? 'Consulting the AI Chef...' : 'Get Recommendations'}
            </button>
          </form>
        </section>

        <section className="results-section">
          {loading && (
            <div className="loading-state glass-panel">
              <div className="spinner"></div>
              <p>Finding the perfect spots for you...</p>
            </div>
          )}

          {error && (
            <div className="error-state glass-panel">
              <p>{error}</p>
            </div>
          )}

          {results && !loading && (
            <div className="recommendations-container">
              {results.summary && (
                <div className="summary-banner glass-panel">
                  <p>✨ {results.summary}</p>
                </div>
              )}
              
              {results.recommendations && results.recommendations.length > 0 ? (
                <div className="cards-grid">
                  {results.recommendations.map((rec, idx) => (
                    <div key={idx} className="restaurant-card glass-panel">
                      <div className="card-header">
                        <h2>{rec.restaurant_name}</h2>
                        <span className="rating-badge">⭐ {rec.rating.toFixed(1)}</span>
                      </div>
                      <div className="card-meta">
                        <span className="cuisine-tag">{rec.cuisine}</span>
                        <span className="cost-tag">🪙 ₹{rec.cost_for_two} for two</span>
                      </div>
                      <div className="card-explanation">
                        <p>"{rec.explanation}"</p>
                      </div>
                    </div>
                  ))}
                </div>
              ) : (
                <div className="empty-state glass-panel">
                  <h3>No exact matches found</h3>
                  <p>Try relaxing your filters, like lowering the minimum rating or increasing the budget.</p>
                </div>
              )}
            </div>
          )}
        </section>
      </main>
    </div>
  )
}

export default App
