# Use an official Node.js runtime as a parent image
FROM node:14

# Set the working directory in the container to /app
WORKDIR /app

# Copy package.json and package-lock.json to the working directory
COPY package*.json ./

# Install the dependencies
RUN npm install

# Copy the current directory contents into the container at /app
COPY . .

# Make the necessary port(s) available to the world outside this container
# Adjust this based on your client's needs
EXPOSE 3001

COPY start-client.sh /app/start-client.sh
RUN chmod +x /app/start-client.sh

CMD ["/app/start-client.sh"]