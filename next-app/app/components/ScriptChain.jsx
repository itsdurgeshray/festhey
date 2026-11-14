'use client';
// Loads a page's interaction scripts one after another, in order, after the page has hydrated.
// The design-system scripts (site.js, app.js, dash.js...) are plain DOM scripts, so order matters:
// GSAP and Lenis must exist before site.js runs.
import { useLayoutEffect } from 'react';

export default function ScriptChain({ srcs = [] }) {
  useLayoutEffect(() => {
    let cancelled = false;
    const added = [];
    (async () => {
      for (const src of srcs) {
        if (cancelled) return;
        await new Promise(resolve => {
          const s = document.createElement('script');
          added.push(s);
          if (typeof src === 'object') {
            // inline <script> block from the HTML page: runs immediately, in its original position
            s.textContent = src.code;
            document.body.appendChild(s);
            return resolve();
          }
          s.src = src;
          s.async = false;
          s.onload = s.onerror = resolve;
          document.body.appendChild(s);
        });
      }
    })();
    return () => { cancelled = true; added.forEach(s => s.remove()); };
  }, [srcs]);
  return null;
}
