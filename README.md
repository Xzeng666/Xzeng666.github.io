# Xzeng666.github.io

中英双语个人技术主页与项目作品集，使用原生 HTML、CSS 和 JavaScript 构建，由 GitHub Pages 直接托管。

首次访问会读取浏览器首选语言：中文设备进入中文页面，其他语言进入英文页面。导航中的 `English / 中文` 按钮可以随时切换，选择会保存在浏览器本地。中文页面使用原有 URL，英文页面位于 `/en/`，两套页面通过 `hreflang`、canonical 和站点地图互相声明。

## 主要页面

- `/`：个人主页与精选项目。
- `/en/`：英文个人主页与对应英文页面入口。
- `/projects/`：全部项目与分类筛选。
- `/projects/reqif-web-viewer/`：ReqIF Web Viewer 项目介绍、真实界面截图与在线使用入口。
- `/projects/carmaker-camera-recorder/`：CarMaker CameraRSI Recorder 1.5.0 项目介绍、真实采集结果、双语界面与硬件编码说明。
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

检查内容包括页面元数据、中英文对应页、`hreflang`、内部链接、图片说明、静态资源路径、站点地图和可访问性基础项。

## 图片来源

ReqIF Web Viewer 页面使用当前线上版本的七张实际界面截图，覆盖文档、搜索定位、工作项、字段设置、图片、表格和统计，内容为车辆状态监测示例需求。CarMaker CameraRSI Recorder 页面使用项目实际中英文 GUI 截图与录制结果；LanExamSystem 页面使用程序实际运行截图。图片仅用于说明对应项目的真实输出与界面。

## 部署

更新合并到 `main` 后由 GitHub Pages 自动发布，无需额外构建步骤。
