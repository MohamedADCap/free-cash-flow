#!/bin/bash

# Example deployment script for Flask web application on Azure App Service

# Install Azure CLI if not already installed
# curl -sL https://aka.ms/InstallAzureCLIDeb | sudo bash

# Authenticate with Azure
az login

# Set Azure subscription
az account set --subscription "Your Subscription ID"

# Deploy the web app to Azure App Service
az webapp up --name your-webapp-name --sku F1 --location your-location --os-type Linux --runtime "PYTHON|3.8"
