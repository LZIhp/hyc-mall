#!/bin/bash
# 华耀城商城 一键部署脚本（Ubuntu 22.04 / 20.04）
# 用法：bash deploy.sh
# 部署后访问：http://服务器IP:8000/

set -e

APP_DIR=/opt/hyc-mall
REPO_URL=https://github.com/LZIhp/hyc-mall.git

echo "=========================================="
echo "  华耀城商城 部署脚本"
echo "=========================================="

# 1. 安装系统依赖
echo "[1/7] 安装系统依赖..."
sudo apt-get update -y
sudo apt-get install -y python3 python3-pip python3-venv nginx git curl

# 2. 安装 Node.js 20（前端构建需要）
echo "[2/7] 检查/安装 Node.js..."
if ! command -v node &>/dev/null; then
  curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
  sudo apt-get install -y nodejs
fi

# 3. 获取代码（从 GitHub 克隆）
echo "[3/7] 获取代码..."
if [ -d "$APP_DIR/.git" ]; then
  cd "$APP_DIR" && git pull
else
  sudo mkdir -p "$APP_DIR"
  sudo chown -R "$USER":"$USER" "$APP_DIR"
  git clone "$REPO_URL" "$APP_DIR"
fi

# 4. 后端：虚拟环境 + 依赖 + 迁移 + 数据
echo "[4/7] 部署后端..."
cd "$APP_DIR/backend"
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python seed.py

# 5. 前端：构建（BASE_URL 留空，走同源相对路径 /api/）
echo "[5/7] 构建前端..."
cd "$APP_DIR/frontend"
npm install
VITE_API_BASE_URL='' npm run build --workspace apps/user -- --base=/

# 6. Nginx + gunicorn(systemd)
echo "[6/7] 配置 Nginx 和 gunicorn..."
sudo cp "$APP_DIR/deploy/nginx.conf" /etc/nginx/sites-available/hyc-mall
sudo ln -sf /etc/nginx/sites-available/hyc-mall /etc/nginx/sites-enabled/hyc-mall
sudo nginx -t && sudo systemctl reload nginx

sudo sed "s|__USER__|$USER|g; s|__APP_DIR__|$APP_DIR|g" "$APP_DIR/deploy/hyc-mall.service" > /etc/systemd/system/hyc-mall.service
sudo systemctl daemon-reload
sudo systemctl enable hyc-mall
sudo systemctl restart hyc-mall

# 7. 完成
IP=$(curl -s ifconfig.me)
echo ""
echo "=========================================="
echo "  部署完成！"
echo "  访问地址：http://$IP:8000/"
echo "=========================================="
