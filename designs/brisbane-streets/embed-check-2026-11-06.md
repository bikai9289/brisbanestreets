# 官方游戏嵌入检查

检查日期：2026-11-06。目标：https://brisbane-streets.pages.dev/

结论：当前官方地址禁止跨站 iframe 嵌入；本站不能仅靠添加 iframe 实现站内游玩。未修改产品页面。

## 当前响应与浏览器证据

使用本机 Edge / Playwright 访问官方页面，返回 HTTP 200，读取到：

```text
X-Frame-Options: SAMEORIGIN
Content-Security-Policy: …; frame-ancestors 'self'
Permissions-Policy: …; microphone=(self)
```

随后用 `http://127.0.0.1:4312/embed-check` 的临时测试页面加载官方 iframe。测试页通过浏览器请求拦截生成，没有添加到网站文件或部署包。

浏览器实际报错：

```text
Framing 'https://brisbane-streets.pages.dev/' violates the following Content Security Policy directive: "frame-ancestors 'self'". The request has been blocked.
net::ERR_BLOCKED_BY_RESPONSE
```

子框架最终地址为 `chrome-error://chromewebdata/`，未进入游戏。这是嵌入被拦截的实测，不是从网页文本猜测。

## 官方说明

已阅读 https://brisbane-streets.pages.dev/terms （页面注明更新于 2026-10-30）：没有发现对第三方网站开放嵌入或游戏文件再分发的说明。此次网页检索也未找到可确认的官方 embed 地址。这不能单独证明法律禁止，但不能当成已经获得嵌入授权。

哥飞 fetch_url 成功返回官方源码，HTTP 200；本次扣 1 积分。此前累计 53，本任务累计查询支出变为 54 积分，余额显示 2166。

## 可行后续

需要开发者提供允许嵌入的专用地址，或在 CSP 中允许本站域名，并相应调整 X-Frame-Options。浏览器能力（全屏、指针锁定、麦克风、存档）还需对获准地址单独测试。本站添加 `allow` 或 `allowfullscreen` 不能覆盖官方的 frame-ancestors 限制。

当前保留打开官方游戏的链接。不使用剥离响应头的代理或未经确认的第三方镜像来冒充官方嵌入。
