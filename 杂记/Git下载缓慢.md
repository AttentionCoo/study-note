# GitHub 访问加速与协议配置指南

在复杂的网络环境下，国内开发者在拉取或推送 GitHub 仓库时，经常会遇到速度极慢（如数十 KiB/s）或连接中断（报错 `fetch-pack: unexpected disconnect`）的情况。本文将系统地梳理 Git 传输协议的底层逻辑，并给出针对性的加速解决方案。

## 一、 核心痛点：为什么配置了代理依然卡顿？

很多开发者在遇到网络卡顿时，会盲目使用如下命令：

Bash

```
git config --global http.proxy http://127.0.0.1:7897
```

**然而，该配置仅对 HTTPS 协议（形如 `[https://github.com/](https://github.com/)...`）生效。**

如果你的远程仓库使用的是 **SSH 协议**（形如 `git@github.com:...`），Git 会将传输任务全权移交给系统的 `ssh` 客户端处理。此时，Git 的 HTTP 代理配置会被完全无视，导致传输依然走直连，速度卡死。

因此，解决速度问题的首要前提是：**识别当前仓库的协议，并匹配对应的代理通道。**

## 二、 解决方案分类详解

通过 `git remote -v` 可以查看当前仓库使用的协议。请根据协议类型选择以下方案：

### 方案 A：针对 SSH 协议的终极加速（最推荐）

如果仓库地址是 `git@github.com:...`，我们需要直接打通系统的 SSH 全局代理。

#### 1. 配置步骤

1. 在 Git Bash 终端中运行以下命令以创建并打开 SSH 配置文件：

   Bash

   ```
   mkdir -p ~/.ssh && touch ~/.ssh/config && notepad ~/.ssh/config
   ```

2. 在打开的记事本中，根据你本地代理软件的端口（如 `7897`），贴入以下规则：

   **SOCKS5 协议配置（通常更稳定）：**

   Plaintext

   ```
   Host github.com
       User git
       ProxyCommand connect -S 127.0.0.1:7897 %h %p
   ```

   **HTTP 协议配置（备用）：**

   Plaintext

   ```
   Host github.com
       User git
       ProxyCommand connect -H 127.0.0.1:7897 %h %p
   ```

   > **注意**：如果后续操作报错提示 `connect command not found`，说明当前环境缺少 `connect` 工具，可将 `ProxyCommand` 行替换为：
   >
   > `ProxyCommand nc -X connect -x 127.0.0.1:7897 %h %p`

#### 2. 原理解析

这段配置告诉系统的 SSH 客户端：当识别到目的地是 `github.com` 时，不要进行直连，而是调用 `ProxyCommand`，将所有流量强行接引到本地的代理端口，借由代理软件的高速海外节点完成数据传输。

### 方案 B：针对 HTTPS 协议的代理配置

如果仓库地址是 `[https://github.com/](https://github.com/)...`，则可以直接通过修改 Git 全局配置来生效。

#### 1. 配置命令

Bash

```
# 1. 使用 HTTP 协议代理
git config --global http.proxy http://127.0.0.1:7897
git config --global https.proxy http://127.0.0.1:7897

# 2. 或者使用更稳定的 SOCKS5 协议（含远程 DNS 解析，防污染）
git config --global http.proxy socks5h://127.0.0.1:7897
git config --global https.proxy socks5h://127.0.0.1:7897
```

#### 2. 取消代理命令

如果后续不需要走代理，或者切换了网络环境，务必及时清除配置以免报错：

Bash

```
git config --global --unset http.proxy
git config --global --unset https.proxy
```

### 方案 C：无代理环境下的免翻墙替代方案（镜像加速）

在没有本地代理软件、或者大文件因超时频繁断开时，可以使用国内的 HTTPS 镜像站进行中转拉取（仅适用于公开仓库或只读操作）。

#### 1. 操作步骤

Bash

```
# 1. 将远程仓库地址临时或永久修改为带镜像前缀的地址
git remote set-url origin https://mirror.ghproxy.com/https://github.com/用户名/仓库名.git

# 2. 适当放大 Git 的全局缓存区（防止大文件引发意外断开）
git config --global http.postBuffer 524288000

# 3. 重新拉取
git pull
```

#### 2. 善后处理

由于镜像站通常只支持下载，若后续需要推送（`git push`）代码，建议在下载完成后将地址切换回官方的原生地址。

## 三、 避坑与排查检查单（Checklist）

- [ ] **核对端口**：确保代理软件处于开启状态，且命令中的端口（如 `7897`, `7890`）与软件设置中的 "LAN Port" 完全一致。
- [ ] **接管模式**：如果端口代理不生效，优先在代理软件中开启 **“系统代理” (System Proxy)** 或 **“TUN 模式”**。
- [ ] **协议对齐**：千万不要用 Git 的 `http.proxy` 去期待加速 `git@github.com` 的本地传输。