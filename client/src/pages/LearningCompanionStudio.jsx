import React, { useEffect, useRef } from 'react';

export default function LearningCompanionStudio() {
  const containerRef = useRef(null);

  useEffect(() => {
    // Fetch and render the standalone Learning Companion Studio HTML inside iframe or element
  }, []);

  return (
    <iframe 
      src="/Learning_Companion_Studio.html" 
      title="Learning Companion Studio" 
      className="w-full h-screen border-0 shadow-none m-0 p-0"
    />
  );
}
