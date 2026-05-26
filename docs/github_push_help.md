# 推送到 GitHub 失败怎么办？

若终端出现类似：

```text
Failed to connect to github.com port 443
Recv failure: Connection was reset
```

这是**网络连不上 GitHub**，一般**不是**账号密码错误（还没到输入密码那一步）。

## 推荐解决办法（任选其一）

### 1. 开代理 / VPN 后再 push

确保浏览器能打开 https://github.com ，再在项目目录执行：

```powershell
git push origin main
```

若使用本地代理（例如 `127.0.0.1:7890`）：

```powershell
git config --global http.proxy http://127.0.0.1:7890
git config --global https.proxy http://127.0.0.1:7890
git push origin main
```

用完后可取消代理：

```powershell
git config --global --unset http.proxy
git config --global --unset https.proxy
```

### 2. 用 GitHub Desktop

1. 安装 [GitHub Desktop](https://desktop.github.com/)
2. 登录同一账号 `luzhangmen`
3. 添加本地仓库 `police-pre-reception`
4. 点 **Push origin**（有时比命令行更稳）

### 3. 网页上传（小改动时）

1. 打开 https://github.com/luzhangmen/police-pre-reception  
2. 需要改的文件点 **Edit**（铅笔图标）粘贴内容  
3. 底部 **Commit changes**

适合只改一两个文件；大批量仍建议修好网络后用 `git push`。

### 4. 换 SSH（有时略好，不保证）

```powershell
git remote set-url origin git@github.com:luzhangmen/police-pre-reception.git
ssh -T git@github.com
git push origin main
```

需先在 GitHub 添加 SSH 公钥。

## 当前仓库状态说明

- 远程 `main` 已包含地图功能与 **GitHub Actions 版 Pages 工作流**（`configure-pages` + `deploy-pages`）。
- 若你本地曾改过 `gh-pages` 分支部署方案但未 push 成功，执行 `git reset --hard origin/main` 可与线上一致。

## 推送成功后：启用 Pages

见 [github_pages_demo.md](./github_pages_demo.md)：

1. **Settings → Pages → Source** 选 **GitHub Actions**  
2. 重新运行 **Deploy GitHub Pages Demo** 工作流  
