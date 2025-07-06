# ───── Stage 1: React build ────────────────────────────────────────────────
FROM node:20-alpine AS builder
WORKDIR /app

COPY package*.json ./
RUN npm ci        # reproducible install

COPY . .
RUN npm run build           # outputs to /app/build  (see webpack)

# ───── Stage 2: Nginx runtime ──────────────────────────────────────────────
FROM nginx:1.27-alpine
COPY nginx.conf /etc/nginx/conf.d/default.conf
COPY --from=builder /app/build /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
