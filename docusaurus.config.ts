import {themes as prismThemes} from 'prism-react-renderer';
import type {Config} from '@docusaurus/types';
import type * as Preset from '@docusaurus/preset-classic';
import type * as OpenApiPlugin from "docusaurus-plugin-openapi-docs";

// This runs in Node.js - Don't use client-side code here (browser APIs, JSX...)

const config: Config = {
  title: 'Monolith Documentation',
  tagline: 'The Next Generation of Barcode Technology',
  favicon: 'https://s3-wp.birbal.dev/monolith/uploads/2024/12/Monolith_Favicon.png',

  // Set the production url of your site here
  url: 'https://docs.monolith.skydom.ai',
  // Set the /<baseUrl>/ pathname under which your site is served
  // For GitHub pages deployment, it is often '/<projectName>/'
  baseUrl: '/',
  deploymentBranch: 'gh-pages',
  trailingSlash: false,

  // GitHub pages deployment config.
  // If you aren't using GitHub pages, you don't need these.
  organizationName: 'jbirbal-skydom', // Usually your GitHub org/user name.
  projectName: 'monolith-docs', // Usually your repo name.

  onBrokenLinks: 'throw',
  onBrokenMarkdownLinks: 'warn',

  // Even if you don't use internationalization, you can use this field to set
  // useful metadata like html lang. For example, if your site is Chinese, you
  // may want to replace "en" with "zh-Hans".
  i18n: {
    defaultLocale: 'en',
    locales: ['en'],
  },
  plugins: [

    [
      'docusaurus-plugin-openapi-docs',
      {
        id: 'api', // Unique identifier for the plugin instance
        docsPluginId: 'classic', // Links this plugin to the main docs plugin
        config: {
          monolithApi: { // Unique identifier for this API configuration
            specPath: 'openapi/openapi.yaml', // Path to your OpenAPI spec file
            outputDir: 'docs/api',   // Directory where the generated docs will go
            sidebarOptions: {
              groupPathsBy: 'tag', // Groups documentation by OpenAPI tags
              categoryLinkSource: "tag",     // Links category items to their tags
            },
          }satisfies OpenApiPlugin.Options,
        },
      },
    ],


  ],
  presets: [
    [
      'classic',
      {
        docs: {
          sidebarPath: './sidebars.ts',
          docItemComponent: '@theme/ApiItem', // Add this line
          // Please change this to your repo.
          // Remove this to remove the "edit this page" links.
          editUrl:
            'https://github.com/jbirbal-skydom/monolith-docs/tree/master/',
        },
        theme: {
          customCss: './src/css/custom.css',
        },
      } satisfies Preset.Options,
    ],
  ],
  stylesheets: [
    // ... other stylesheets
  ],
  themes: ['docusaurus-theme-openapi-docs', 
    '@docusaurus/theme-mermaid',
  ],
  themeConfig: {
    // Replace with your project's social card
    image: 'img/docusaurus-social-card.jpg',
    navbar: {
      title: 'Monolith',
      logo: {
        alt: 'Monolith Logo',
        src: 'img/logo.svg',
      },
      items: [
        {
          type: 'docSidebar',
          sidebarId: 'startedSidebar',
          position: 'left',
          label: 'Get Started',
        },
        {
          type: 'docSidebar',
          sidebarId: 'apiSidebar',
          position: 'left',
          label: 'API',
        },
        // {
        //   type: 'docSidebar',
        //   sidebarId: 'conceptSidebar',
        //   position: 'left',
        //   label: 'Concepts',
        // },
        {
          type: 'docSidebar',
          sidebarId: 'resourceSidebar',
          position: 'left',
          label: 'Resources',
        },
        {
          href: 'https://github.com/jbirbal-skydom/monolith-docs',
          label: 'GitHub',
          position: 'right',
        },
      ],
    },
    footer: {
      style: 'dark',
      links: [
        {
          title: 'Docs',
          items: [
            {
              label: 'Getting Started',
              to: '/docs/get_started',
            },
          ],
        },
        {
          title: 'Community',
          items: [
            {
              label: 'Discussions',
              href: 'https://github.com/jbirbal-skydom/monolith-docs/discussions',
            },
            // {
            //   label: 'Discord',
            //   href: 'https://discordapp.com/invite/docusaurus',
            // },
          ],
        },
        {
          title: 'More',
          items: [
            {
              label: 'Skydom',
              href: 'https://skydom.ai',
            },
            {
              label: 'GitHub',
              href: 'https://github.com/jbirbal-skydom/monolith-docs',
            },
          ],
        },
      ],
      copyright: `Copyright © ${new Date().getFullYear()} Monolith Project. Built with Docusaurus.`,
    },
    prism: {
      theme: {
        plain: {
          backgroundColor: '#2A1B1B', // Matches basic code block background
          color: '#F7D9D9', // Light pink for base text
        },
        styles: [
          {
            types: ['keyword'],
            style: { color: '#8B0909', fontStyle: 'italic' }, // Monolith red for keywords
          },
          {
            types: ['string', 'char'],
            style: { color: '#3CAD6E' }, // Monolith green for strings
          },
          {
            types: ['function'],
            style: { color: '#FFC857' }, // Yellow for functions
          },
          {
            types: ['comment'],
            style: { color: '#7A2020', fontStyle: 'italic' }, // Muted maroon for comments
          },
        ],
      },
      darkTheme: prismThemes.dracula,
      additionalLanguages: ['rust'],
    },
    mermaid: {
      theme: { light: 'default', dark: 'dark' }, // Mermaid diagram themes
    },
  } satisfies Preset.ThemeConfig,
};

export default config;
