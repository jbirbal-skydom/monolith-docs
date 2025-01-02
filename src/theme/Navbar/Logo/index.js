import React from 'react';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
import LottieLogo from '@site/src/components/lottie/lottielogo';
import { useBaseUrlUtils } from '@docusaurus/useBaseUrl';
import Link from '@docusaurus/Link';

export default function LogoWrapper(props) {
  const {siteConfig} = useDocusaurusContext();
  const {withBaseUrl} = useBaseUrlUtils();

  return (
    <div
      className="navbar__brand"
      style={{
        display: props.mobileLogo || props.className?.includes('navbar-sidebar') ? 'none' : 'flex',
        alignItems: 'center',
      }}
    >
      <Link
        href="https://monolith.skydom.ai/"
        className="navbar__logo"
        style={{ display: 'flex' }}
      >
        <LottieLogo
          url="https://s3-wp.birbal.dev/skydom/lottie/monolithHex.json"
          width="32px"
          height="32px"
          loop={true}
          autoplay={true}
        />
      </Link>
      <Link
        to={withBaseUrl('/')}
        className="navbar__title text--truncate"
      >
        <b>{siteConfig.title}</b>
      </Link>
    </div>
  );
}