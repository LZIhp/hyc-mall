# 华耀城商城 · 前端（Vue3 + TS + Vite monorepo）

## 目录结构

```
apps/
  user/        用户端（C 端商城）
  merchant/    商家端（后台）
  admin/       管理端（后台）
packages/
  ui/          共享 UI 组件库
  request/     统一 Axios 请求封装
```

## 开发命令

```bash
npm install            # 安装所有依赖
npm run dev:user       # 启动用户端（5173）
npm run dev:merchant   # 启动商家端（5174）
npm run dev:admin      # 启动管理端（5175）
npm run build          # 构建全部
```
