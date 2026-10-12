@echo off
rem Windows 一键部署脚本
rem 1) 先在 https://github.com/new 创建一个名为「guofeng」的空仓库（Public）
rem 2) 然后在本目录双击运行此脚本

set REPO_USER=txzj666666
set REPO_NAME=guofeng
set BRANCH=main

cd /d "%~dp0"

rem git 用户身份（首次使用请改成你自己的名字/邮箱）
git config --global user.name >nul 2>&1 || git config --global user.name "Your Name"
git config --global user.email >nul 2>&1 || git config --global user.email "you@example.com"

if not exist ".git" (
  git init
  git checkout -b %BRANCH%
  git add .
  git commit -m "init: 国风名将养成规划系统"
)

git remote get-url origin >nul 2>&1 || git remote add origin "https://github.com/%REPO_USER%/%REPO_NAME%.git"

git push -u origin %BRANCH%

echo.
echo ========================================================
echo 已推送到 GitHub！
echo 接下来打开：https://github.com/%REPO_USER%/%REPO_NAME%/settings/pages
echo   1) Source 选 Deploy from a branch
echo   2) Branch 选 main / root
echo   3) 等 30 秒发布完后访问：
echo      https://%REPO_USER%.github.io/%REPO_NAME%/
echo ========================================================
pause
