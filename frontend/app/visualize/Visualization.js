'use client'

import { useRef, useLayoutEffect } from 'react';
import Script from 'next/script'

export default function VisualElem({ markup }) {
  const elRef = useRef();

  useLayoutEffect(() => {
    // Create a range/slice of the document. 
    const range = document.createRange();

    // Set the context to our containing node. 
    range.selectNode(elRef.current);

    // Create a new fragment within that range. 
    const documentFragment = range.createContextualFragment(markup);

    // Inject the markup, triggering a re-run! 
    elRef.current.innerHTML = '';
    elRef.current.append(documentFragment);
  }, []);

  return (
    <>
      <Script
        src="https://cdnjs.cloudflare.com/ajax/libs/require.js/2.3.4/require.min.js"
        strategy="lazyOnload"
      />
      <Script
        src="https://cdn.jsdelivr.net/npm/@jupyter-widgets/html-manager@^1.0.1/dist/embed-amd.js"
        strategy="lazyOnload"
      />
      <Script
        src="nglview-js-widgets.js"
        strategy="lazyOnload"
      />
      {/* elems = document.getElementsByClassName('jupyter-button');
        elem = document.getElementsByClassName('widget-readout')[0];
        elem.innerHTML -> frame number
        elems[1].onclick() -> plays
        elems[2].onclick() -> stops
        elems[3].onclick() -> repeats */}
      <div
        ref={elRef}
        dangerouslySetInnerHTML={{ __html: markup }}>
      </div>
    </>
  );
}