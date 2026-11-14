// Root layout: fonts, the FestHey design system (site.css), the figma/anim class and the global grain.
export const metadata = {
  title: 'FestHey | Discover College Fests & Events Across India',
  description: 'Experience the raw energy of Indian college festivals. Discover, register, and conquer the biggest stages across the country.',
  icons: { icon: '/assets/img/favicon.svg' },
};
export const viewport = { themeColor: '#FF5A14', width: 'device-width', initialScale: 1 };

const MODE = "(function(){var f=/[?&]figma/.test(location.search)||navigator.webdriver;document.documentElement.className=f?'figma':'anim';})();";

export default function RootLayout({ children }) {
  return (
    <html lang="en" suppressHydrationWarning>
      <head>
        <script dangerouslySetInnerHTML={{ __html: MODE }} />
        <link rel="preconnect" href="https://api.fontshare.com" crossOrigin="" />
        <link href="https://api.fontshare.com/v2/css?f[]=clash-display@500,600,700&f[]=satoshi@400,500,700,900&display=swap" rel="stylesheet" />
      </head>
      <body suppressHydrationWarning>
        {/* site.css first: page stylesheets use precedence="page", so they always load after the design system */}
        <link rel="stylesheet" href="/assets/site.css" precedence="base" />
        <div className="noise" aria-hidden="true" />
        {children}
      </body>
    </html>
  );
}
