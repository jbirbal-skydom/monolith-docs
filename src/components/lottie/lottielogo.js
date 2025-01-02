import React, { useEffect, useRef } from 'react';
import PropTypes from 'prop-types';
import lottie from 'lottie-web';

const LottieLogo = ({ url, width = '50px', height = '50px', loop = true, autoplay = true }) => {
  const containerId = useRef(`lottie-logo-${Math.random().toString(36).substr(2, 9)}`);

  useEffect(() => {
    if (!url) {
      console.error('LottieLogo: Missing Lottie JSON URL');
      return;
    }

    const animation = lottie.loadAnimation({
      container: document.getElementById(containerId.current),
      renderer: 'svg',
      loop: loop,
      autoplay: autoplay,
      path: url,
    });

    return () => {
      animation.destroy(); // Cleanup animation on component unmount
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
