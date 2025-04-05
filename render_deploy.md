# Deploying Sports Event Tracker on Render (Free Tier)

Render.com offers a generous free tier for web services that's perfect for deploying your Sports Event Tracker project. This guide will walk you through the entire process.

## Prerequisites

1. A [Render account](https://render.com/signup) (you can sign up with GitHub)
2. Your Sports Event Tracker project on GitHub or GitLab

## Step 1: Prepare Your Project for Deployment

Before deploying, make sure your project has the following files:

### 1. Create a `requirements.txt` file

```
flask==2.0.3
flask-socketio==5.1.1
python-dotenv==0.19.2
requests==2.27.1
pytz==2021.3
gunicorn==20.1.0
eventlet==0.33.0
```

Add any other dependencies your project uses.

### 2. Create a `render.yaml` file in your project root

```yaml
services:
  - type: web
    name: sports-event-tracker
    env: python
    buildCommand: pip install -r requirements.txt
    startCommand: gunicorn --worker-class eventlet -w 1 app:app
    envVars:
      - key: SPORTS_API_KEY
        sync: false
      - key: FOOTBALL_API_KEY
        sync: false
      - key: CRICKET_API_KEY
        sync: false
      - key: OPENROUTER_API_KEY
        sync: false
      - key: API_PROVIDER
        value: balldontlie
```

### 3. Make sure your `app.py` listens on the port provided by Render

Modify your app to use the PORT environment variable:

```python
if __name__ == '__main__':
    # Get port from environment variable or default to 5000
    port = int(os.environ.get('PORT', 5000))
    # Use 0.0.0.0 to make the app publicly available
    app.run(host='0.0.0.0', port=port)
```

### 4. Push these changes to your GitHub/GitLab repository

## Step 2: Deploy on Render

1. **Log in to Render** and go to your dashboard

2. **Click "New +"** and select "Web Service"

3. **Connect your repository**:
   - Select GitHub or GitLab
   - Authorize Render to access your repositories
   - Find and select your Sports Event Tracker repository

4. **Configure your service**:
   - **Name**: sports-event-tracker (or your preferred name)
   - **Environment**: Python
   - **Region**: Choose the region closest to you
   - **Branch**: main (or your main branch)
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn --worker-class eventlet -w 1 app:app`
   - **Plan**: Free

5. **Set environment variables**:
   - Click on "Advanced" to expand options
   - Add the following environment variables:
     - `SPORTS_API_KEY`: Your Sports API key
     - `FOOTBALL_API_KEY`: Your Football API key
     - `CRICKET_API_KEY`: Your Cricket API key
     - `OPENROUTER_API_KEY`: Your OpenRouter API key
     - `API_PROVIDER`: balldontlie

6. **Click "Create Web Service"**

Render will now start building and deploying your application. This can take a few minutes for the initial build.

## Step 3: Verify Your Deployment

Once the deployment is complete:

1. **Click on the URL** provided by Render (it will look like `https://sports-event-tracker.onrender.com`)
2. Your Sports Event Tracker application should now be live!

## Important Notes About Render's Free Tier

- Free web services on Render **shut down after 15 minutes of inactivity**
- They **spin up again** when a new request comes in
- The **first request after inactivity may be slow** (10-30 seconds) as the service restarts
- Free tier includes **750 hours of runtime per month**
- **No credit card required** for the free tier

## Troubleshooting

If you encounter issues with your deployment:

1. **Check the logs**: 
   - Go to your web service on Render
   - Click on "Logs" to see error messages

2. **Common issues**:
   - **Service crashes**: Check if all required environment variables are set
   - **Dependencies missing**: Make sure all dependencies are in requirements.txt
   - **Socket.IO issues**: Make sure you're using eventlet with gunicorn as shown in the start command

3. **Make changes**:
   - Update your code on GitHub/GitLab
   - Render will automatically redeploy when you push changes

## Next Steps

Once your application is successfully deployed, you might want to:

1. **Add a custom domain** (requires upgrading to a paid plan)
2. **Set up a persistent database** if needed
3. **Implement proper authentication** if making your app public
4. **Monitor usage** to ensure you stay within free tier limits

That's it! You've successfully deployed your Sports Event Tracker on Render's free tier. 