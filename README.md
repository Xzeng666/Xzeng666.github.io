# Xzeng666.github.io

个人技术主页与项目作品集，使用原生 HTML、CSS 和 JavaScript 构建，由 GitHub Pages 直接托管。

## 主要页面

- `/`：个人主页与精选项目。
- `/projects/`：全部项目与分类筛选。
- `/projects/carmaker-camera-recorder/`：CarMaker CameraRSI Recorder 项目介绍、真实采集结果与使用方式。
- `/lanexamsystem/`：LanExamSystem 项目介绍。
- `/articles/`：技术文章入口。

## 本地预览

```powershell
python -m http.server 4173
```

浏览器访问 `http://127.0.0.1:4173/`。

## 检查

```powershell
python scripts/check_site.py
```

检查内容包括页面元数据、内部链接、图片说明、静态资源路径、站点地图和可访问性基础项。

## 图片来源

CarMaker CameraRSI Recorder 页面使用项目实际录制结果；LanExamSystem 页面使用程序实际运行截图。图片仅用于说明对应项目的真实输出与界面。

## 部署

更新合并到 `main` 后由 GitHub Pages 自动发布，无需额外构建步骤。
