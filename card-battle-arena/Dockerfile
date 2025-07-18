FROM node:20 AS builder

WORKDIR /app

COPY package*.json ./
RUN npm ci

COPY . .

# Stage 2
FROM node:21-alpine

WORKDIR /app

COPY --from=builder /app ./

EXPOSE 5173

CMD ["npm","run","dev"]