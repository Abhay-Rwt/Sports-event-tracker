# Deployment Guide for Sports Event Tracker

This guide provides several options for deploying your Sports Event Tracker application to make it accessible on the internet.

## Option 1: Deploying on Heroku

Heroku is a simple platform-as-a-service (PaaS) that's great for Python Flask applications.

### Prerequisites
- A [Heroku account](https://signup.heroku.com/)
- [Heroku CLI](https://devcenter.heroku.com/articles/heroku-cli) installed
- Git installed

### Steps

1. **Create requirements.txt** (if not already present):
   ```
   pip freeze > requirements.txt
   ```

2. **Create a Procfile**:
   Create a file named `Procfile` (no extension) in your project root with:
   ```
   web: gunicorn app:app
   ```
   Make sure to install gunicorn:
   ```
   pip install gunicorn
   ```

3. **Create runtime.txt**:
   Create a file named `runtime.txt` in your project root with:
   ```
   python-3.11.9
   ```
   (Adjust version to match your Python version)

4. **Initialize Git repository** (if you haven't already):
   ```
   git init
   git add .
   git commit -m "Initial commit for deployment"
   ```

5. **Create and deploy to Heroku**:
   ```
   heroku create sports-event-tracker
   git push heroku main
   ```

6. **Set environment variables**:
   ```
   heroku config:set SPORTS_API_KEY=your_api_key
   heroku config:set FOOTBALL_API_KEY=your_api_key
   heroku config:set CRICKET_API_KEY=your_api_key
   heroku config:set OPENROUTER_API_KEY=your_openrouter_key
   ```

7. **Scale the app**:
   ```
   heroku ps:scale web=1
   ```

8. **Open the app**:
   ```
   heroku open
   ```

## Option 2: Deploying on PythonAnywhere

PythonAnywhere is a cloud-based Python development environment that's great for hosting Flask applications.

### Steps

1. **Sign up** for a [PythonAnywhere account](https://www.pythonanywhere.com/registration/register/beginner/)

2. **Upload your code**:
   - Go to the "Files" tab
   - Click "Upload a file" and upload your project as a ZIP file
   - Or use Git to clone your repository

3. **Create a virtual environment**:
   ```
   mkvirtualenv --python=/usr/bin/python3.9 sports-tracker-env
   pip install -r requirements.txt
   ```

4. **Configure a web app**:
   - Go to the "Web" tab
   - Click "Add a new web app"
   - Select "Flask" as your framework
   - Point it to your app.py file

5. **Set environment variables**:
   - In the "Web" tab, go to the "WSGI configuration file"
   - Add your environment variables at the top:
   ```python
   import os
   os.environ['SPORTS_API_KEY'] = 'your_api_key'
   os.environ['FOOTBALL_API_KEY'] = 'your_api_key'
   os.environ['CRICKET_API_KEY'] = 'your_api_key'
   os.environ['OPENROUTER_API_KEY'] = 'your_openrouter_key'
   ```

6. **Reload the web app**

## Option 3: Deploying on DigitalOcean

For more control and scalability, DigitalOcean is a great option.

### Steps

1. **Sign up** for a [DigitalOcean account](https://www.digitalocean.com/try/developer-brand)

2. **Create a Droplet** with Ubuntu

3. **SSH into your Droplet**:
   ```
   ssh root@your_droplet_ip
   ```

4. **Install dependencies**:
   ```
   apt update
   apt install python3-pip python3-dev build-essential libssl-dev libffi-dev python3-setuptools
   ```

5. **Set up a Python virtual environment**:
   ```
   apt install python3-venv
   mkdir -p /var/www/sports-tracker
   cd /var/www/sports-tracker
   python3 -m venv venv
   source venv/bin/activate
   ```

6. **Clone your repository and install requirements**:
   ```
   git clone https://your-repository-url.git .
   pip install -r requirements.txt
   pip install gunicorn
   ```

7. **Set up Nginx**:
   ```
   apt install nginx
   ```

8. **Create Nginx configuration**:
   Create `/etc/nginx/sites-available/sports-tracker` with:
   ```
   server {
       listen 80;
       server_name your_domain_or_ip;
       
       location / {
           include proxy_params;
           proxy_pass http://127.0.0.1:8000;
       }
   }
   ```

9. **Enable the site**:
   ```
   ln -s /etc/nginx/sites-available/sports-tracker /etc/nginx/sites-enabled
   ```

10. **Set up Systemd service**:
    Create `/etc/systemd/system/sports-tracker.service` with:
    ```
    [Unit]
    Description=Gunicorn instance to serve Sports Tracker
    After=network.target

    [Service]
    User=root
    Group=www-data
    WorkingDirectory=/var/www/sports-tracker
    Environment="PATH=/var/www/sports-tracker/venv/bin"
    Environment="SPORTS_API_KEY=your_api_key"
    Environment="FOOTBALL_API_KEY=your_api_key"
    Environment="CRICKET_API_KEY=your_api_key"
    Environment="OPENROUTER_API_KEY=your_openrouter_key"
    ExecStart=/var/www/sports-tracker/venv/bin/gunicorn --workers 3 --bind 127.0.0.1:8000 app:app

    [Install]
    WantedBy=multi-user.target
    ```

11. **Start and enable the service**:
    ```
    systemctl start sports-tracker
    systemctl enable sports-tracker
    systemctl restart nginx
    ```

## Option 4: Deploying on AWS Elastic Beanstalk

For a more managed approach with good scalability, AWS Elastic Beanstalk is a solid choice.

### Prerequisites
- [AWS account](https://aws.amazon.com/free/)
- [AWS CLI](https://aws.amazon.com/cli/) installed
- [EB CLI](https://docs.aws.amazon.com/elasticbeanstalk/latest/dg/eb-cli3-install.html) installed

### Steps

1. **Initialize Elastic Beanstalk**:
   ```
   eb init -p python-3.8 sports-tracker
   ```

2. **Create an `.ebignore` file**:
   Add files/directories you don't want to upload (e.g., venv, __pycache__, etc.)

3. **Create a `requirements.txt` file** (if not already present)

4. **Add environment configuration**:
   Create a `.ebextensions` directory in your project root
   Create a file `.ebextensions/environment.config`:
   ```yaml
   option_settings:
     aws:elasticbeanstalk:application:environment:
       SPORTS_API_KEY: your_api_key
       FOOTBALL_API_KEY: your_api_key
       CRICKET_API_KEY: your_api_key
       OPENROUTER_API_KEY: your_openrouter_key
   ```

5. **Create the environment and deploy**:
   ```
   eb create sports-tracker-env
   ```

6. **Open the app**:
   ```
   eb open
   ```

## Option 5: Docker Deployment

If you prefer containerization, Docker is a great option that can be deployed almost anywhere.

### Prerequisites
- [Docker](https://docs.docker.com/get-docker/) installed

### Steps

1. **Create a Dockerfile**:
   ```Dockerfile
   FROM python:3.9-slim

   WORKDIR /app

   COPY requirements.txt .
   RUN pip install --no-cache-dir -r requirements.txt

   COPY . .

   ENV SPORTS_API_KEY=your_api_key
   ENV FOOTBALL_API_KEY=your_api_key
   ENV CRICKET_API_KEY=your_api_key
   ENV OPENROUTER_API_KEY=your_openrouter_key

   EXPOSE 5000

   CMD ["python", "app.py"]
   ```

2. **Build the Docker image**:
   ```
   docker build -t sports-tracker .
   ```

3. **Run the container**:
   ```
   docker run -p 5000:5000 sports-tracker
   ```

4. **For deployment on services like Docker Hub**:
   ```
   docker tag sports-tracker yourusername/sports-tracker
   docker push yourusername/sports-tracker
   ```

## Important Security Considerations

1. **Never hardcode API keys** in your source code
2. **Use environment variables** for all sensitive information
3. **Enable HTTPS** for production deployments
4. **Implement proper authentication** if you plan to make this publicly accessible
5. **Consider rate limiting** to prevent abuse of your APIs
6. **Regularly update dependencies** to address security vulnerabilities

## Additional Resources

- [Flask Deployment Options](https://flask.palletsprojects.com/en/2.0.x/deploying/)
- [Heroku Python Deployment](https://devcenter.heroku.com/articles/getting-started-with-python)
- [PythonAnywhere Help Pages](https://help.pythonanywhere.com/pages/)
- [DigitalOcean Flask Deployment Tutorial](https://www.digitalocean.com/community/tutorials/how-to-serve-flask-applications-with-gunicorn-and-nginx-on-ubuntu-20-04)
- [AWS Elastic Beanstalk Python Guide](https://docs.aws.amazon.com/elasticbeanstalk/latest/dg/create-deploy-python-flask.html)
- [Docker Documentation](https://docs.docker.com/) 