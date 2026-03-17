FROM node:alpine
WORKDIR /usr/app/frontend
EXPOSE 5173
COPY ./ .
RUN npm install
CMD ["npm", "run", "dev"]