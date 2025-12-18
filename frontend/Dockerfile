FROM node:22-alpine

WORKDIR /app

# 1) Копируем только манифесты
COPY package.json package-lock.json* pnpm-lock.yaml* yarn.lock* ./

# 2) Устанавливаем зависимости внутри контейнера
# Если есть lock-файл — используем ci, иначе fallback на install
# silent - отключает лишние логи
RUN npm ci --silent || npm install --silent

# 3) Копируем остальной исходный код (node_modules игнорируются .dockerignore)
COPY . .

# 4) Сборка
RUN npm run build

# 5) По необходимости: команда на dev/prod
CMD ["npm","run","preview"]
