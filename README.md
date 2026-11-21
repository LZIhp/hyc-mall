# 华耀城商城系统（重构版）

展示型电商商城 + AI 增值服务，三端（用户 / 商家 / 管理）。

## 技术栈

| 层 | 技术 |
|---|---|
| 前端 | Vue3 + TypeScript + Vite（npm workspaces monorepo） |
| 后端 | Python Django 5 + DRF + SimpleJWT + drf-spectacular |
| 数据库 | 开发 SQLite / 生产 MySQL 8 |

## 目录结构

```
hyc-mall/
├── frontend/                 # 前端 monorepo
│   ├── apps/
│   │   ├── user/             # 用户端（5173）
│   │   ├── merchant/         # 商家端（5174）
│   │   └── admin/            # 管理端（5175）
│   └── packages/
│       ├── ui/               # 共享 UI 组件库
│       └── request/          # 统一 Axios 请求封装
└── backend/                  # Django 后端
    ├── manage.py
    ├── config/               # 项目配置（settings/urls）
    └── apps/                 # 业务应用（阶段 4 填充）
```

## 快速开始

### 前端

```bash
cd frontend
npm install
npm run dev:user        # 用户端 http://localhost:5173
npm run dev:merchant    # 商家端 http://localhost:5174
npm run dev:admin       # 管理端 http://localhost:5175
```

### 后端

```bash
cd backend
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver   # http://localhost:8000
# Swagger 文档：http://localhost:8000/api/docs/
```

## 文档

项目需求/设计文档见上一级目录：`00-PRD文档.md`、`01-需求文档.md`、`02-数据库文档.md`、`03-接口设计文档.md`、`04-业务术语表.md`。
