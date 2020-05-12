FROM mcr.microsoft.com/dotnet/core/sdk:3.1 as builder

WORKDIR /app/WebServer

COPY ./WebServer/WebServer.sln ./
COPY ./WebServer/App/FaceIdentifier.csproj ./App/

RUN dotnet restore

WORKDIR /app

COPY ./protos/ ./protos/
COPY ./WebServer/ ./WebServer/

WORKDIR /app/WebServer

RUN dotnet publish -c Release -o out ./App --no-restore


# Final Image
FROM mcr.microsoft.com/dotnet/core/sdk:3.1

RUN set -x \
    && apt update \
    && apt install -y \
        libc6-dev \
        libgdiplus \
        libx11-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY ./data/ ./data/
COPY --from=builder /app/WebServer/out/ ./WebServer/out/
COPY --from=builder /app/WebServer/App/ ./WebServer/App/

WORKDIR /app/WebServer/out

CMD ["dotnet", "FaceIdentifier.dll", "--urls", "http://*:5000;http://*:5001"]
