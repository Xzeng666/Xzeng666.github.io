# Xzeng666.github.io

Clin（Xzeng）的个人技术主页与项目作品集。站点使用原生 HTML、CSS 和 JavaScript 构建，由 GitHub Pages 直接托管，无构建步骤、运行时框架或第三方分析脚本。

## 页面与目录

```text
/
├── index.html                 # 个人主页、精选项目、技能与联系入口
├── projects/index.html        # 全部项目与轻量分类筛选
├── projects/music-player/     # Resonance Music Case Study
├── projects/dialect-asr/      # 川渝智能导航方言 ASR Case Study
├── projects/carmaker-validation/ # CarMaker 验证工具链 Case Study
├── projects/racecar/          # ROS 2 Racecar Case Study
├── lanexamsystem/index.html   # LanExamSystem Case Study（保留旧 URL）
├── articles/index.html        # Technical Writing 入口
├── resume/index.html          # 简历占位页（noindex，待补充内容）
├── 404.html                   # GitHub Pages 404 页面
├── CONTENT_TODO.md            # 需要本人确认的内容清单
├── assets/
│   ├── css/site.css           # Design Tokens、布局、组件与响应式规则
│   ├── js/site.js             # 导航、渐进 reveal、项目筛选与年份
│   └── images/                # 真实截图、架构图与 favicon
├── design-system/             # 设计规则与页面设计记录
├── scripts/check_site.py      # 零依赖静态质量检查
├── sitemap.xml
├── robots.txt
└── .github/workflows/quality.yml
```

## 本地运行

在仓库根目录执行：

```powershell
python -m http.server 4173
```

浏览器访问 `http://127.0.0.1:4173/`。不要直接双击 HTML 验证 404、目录 URL 或绝对路径；本地 HTTP 服务更接近 GitHub Pages。

## 质量检查

```powershell
python scripts/check_site.py
```

检查内容包括：

- HTML 重复 ID、标题、描述、语言、主内容 landmark；
- 图片 `alt`、外部新窗口链接的 `rel`；
- 内部链接、锚点、CSS、JavaScript 与图片资源路径；
- indexable 页面 canonical；
- `sitemap.xml` 中页面是否存在；
- `robots.txt` 中 Sitemap 地址是否正确；
- 可复用样式是否仍被 inline style 绕过。

GitHub Actions 只运行同一份 Python 标准库脚本，不替换当前 GitHub Pages 部署方式。

## 添加项目

1. 在 `projects/index.html` 添加语义化 `article.project-card`，正文必须保留在 HTML 中。
2. 使用统一的 `.project-tag-list` 与 `.project-tag`，不要复制项目专属标签 CSS。
3. 为卡片设置 `data-project-categories`；允许值目前为 `ai`、`software`、`automotive`、`automation`。
4. 首页只保留最有代表性的项目；完整列表放在 `/projects/`。
5. 重点项目需要独立 Case Study 时，按 Overview、Context、Problem、Requirements、Architecture、Technical Decisions、Challenges、Solutions、Results、Screenshots、Repository、Lessons Learned 组织内容。
6. 新增公开页面后同步更新 `sitemap.xml`。

任何性能指标、用户数、奖项、准确率、项目状态或个人经历都必须有仓库资料或本人确认，不能为了卡片完整而猜测。

## 添加文章

正式文章尚未启用。增加文章时：

1. 在 `articles/` 下创建稳定、可读的目录名；
2. 使用独立的 `title`、description、canonical 和社交分享元数据；
3. 在 `articles/index.html` 增加标题、日期、分类、摘要和入口；
4. 更新 `sitemap.xml`，但不要加入草稿或隐藏页面。

## 图片规范

- 优先使用真实运行截图、真实结果或经核验的架构图；不生成假界面冒充产品。
- HTML 中写明 `width`、`height` 和有意义的 `alt`，避免 CLS。
- 非首屏图片使用 `loading="lazy"` 与 `decoding="async"`。
- 首屏 LCP 图片不 lazy-load；只在确有必要时使用 `fetchpriority="high"`。
- 优先 SVG、WebP 或 AVIF，但小尺寸 JPG 无需为格式而强制转换。
- 项目页的多图组件使用 `[data-carousel]`；每张图片使用独立 `figure`、准确 `alt` 和说明文字。
- 替换占位图时，修改对应项目页的 `img src`、`alt` 与 `figcaption`。同一轮换建议使用接近 16:9 的统一画幅。
- 轮换不自动播放；按钮、分页圆点和键盘左右方向键均可操作。无 JavaScript 时所有图片会按普通图集展示。

## SEO 修改位置

- 页面级标题、描述、canonical、Open Graph、Twitter Card：各页面 `<head>`。
- 主页结构化数据：`index.html` 的 ProfilePage / Person JSON-LD。
- LanExamSystem 结构化数据：`lanexamsystem/index.html`。
- 公开页面清单：`sitemap.xml`。
- 爬虫入口：`robots.txt`。
- 待补充的 OG 封面与个人内容：`CONTENT_TODO.md`。

## 设计与可访问性

- `assets/css/site.css` 保存所有页面共享的结构、组件与交互规则；`assets/css/themes.css` 只负责主页和项目的视觉身份，不复制轮播、导航或响应式逻辑。
- 主页采用深蓝绿的编辑式工程档案布局；项目页分别使用 LanExamSystem 蓝绿运维、Resonance Music 紫绿声场、方言 ASR 青色波形与琥珀审计、CarMaker 石墨灰与安全橙、Racecar 红青遥测主题。
- 新增项目卡片时同时设置 `data-project-theme`；新增项目详情页时在 `body` 上设置 `project-theme theme-*`，并在 `design-system/xzeng-portfolio/pages/` 记录页面覆盖规则。
- 交互目标至少 44×44 px，键盘焦点可见，移动导航同步 `aria-expanded`。
- reveal 默认可见，只有 JavaScript 成功启用后才应用动画；禁用 JavaScript 不会隐藏正文。
- `prefers-reduced-motion` 下禁用平滑滚动和视觉位移动画。
- 支持现代 Chrome、Edge、Firefox、Safari、Mobile Chrome 与 Mobile Safari；不支持 IE。

## 部署

仓库继续使用 GitHub Pages 的现有静态部署方式。合并到默认分支后由 Pages 发布，无需新增 Pages 构建工作流。发布前先本地运行质量检查和页面验收。
