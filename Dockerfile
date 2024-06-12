# Use an official Python runtime as a parent image
FROM python:3.11.7 

# Set the working directory in the container
WORKDIR /app

# Copy the profiles.yml from the host into the container
COPY ~/.dbt/profiles.yml /root/.dbt/profiles.yml

# Copy the entire current directory into the container at /app
COPY . /app

# Install any needed dependencies specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# # Install dbt
# RUN pip install dbt

# Run dbt models
RUN dbt run --profiles-dir /root/.dbt/

# Expose port 8050 to allow communication to/from server
EXPOSE 8050

# Run the Dash application when the container launches
CMD ["python", "scripts/app.py"]
