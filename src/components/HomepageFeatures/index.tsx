import clsx from 'clsx';
import Heading from '@theme/Heading';
import styles from './styles.module.css';

type FeatureItem = {
  title: string;
  Svg: React.ComponentType<React.ComponentProps<'svg'>>;
  description: JSX.Element;
};

const FeatureList: FeatureItem[] = [
  {
    title: 'Quick Integration',
    Svg: require('@site/static/img/quick-start.svg').default,
    description: (
      <>
        Get started with Monolith in minutes. Our documentation guides you through
        implementing color-based barcode scanning step by step.
      </>
    ),
  },
  {
    title: 'Comprehensive API',
    Svg: require('@site/static/img/api-docs.svg').default,
    description: (
      <>
        Access detailed API documentation covering everything from basic scanning
        to advanced features like encryption and error correction.
      </>
    ),
  },
  {
    title: 'Industry Solutions',
    Svg: require('@site/static/img/solutions.svg').default,
    description: (
      <>
        Explore real-world implementations for healthcare, logistics, retail,
        and other industries with our detailed guides.
      </>
    ),
  },
];

function Feature({title, Svg, description}: FeatureItem) {
  return (
    <div className={clsx('col col--4')}>
      <div className="text--center">
        <Svg className={styles.featureSvg} role="img" />
      </div>
      <div className="text--center padding-horiz--md">
        <Heading as="h3">{title}</Heading>
        <p>{description}</p>
      </div>
    </div>
  );
}

export default function HomepageFeatures(): JSX.Element {
  return (
    <section className={styles.features}>
      <div className="container">
        <div className="row">
          {FeatureList.map((props, idx) => (
            <Feature key={idx} {...props} />
          ))}
        </div>
      </div>
    </section>
  );
}
