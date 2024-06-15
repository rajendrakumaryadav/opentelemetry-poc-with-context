### OpenTelemetry POC with Context
1. How to clone it?
By running the below command in Linux/Windows/Mac Terminal can clone the project.
```bash
git clone https://github.com/rajendrakumaryadav/opentelemetry-poc-with-context.git
```
2. How can run it?
To the run the application stack in docker is quite simple. I have already added the docker-compose.yml file and dockerfile(s) which have all the required things.
```bash
docker compose up
```
or in detached mode
```bash
docker compose up -d
```
3. How to test it?
Once both the above steps completed. You can simply open any browser and type `http://localhost:5000` to access the response in the docker.
To see the traces open `http://localhost:16686/search`, you can find the UI of jaeger with all the traces. Below is the response of jaeger traces tracking frontend.
![Jaeger UI Frontend](https://github.com/rajendrakumaryadav/opentelemetry-poc-with-context/assets/13816347/ca0e6426-a817-48a2-a036-f1ec0ef42861)
