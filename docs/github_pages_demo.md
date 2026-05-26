# GitHub Pages 在线地图 Demo

可以把**地图交互演示**发布到 GitHub，队友打开链接即可查看，无需安装 Python 或配置 Kimi。

> **说明**：在线 Demo 为静态页面，使用预设示例坐标展示地图效果。完整「语音 → AI 推理 → 真实地理编码」仍需本地或云服务器运行 `backend`。

## 访问地址

推送并启用 Pages 后，演示页一般为：

```text
https://<你的GitHub用户名>.github.io/<仓库名>/demo.html
```

例如仓库 `zhangsan/police-pre-reception`：

```text
https://zhangsan.github.io/police-pre-reception/demo.html
```

主页 `index.html` 依赖后端 API；**推荐给访客的是 `demo.html`**。

## 一次性配置步骤

### 1. 推送代码到 GitHub

确保仓库包含：

- `frontend/public/demo.html`
- `.github/workflows/github-pages.yml`

### 2. 开启 GitHub Pages

1. 打开仓库 **Settings → Pages**
2. **Build and deployment → Source** 选择 **GitHub Actions**
3. 推送 `main`（或 `master`）分支，等待 Actions 工作流 **Deploy GitHub Pages Demo** 变绿

### 3.（推荐）配置高德 Key，使用国内底图

1. 登录 [高德开放平台](https://lbs.amap.com/)，创建应用，开通 **Web 端 JS API**
2. 在 Key 的域名白名单中添加：

   ```text
   https://<你的用户名>.github.io
   ```

3. 在 GitHub 仓库 **Settings → Secrets and variables → Actions** 新建：

   | Name | Value |
   |------|--------|
   | `AMAP_WEB_KEY` | 你的高德 JS API Key |

4. 重新运行 Actions 部署（或再 push 一次）

未配置 Secret 时，Demo 仍可使用 OpenStreetMap 备用底图 + 示例坐标，适合先给同学看交互流程。

### 4. 在 README 放上 Demo 链接

```markdown
## Live Demo（地图）

[在线地图演示](https://luzhangmen.github.io/police-pre-reception/demo.html)
```

若 fork 到其他账号，将 URL 中的用户名与仓库名替换即可。

## 本地预览 Demo

```powershell
cd frontend/public
# 可选：copy demo-env.example.js demo-env.js 并填入 AMAP Key
py -3.12 -m http.server 8080
```

浏览器打开：`http://127.0.0.1:8080/demo.html`

## 常见问题

| 问题 | 处理 |
|------|------|
| Pages 404 | 确认 Actions 已成功；URL 是否包含仓库名（Project Pages） |
| 高德地图空白 | 检查 `AMAP_WEB_KEY` Secret 与白名单域名 |
| `index.html` 提交失败 | 正常：Pages 上没有后端，请使用 `demo.html` |
| 想展示完整 AI | 需另部署后端（Render / 云主机等），并把前端 API 地址指向该服务 |

## 安全提示

- `AMAP_WEB_KEY` 会出现在部署后的 `demo-env.js` 中，这是 JS API 的常见用法，务必用**域名白名单**限制。
- 不要把 `.env` 或含 LLM Key 的文件提交到 GitHub。
