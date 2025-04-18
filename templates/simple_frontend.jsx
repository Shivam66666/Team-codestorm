import { useState } from 'react'
import './simple_frontend.css'

function Form() {

    return (
      <>
<header>
  <div className="header-content">
    <h1>🔍 Market Research Bot</h1>
    <p>A lightweight, real-time market intelligence tool for product builders</p>
  </div>
</header>

<div className="container">
  {/* Search Section */}
  <div className="bento-grid">
    <div className="bento-card search-card">
      <h2>Search for Market Insights</h2>

      <form action="http://localhost:5000/analyze" method="POST">
        <div className="form-group">
          <label htmlFor="searchTerm">What product or topic would you like to research?</label>
          <input
            type="text"
            id="searchTerm"
            name="searchTerm"
            placeholder="Enter a product, technology, or topic..."
            required
          />
        </div>

        <div className="form-group">
          <label>Select platforms to analyze:</label>
          <div className="checkbox-group">
            <label className="platform-checkbox">
              <input type="checkbox" name="platforms" value="hackernews" />
              <span className="checkmark"><i className="fab fa-hacker-news"></i> Hacker News</span>
            </label>
            <label className="platform-checkbox">
              <input type="checkbox" name="platforms" value="quora" />
              <span className="checkmark"><i className="fab fa-quora"></i> Quora</span>
            </label>
          </div>
        </div>

        <button id="searchButton" type="submit">
          <i className="fas fa-search"></i> Analyze Sentiment
        </button>
      </form>
    </div>
  </div>
</div>

      </>
    )
}

export default Form