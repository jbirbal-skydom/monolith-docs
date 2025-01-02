import React, { useEffect, useRef } from 'react';
import PropTypes from 'prop-types';
import ExecutionEnvironment from '@docusaurus/ExecutionEnvironment';

const LottieLogo = ({ url, width = '50px', height = '50px', loop = true, autoplay = true }) => {
  const containerId = useRef(`lottie-logo-${Math.random().toString(36).substr(2, 9)}`);
  const animationRef = useRef(null);

  useEffect(() => {
    if (!ExecutionEnvironment.canUseDOM) {
      return;
    }

    if (!url) {
      console.error('LottieLogo: Missing Lottie JSON URL');
      return;
    }

    // Dynamic import of lottie-web to ensure it only loads in browser
    import('lottie-web').then((lottie) => {
      animationRef.current = lottie.default.loadAnimation({
        container: document.getElementById(containerId.current),
        renderer: 'svg',
        loop: loop,
        autoplay: autoplay,
        path: url,
      });
    });

    return () => {
      if (animationRef.current) {
        animationRef.current.destroy(); // Cleanup animation on component unmount
      }
    };
  }, [url, loop, autoplay]);

  return <div id={containerId.current} style={{ width, height }}></div>;
};

LottieLogo.propTypes = {
  url: PropTypes.string.isRequired,
  width: PropTypes.string,
  height: PropTypes.string,
  loop: PropTypes.bool,
  autoplay: PropTypes.bool,
};

export default LottieLogo;