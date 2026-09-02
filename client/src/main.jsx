import React from 'react';
import ReactDOM from 'react-dom/client';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import './styles.css';
import LearningCompanionStudio from './pages/LearningCompanionStudio';

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <BrowserRouter>
      <Routes>
        <Route path="*" element={<LearningCompanionStudio />} />
      </Routes>
    </BrowserRouter>
  </React.StrictMode>
);
