import React from 'react'
import Hero from './components/Hero'
import Features from './components/Features'
import Installation from './components/Installation'
import InteractiveDemo from './components/InteractiveDemo'
import WhyBrainTrust from './components/WhyBrainTrust'
import Metrics from './components/Metrics'
import Footer from './components/Footer'
import './App.css'

function App() {
  return (
    <div className="app">
      <Hero />
      <Features />
      <Installation />
      <Metrics />
      <InteractiveDemo />
      <WhyBrainTrust />
      <Footer />
    </div>
  )
}

export default App
