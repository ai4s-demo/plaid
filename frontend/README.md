# Smart Campaign Designer - 前端

AI 驱动的微孔板布局设计工具前端应用。

## 技术栈

- **React 18** - UI 框架
- **TypeScript** - 类型安全
- **Vite** - 构建工具
- **@dnd-kit** - 拖拽功能
- **jsPDF** - PDF 生成
- **Axios** - HTTP 客户端

## 快速开始

```bash
# 安装依赖
npm install

# 启动开发服务器
npm run dev

# 构建生产版本
npm run build
```

## 项目结构

```
frontend/
├── src/
│   ├── components/       # React 组件
│   │   ├── ChatPanel.tsx     # 对话面板
│   │   ├── FileUpload.tsx    # 文件上传
│   │   ├── PlateView.tsx     # 板布局可视化（SVG + 拖拽）
│   │   └── DownloadPanel.tsx # 下载面板
│   ├── hooks/
│   │   └── useChat.ts    # 聊天状态管理
│   ├── services/
│   │   └── api.ts        # API 调用 + SSE
│   ├── types/
│   │   └── index.ts      # TypeScript 类型定义
│   ├── App.tsx           # 主应用
│   ├── main.tsx          # 入口
│   └── index.css         # 样式
├── package.json
├── vite.config.ts
└── tsconfig.json
```

## 功能特性

### 🗣️ 对话交互
- 自然语言描述实验需求
- SSE 实时流式响应
- 上下文感知对话

### 📁 文件处理
- 拖拽上传 Excel/CSV
- 自动解析源板数据
- 实时预览

### 🧫 板布局可视化
- SVG 渲染 96/384 孔板
- 拖拽调整基因位置
- 颜色编码区分类型
- 约束违规高亮

### 📥 导出功能
- Picklist CSV（Echo 兼容）
- 布局 JSON
- PDF 报告

## 开发说明

### API 代理

开发模式下，Vite 会将 `/api` 请求代理到后端：

```typescript
// vite.config.ts
proxy: {
  '/api': {
    target: 'http://localhost:8000',
    changeOrigin: true,
  },
}
```

### 类型定义

所有数据类型定义在 `src/types/index.ts`，与后端 Pydantic 模型保持一致。

### 状态管理

使用 `useChat` hook 管理全局状态，包括：
- 源板数据
- 当前布局
- 设计参数
- 对话历史
- 加载/错误状态

## 部署

```bash
# 构建
npm run build

# 输出目录: dist/
# 可部署到任何静态文件服务器
```

生产环境需配置 Nginx 反向代理到后端 API。
