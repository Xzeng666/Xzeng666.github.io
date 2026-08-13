# Xzeng666.github.io

个人项目展示站，使用原生 HTML、CSS 与 JavaScript 构建，可由 GitHub Pages 直接托管，无需构建步骤。

## 页面

- `/`：个人主页与重点项目入口。
- `/lanexamsystem/`：LanExamSystem 重点项目专页，面向高校、培训机构和企业使用者。

## 本地预览

```powershell
python -m http.server 4173
```

浏览器访问 `http://127.0.0.1:4173/`。

## 设计与资源

- 设计规则保存在 `design-system/lanexamsystem-project-page/MASTER.md`。
- 教师端与考生端产品图来自程序实际运行截图，并压缩为轻量 JPG；架构图根据当前代码和项目引用绘制为 SVG。
- 所有页面支持键盘焦点、移动端导航和 `prefers-reduced-motion`。
