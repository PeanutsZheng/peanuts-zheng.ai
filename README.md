# PeanutsZheng.ai

一个基于 Vue 3 + TypeScript 的 AI 聊天和图像生成应用。

## 项目简介

提供了与 AI 模型交互的界面，主要功能包括：
- 与 AI 模型进行对话聊天
- 使用 Stable Diffusion 模型生成图像
- 支持明暗两种主题模式切换
- 响应式设计和流畅的动画效果

## 技术栈

- Vue 3 (Composition API + `<script setup>`)
- TypeScript
- Vue Router
- Axios
- CSS Modules + Catppuccin 主题

## 功能特性

### 1. 主题系统
- 支持 Latte（浅色）和 Frappe（深色）两种主题
- 动态加载 CSS 样式文件
- 平滑的主题切换动画

### 2. 自定义组件
#### CtrlPanel 控制面板
动态渲染的控制面板组件，用于控制各参数，支持多种控件类型：
- 文本输入框
- 数字输入框
- 滑块
- 下拉选择框
- 按钮
- 文本域

#### Popup 消息弹窗
美观的消息提示组件，支持自动关闭和手动关闭。

### 3. AI 交互
- 这是一个前端的项目，所以 AI 部分不多赘述。

## 项目结构

```
src/
├── assets/
│   └── css/
├── components/
├── hooks/
├── router/
├── store/           # 控制面板 widgets 配置
├── types/
└── views/
```

## 安装与运行

1. 克隆项目
```bash
git clone https://github.com/PeanutsZheng/peanuts-zheng.ai
```

2. 安装依赖
```bash
npm install
```

3. 启动开发服务器
```bash
npm run dev
```


## 自定义组件使用

### CtrlPanel 组件
```typescript
// 引入组件和相关 hooks
import CtrlPanel from '../components/CtrlPanel.vue'
import { useCtrlPanel } from '../hooks/useCtrlPanel'

// 在组件中使用
const { ctrlPanelRef, registerCtrlPanelEvent,
    getCtrlPanelValues, setCtrlPanelValue } = useCtrlPanel()

// 注册控件事件
registerCtrlPanelEvent('button', 'onClick', () => { consle.log('Hello world') )}

// 获取控件值
const values = getCtrlPanelValues()

// 设置控件值
setCtrlPanelValue('label', value)
```

### Popup 组件
```typescript
import Popup from '../components/Popup.vue'
import { usePopup } from '../hooks/usePopup'

const { popupRef, messagePopup } = usePopup()

// 显示消息
messagePopup('Hello world', 2000) // 2秒后自动关闭
```

## API 接口配置

与 AI 交互需要配合后端服务使用：
API 可在控制面板的API key中配置。

## 作者

PeanutsZheng

## 许可证

MIT License