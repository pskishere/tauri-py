# Tauri Python Integration Project

这是一个集成了 Python 支持的 Tauri + React 项目。它使用了 `tauri-plugin-python` 插件，能够在桌面端（使用 PyO3/CPython）和移动端（使用 RustPython）运行 Python 逻辑。

## 项目初始化过程

以下是本项目从零开始的构建过程，供参考：

### 1. 创建基础 Tauri 项目
使用官方脚手架创建 React + TypeScript 项目：
```bash
npm create tauri-app@latest .
# 选择：
# - Project name: tauri-py
# - Frontend language: TypeScript / JavaScript
# - Package manager: npm
# - UI template: React
# - UI flavor: TypeScript
```

### 2. 集成 Python 插件
本项目使用了 `tauri-plugin-python` 来实现 Rust 与 Python 的互操作。

#### 安装前端 API
```bash
npm install tauri-plugin-python-api
```

#### 配置 Rust 后端依赖 (Cargo.toml)
为了支持移动端和桌面端的不同 Python 引擎（桌面端用 PyO3，移动端用 RustPython），在 `src-tauri/Cargo.toml` 中进行了特殊配置：

```toml
[target.'cfg(any(target_os = "android", target_os = "ios"))'.dependencies]
tauri-plugin-python = { version = "0.3.7", default-features = false, features = ["rustpython"] }

[target.'cfg(not(any(target_os = "android", target_os = "ios")))'.dependencies]
tauri-plugin-python = { version = "0.3.7", default-features = false, features = ["pyo3"] }
```

### 3. 配置权限与资源
1. **权限设置**：在 `src-tauri/capabilities/default.json` 中添加 `"python:default"`，允许前端调用 Python 插件。
2. **资源打包**：在 `src-tauri/tauri.conf.json` 的 `bundle -> resources` 中添加 `"src-python/*"`，确保 Python 脚本被打包进安装包。

### 4. 初始化 iOS 支持
```bash
npx tauri ios init
```

## 核心特性

- **跨平台 Python 支持**：
  - **桌面端 (macOS/Windows/Linux)**：通过 PyO3 集成系统的 CPython 环境，支持丰富的第三方库。
  - **移动端 (iOS/Android)**：通过 RustPython 解释器运行，无需在移动端配置复杂的 CPython 交叉编译环境。
- **React 前端**：现代化的 UI 交互。
- **Rust 后端**：高性能的系统级交互。

## 前置要求

在运行项目之前，请确保已安装以下工具：

- [Node.js](https://nodejs.org/) (建议 v18+)
- [Rust](https://www.rust-lang.org/) (建议最新稳定版)
- **桌面端运行**：系统需安装 Python 3
- **iOS 运行**：
  - Xcode
  - CocoaPods: `sudo gem install cocoapods`
  - iOS 模拟器或真机

## 快速开始

### 1. 安装依赖

```bash
# 安装前端依赖
npm install

# 安装 iOS 平台支持 (如果需要运行 iOS)
npx tauri ios init
```

### 2. 开发模式运行

#### 桌面端 (Desktop)
```bash
npm run tauri dev
```

#### iOS 模拟器 (iOS Simulator)
```bash
# 启动 iOS 模拟器并运行
npm run tauri ios dev
```

### 3. 构建打包

#### 桌面端 (Desktop)
```bash
npm run tauri build
```

#### iOS 模拟器打包 (iOS Simulator Build)
```bash
# 针对模拟器架构进行构建
npm run tauri ios build -- --target aarch64-sim
```

## 项目结构

- `src/`: React 前端源码。
- `src-tauri/`: Rust 后端源码。
  - `src-python/`: Python 脚本存放目录（会自动打包进应用资源）。
  - `src/lib.rs`: Tauri 插件和命令初始化。
  - `Cargo.toml`: 跨平台 Python 依赖配置。

## Python 调用示例

前端通过 `tauri-plugin-python-api` 调用 Python 函数：

```typescript
import { callFunction } from "tauri-plugin-python-api";

const result = await callFunction("greet_python", ["World"]);
console.log(result); // 输出: Hello World from Python!
```

Python 函数定义在 `src-tauri/src-python/main.py` 中：

```python
def greet_python(name):
    return f"Hello {name} from Python!"
```

## 注意事项

1. **移动端限制**：移动端使用的是 RustPython，它是一个纯 Rust 实现的 Python 解释器。并非所有 CPython 的第三方库（特别是带有 C 扩展的库）都能在 RustPython 中运行。
2. **iOS 权限**：已在 `capabilities/default.json` 中配置了必要的插件权限。
