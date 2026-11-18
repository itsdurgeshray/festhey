// Root layout: fonts and the figma/anim class. Each page loads its own stylesheets (see scripts/port.py).
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
      </head>
      <body suppressHydrationWarning>
        {children}
      </body>
    </html>
  );
}
