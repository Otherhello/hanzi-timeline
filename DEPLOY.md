# GitHub Pages 部署完整步骤

本项目已经**自动接管**了构建与部署（`.github/workflows/deploy.yml`）。你只需要做「推送 + 开 Pages」两步。

## 已就绪的部分（无需改动）

| 文件 | 作用 |
|------|------|
| `vite.config.ts` | `base: './'` → 任何仓库名/子路径下静态资源都能正确加载 |
| `.github/workflows/deploy.yml` | push 到 `main` → 自动 `pnpm build` + 上传 `dist` + 部署 |
| `.gitignore` | 排除 `node_modules/`、`dist/` |
| `public/glyphs/*.svg` | 字形图（会被推送，不忽略） |

> 注：CI 用 `pnpm@9` + `node@20`，`build` 脚本为 `tsc -b && vite build`。
> 已修正 `src/App.tsx` 未使用变量导致的 `tsc` 报错，`tsc` 与 `vite build` 都已本地通过。

## 步骤 1 —— 在 GitHub 建仓库

1. 登录 GitHub → 右上角 **+** → **New repository**。
2. Repository name：`hanzi-timeline`（任意名均可，`base:'./'` 不挑仓库名）。
3. 设为 **Public**（若你是免费账号要开 GitHub Pages，公开仓库最省事）。
4. 不要勾选自动创建 README/初始化（保持空仓库即可）。
5. 点 **Create repository**。

## 步骤 2 —— 在项目本地初始化 git 并推送

在项目文件夹 `E:\DSH项目\hanzi-timeline\` 打开终端（Git Bash / PowerShell，需本机已装 git）：

```bash
cd "E:\DSH项目\hanzi-timeline"
git init
git add .
git commit -m "init: hanzi timeline"
git branch -M main
git remote add origin https://github.com/<你的用户名>/hanzi-timeline.git
git push -u origin main
```

> 把 `<你的用户名>` 换成你的实际 GitHub 用户名。
> 首次 push 会提示登录；用浏览器授权的 Git Credential Manager 或 Personal Access Token。

## 步骤 3 —— 开 GitHub Pages（选择 Actions 模式）

1. 进入仓库页 → **Settings** → 左侧 **Pages**。
2. **Source** 下拉框：选择 **GitHub Actions**（**不要**选 "Deploy from a branch"）。
3. 选好后无需其他配置。

## 步骤 4 —— 触发生成与验证

1. 回到仓库 → **Actions** 标签，应看到一个 `Deploy to GitHub Pages` 工作流开始运行（由刚才的 push 触发）。
2. 等它跑完（绿色 ✓）。构建、上传、部署三个 job 都成功即上线。
3. 访问站点：
   ```
   https://<你的用户名>.github.io/hanzi-timeline/
   ```
   站点内容 = `dist/`，即你本地看到的完整字形时间轴。

## 之后每改一次代码

保存 → `git add .` → `git commit -m "..."` → `git push`。
push 到 `main` 即自动重新构建并发布，无需手动操作。

---

## 常见问题排查

- **现象**：Pages 页面 404 或样式丢失。
  - 检查 **Settings → Pages → Source** 是否选了 **GitHub Actions**。
  - 确认 `Actions` 工作流是否成功，失败则点进日志看是 `tsc` 还是 `vite build` 报错。

- **现象**：本地 `pnpm build` / `pnpm dev` 报 `ERR_PNPM_IGNORED_BUILDS`。
  - 这是本地 pnpm 11 对 `esbuild` 安全策略所致，**不影响 GitHub CI**（CI 用的是 pnpm 9，默认执行构建脚本）。
  - 本地规避：`pnpm approve-builds` 允许 esbuild，或直接用 `node node_modules/vite/bin/vite.js build`。

- **现象**：站点打不开，提示 "The site has no source"。
  - 说明 Pages 还没部署成功，等 Actions 跑完或点 **Actions** 看失败原因。

- **甲方要求用别的分支**：改 `.github/workflows/deploy.yml` 里 `branches: [main]` 为你的分支名，并 push 到该分支。
