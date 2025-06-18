const { chromium } = require('playwright');  // Or 'webkit' or 'firefox'.

(async () => {
  // 启动服务器
  const browserServer = await chromium.launchServer();
  const wsEndpoint = browserServer.wsEndpoint();
  console.log(wsEndpoint);

  // 通过 ws 连接服务器
  const browser = await chromium.connect(wsEndpoint);
  browser.newPage("https://playwright.dev/");

  // 等待 600 秒
  await new Promise(resolve => setTimeout(resolve, 600 * 1000));

  // 关闭服务器
  await browserServer.close();
})();
