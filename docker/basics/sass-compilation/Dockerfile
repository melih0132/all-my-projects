FROM node:19-alpine

LABEL maintainer="Melih Cetinkaya"
LABEL description="SASS compilation container with hot reloading"
LABEL version="1.0"

WORKDIR /app

# Copy package files
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy source code
COPY . .

# Expose port for live reload (if needed)
EXPOSE 35729

# Default command to compile SASS
CMD ["npm", "run", "sass-compile"]