// 引导式截图脚本 · 多帧 · 桌面 + 手机
const { chromium } = require('playwright');
const path = require('path');
const fs = require('fs');

const ROOT = __dirname;
const URL  = 'file:///' + path.join(ROOT, 'index.html').replace(/\\/g, '/');
const OUT  = path.join(ROOT, 'screenshots');
fs.mkdirSync(OUT, { recursive: true });

const EDGE = 'C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe';

(async () => {
  const browser = await chromium.launch({
    executablePath: EDGE,
    headless: true,
    args: ['--no-sandbox','--disable-gpu','--font-render-hinting=none','--enable-font-smoothing']
  });

  // 桌面端
  const ctx  = await browser.newContext({
    viewport: { width: 1440, height: 900 },
    deviceScaleFactor: 1,
    colorScheme: 'dark',
  });
  const page = await ctx.newPage();
  async function shot(name, full=false){
    const file = path.join(OUT, name + '.png');
    await page.screenshot({ path: file, fullPage: full });
    console.log('saved:', file);
  }
  async function move(pageId){
    await page.evaluate((id)=> { location.hash = '#'+id; }, pageId);
    await page.waitForTimeout(500);
  }

  await page.goto(URL, { waitUntil: 'load' });
  await page.waitForTimeout(900);

  // 01 · 首页（可视区）
  await move('cover');
  await shot('guide-01-cover');

  // 02 · 首页（全页滚动截图）
  await shot('full-01-cover', true);

  // 03 · 按 → 进入铸剑阁
  await page.keyboard.press('ArrowRight');
  await page.waitForTimeout(800);
  await shot('guide-02-forge-default');

  // 04 · 切换名将到张飞
  await page.evaluate(()=>{
    const cards = document.querySelectorAll('#general-picker .general-card');
    cards.forEach(c=>{ if(c.dataset.id==='zhangfei') c.click(); });
  });
  await page.waitForTimeout(500);
  await shot('guide-03-forge-hero-change');

  // 05 · 调高目标等级至 60 + 明细滚动到中心
  await page.evaluate(()=>{
    const t = document.getElementById('lvl-to');
    t.value = 60; t.dispatchEvent(new Event('input'));
  });
  await page.waitForTimeout(400);
  await page.evaluate(()=> document.querySelector('.calc-wrap').scrollIntoView({block:'center', behavior:'instant'}));
  await page.waitForTimeout(200);
  await shot('guide-04-forge-lvl60-detail');

  // 06 · 切换修炼路径 → 行伍历练
  await page.evaluate(()=> window.scrollTo({top:0, behavior:'instant'}));
  await page.evaluate(()=>{
    document.querySelectorAll('#path-picker .select-tile').forEach(b=>{
      if(b.textContent.indexOf('行伍历练')>=0) b.click();
    });
  });
  await page.waitForTimeout(500);
  await page.evaluate(()=> document.querySelector('.calc-wrap').scrollIntoView({block:'center', behavior:'instant'}));
  await page.waitForTimeout(200);
  await shot('guide-05-forge-path-change');

  // 07 · 全页
  await shot('full-02-forge', true);

  // 08 · 铸剑阁全页
  // 09 · 进入图鉴（按 →）
  await page.keyboard.press('ArrowRight');
  await page.waitForTimeout(800);
  await shot('guide-06-gallery-grid');

  // 10 · 筛选秦汉
  await page.evaluate(()=>{
    document.querySelectorAll('.filter-chip').forEach(b=>{ if(b.textContent.indexOf('秦汉')>=0) b.click(); });
  });
  await page.waitForTimeout(400);
  await shot('guide-07-gallery-filter');

  // 11 · 恢复全部 + 打开韩信详情
  await page.evaluate(()=>{
    document.querySelectorAll('.filter-chip').forEach(b=>{ if(b.textContent.indexOf('全部')>=0) b.click(); });
  });
  await page.waitForTimeout(400);
  await page.evaluate(()=>{
    const cards = document.querySelectorAll('.hero-card');
    cards.forEach(c=>{
      const nm = c.querySelector('.name');
      if(nm && nm.textContent.trim()==='韩信') c.click();
    });
  });
  await page.waitForTimeout(700);
  await page.evaluate(()=> document.getElementById('detail-card').scrollIntoView({behavior:'instant', block:'start'}));
  await page.waitForTimeout(400);
  await shot('guide-08-gallery-detail-hanxin');

  // 12 · 数字键 4 跳到终章
  await page.keyboard.press('4');
  await page.waitForTimeout(800);
  await shot('guide-09-epilogue');

  // 13 · 终章全页
  await shot('full-03-epilogue', true);

  // 14 · 从终章跳回首页（按 1）
  await page.keyboard.press('1');
  await page.waitForTimeout(800);
  await shot('guide-10-back-to-cover');

  // 15 · 从首页按数字键 3 跳到图鉴
  await page.keyboard.press('3');
  await page.waitForTimeout(800);
  await shot('guide-11-direct-to-gallery');

  // 16 · 移动端首页
  await ctx.close();
  const mctx = await browser.newContext({
    viewport: { width: 390, height: 844 },
    deviceScaleFactor: 2,
    isMobile: true,
    hasTouch: true,
    userAgent: 'Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1',
    colorScheme: 'dark',
  });
  const mp = await mctx.newPage();
  await mp.goto(URL, { waitUntil: 'load' });
  await mp.waitForTimeout(900);
  await mp.screenshot({ path: path.join(OUT, 'guide-12-mobile-cover.png'), fullPage: false });

  // 17 · 移动端第二页
  await mp.keyboard.press('ArrowRight');
  await mp.waitForTimeout(800);
  await mp.screenshot({ path: path.join(OUT, 'guide-13-mobile-forge.png'), fullPage: false });

  // 18 · 移动端图鉴
  await mp.keyboard.press('ArrowRight');
  await mp.waitForTimeout(800);
  await mp.screenshot({ path: path.join(OUT, 'guide-14-mobile-gallery.png'), fullPage: false });

  await browser.close();
  console.log('全部截图完成 ✓');
})().catch(err => {
  console.error('截图脚本异常:', err);
  process.exit(1);
});
