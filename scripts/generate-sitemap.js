const fs = require('fs');
const path = require('path');

const DOMAIN = 'https://www.okanaganconstruction.ca';
const PUBLIC_DIR = path.join(process.cwd(), 'public');
const ROOT_DIR = process.cwd();

const EXCLUDED_DIRS = new Set([
  'node_modules',
  '.git',
  'build',
  'dist',
  '.vercel',
  '.next',
  'out',
]);

function ensureDir(dir) {
  if (!fs.existsSync(dir)) {
    fs.mkdirSync(dir, { recursive: true });
  }
}

function formatDate(date) {
  return date.toISOString().split('T')[0];
}

function isExcluded(entry, fullPath) {
  const basename = entry.name;

  // Hidden files and directories
  if (basename.startsWith('.')) return true;

  // Files or directories beginning with _
  if (basename.startsWith('_')) return true;

  // Drafts
  if (basename.toLowerCase().includes('draft')) return true;

  // Excluded directories
  if (entry.isDirectory() && EXCLUDED_DIRS.has(basename)) return true;

  return false;
}

function findHtmlFiles(dir, files = []) {
  const entries = fs.readdirSync(dir, { withFileTypes: true });

  for (const entry of entries) {
    const fullPath = path.join(dir, entry.name);

    if (isExcluded(entry, fullPath)) continue;

    if (entry.isDirectory()) {
      findHtmlFiles(fullPath, files);
    } else if (entry.isFile() && entry.name.endsWith('.html')) {
      const relativePath = path.relative(ROOT_DIR, fullPath).replace(/\\/g, '/');
      files.push({
        filePath: fullPath,
        relativePath,
      });
    }
  }

  return files;
}

function getUrlFromFile(relativePath) {
  let urlPath = '/' + relativePath;

  // index.html at the root becomes /
  if (urlPath === '/index.html') return '/';

  return urlPath;
}

function getPriority(relativePath) {
  const urlPath = getUrlFromFile(relativePath);

  if (urlPath === '/') return '1.0';
  if (urlPath.startsWith('/projects/')) return '0.7';
  return '0.8';
}

function getChangefreq() {
  return 'monthly';
}

function escapeXml(str) {
  return str
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&apos;');
}

function generateSitemap() {
  const htmlFiles = findHtmlFiles(ROOT_DIR);

  // Sort URLs for consistent output: root first, then main pages, then projects
  htmlFiles.sort((a, b) => {
    const urlA = getUrlFromFile(a.relativePath);
    const urlB = getUrlFromFile(b.relativePath);
    return urlA.localeCompare(urlB);
  });

  let xml = '<?xml version="1.0" encoding="UTF-8"?>\n';
  xml += '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n';

  for (const { filePath, relativePath } of htmlFiles) {
    const stats = fs.statSync(filePath);
    const lastmod = formatDate(stats.mtime);
    const loc = DOMAIN + getUrlFromFile(relativePath);
    const priority = getPriority(relativePath);
    const changefreq = getChangefreq();

    xml += '  <url>\n';
    xml += `    <loc>${escapeXml(loc)}</loc>\n`;
    xml += `    <lastmod>${lastmod}</lastmod>\n`;
    xml += `    <changefreq>${changefreq}</changefreq>\n`;
    xml += `    <priority>${priority}</priority>\n`;
    xml += '  </url>\n';
  }

  xml += '</urlset>\n';

  return xml;
}

function generateRobots() {
  return `User-agent: *
Allow: /

Sitemap: ${DOMAIN}/sitemap.xml
`;
}

function main() {
  ensureDir(PUBLIC_DIR);

  const sitemap = generateSitemap();
  const sitemapPath = path.join(PUBLIC_DIR, 'sitemap.xml');
  fs.writeFileSync(sitemapPath, sitemap, 'utf8');

  const urlCount = (sitemap.match(/<url>/g) || []).length;
  console.log(`Generated ${path.relative(ROOT_DIR, sitemapPath)} with ${urlCount} URLs`);

  const robots = generateRobots();
  const robotsPath = path.join(PUBLIC_DIR, 'robots.txt');
  fs.writeFileSync(robotsPath, robots, 'utf8');
  console.log(`Generated ${path.relative(ROOT_DIR, robotsPath)}`);
}

main();
