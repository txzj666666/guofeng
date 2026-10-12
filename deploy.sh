#!/usr/bin/env bash
# 一键初始化 + 推送到 GitHub Pages
# 用法：先在 https://github.com/new 创建一个名为「guofeng」的空仓库（Public）
#     然后在本目录命令行跑：bash deploy.sh
set -e
cd "$(dirname "$0")"

REPO_USER="${REPO_USER:-txzj666666}"
REPO_NAME="${REPO_NAME:-guofeng}"
BRANCH="${BRANCH:-main}"

# git 用户身份（首次使用时改成你自己的）
if [ -z "$(git config --global user.name)" ]; then
  git config --global user.name  "Your Name"
  git config --global user.email "you@example.com"
  echo ">>> 已设置默认 git 身份（如需修改请编辑 ~/.gitconfig）"
fi

# 1) 初始化 git
if [ ! -d .git ]; then
  git init
  git checkout -b "$BRANCH"
  git add .
  git commit -m "init: 国风名将养成规划系统"
  echo ">>> 已初始化并首次提交"
else
  echo ">>> 已存在 .git，跳过 init"
fi

# 2) 配置远程
REMOTE="https://github.com/${REPO_USER}/${REPO_NAME}.git"
if git remote get-url origin >/dev/null 2>&1; then
  echo ">>> 远程已存在：$(git remote get-url origin)"
else
  git remote add origin "$REMOTE"
  echo ">>> 已添加远程：$REMOTE"
fi

# 3) 推送
echo ">>> 推送到 origin/$BRANCH ..."
git push -u origin "$BRANCH"

cat <<EOF

========================================================
✅ 已推送到 GitHub！
👉 接下来 5 秒内打开：https://github.com/${REPO_USER}/${REPO_NAME}/settings/pages
   1) Source 选 "Deploy from a branch"
   2) Branch 选 main / root
   3) 等 30 秒~1 分钟发布完后访问：
      https://${REPO_USER}.github.io/${REPO_NAME}/
========================================================
EOF
