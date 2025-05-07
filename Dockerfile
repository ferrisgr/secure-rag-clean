# Use the official Python image from Docker Hub
FROM python:3.10

#Set working directory in the container
WORKDIR /app

# Copy all local files to the container
COPY . .

# Install Python dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

#Expose Streamlit default port
EXPOSE 8501

#Run the Streamlit app on container startup
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address= 0.0.0.0"]

# Copy Streamlit config
RUN mkdir -p ~/.streamlit
COPY .streamlit/config.toml ~/.streamlit/config.toml