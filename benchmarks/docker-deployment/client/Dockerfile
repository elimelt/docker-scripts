
FROM node:14
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .

EXPOSE 3001

COPY start-client.sh /app/start-client.sh
RUN chmod +x /app/start-client.sh

CMD ["/app/start-client.sh"]