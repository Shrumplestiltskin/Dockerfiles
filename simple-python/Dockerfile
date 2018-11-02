#Use alpine 3.8 with python3.7
FROM python:3.7-alpine3.8

#Set workdir directory
WORKDIR /app

#Set an env var, persists into container
ENV applesauce=taco

#Copy python app into container
COPY print-env.py ./ 

#Run python
CMD ["python", "./something.py" ]
