# 上线建议复核与修复

2026-11-06。当前线上旧版已实测可访问；本次修复在本地，尚未提交或推送。

## 线上确认

5个正式页、robots、sitemap均200；6个旧路径均301至正确目标并最终200；随机不存在路径404且noindex。原报告“技术层面全部通过”范围过大，但上述实际项目现在有浏览器证据。抓取响应耗时不能替代用户加载速度或CWV。

## 建议处理

| 建议 | 判断与处理 |
|---|---|
| 首页H1混入小字且连读 | 确认。H1改为纯文本Brisbane Streets Game，小字移至H1外；共享模板的br后补空白，避免其他标题textContent连读。 |
| unblocked目标词丢失 | 确认标题未承接该查询。恢复到Title/Description/H1和开篇，标题用问句；补网络限制、图形失败、应用内浏览器、镜像与存档保护说明，不保证解除限制。 |
| 每页VideoGame | 首页添加VideoGame，WebPage.about链接官方游戏实体，作者SohybQS在可见正文出现。关于、隐私等页不机械重复标成游戏，无虚构评分或截图。 |
| FAQPage是必需且能获得展示 | 不采用该结论。Google当前更新记录说明FAQ富结果自2026-05-07停止展示。保留可见FAQ；缺标记不是上线阻塞。 |
| 首页和帮助页必须1200词 | 无此Google硬性门槛。根据问题补有用信息，不以达到体检分或字数为目标。 |
| 删除/designs/ robots规则 | 已删除无实际部署对象的残留。设计资料仍通过干净dist排除，robots不是访问控制。 |
| 必建metro-code页，只说没有验证也可 | 暂不建。没有验证解法或所称空盘搜索证据，首页已有诚实说明；不能承诺仅占词就会拿曝光。 |
| site零结果等于未收录 | 不成立。需GSC URL Inspection确认，site结果不是完整索引清单。 |
| 两周零曝光说明一定是内容内链；30名后说明一定缺权重 | 不成立。先查索引状态、抓取、canonical及具体query/page数据，不能用单一阈值确定原因。 |
| 所有修改结束才可提交GSC | 不必当作硬门槛。现有有效页面可检查并提交；持续改进不必等待工具打分满分。 |

## 原始来源

- Google有用内容指南：https://developers.google.com/search/docs/fundamentals/creating-helpful-content ，明确不偏好固定词数。
- Google更新记录：https://developers.google.com/search/updates ，2026-05-08说明FAQ富结果停止展示。
- site限制：https://developers.google.com/search/docs/monitor-debug/search-operators/all-search-site
- Schema.org VideoGame：https://schema.org/VideoGame
- 官方游戏：https://brisbane-streets.pages.dev/ ，作者、免费和浏览器运行来自当前界面。

哥飞追加knowledge_ask 8积分，余额2130；未返回足够直接依据支撑1200词、两周零曝光归因、空Metro页必做等断言，未把弱相关材料当认可。

## 验证

新增检查先在旧版上复现首页H1断言失败，修复后20组视口及原交互检查通过；新断言覆盖纯H1、unblocked TDH、准确游戏实体关系和可见作者、无虚构评分。站内链接和片段、干净导出检查通过。线上仍为修复前版本，不混淆本地与线上结果。
