# 1) STAGE DI BUILD: usa l'SDK completo per compilare
FROM mcr.microsoft.com/dotnet/sdk:8.0 AS build
WORKDIR /src

# Copia il file csproj e ripristina i pacchetti
COPY *.csproj .
RUN dotnet restore

# Copia il resto dei file e pubblica
COPY . .
RUN dotnet publish -c Release -o /app/publish

# 2) STAGE DI RUNTIME: immagine più leggera
FROM mcr.microsoft.com/dotnet/aspnet:8.0 AS final
WORKDIR /app

COPY --from=build /app/publish .

EXPOSE 8080

ENTRYPOINT ["dotnet", "llm-api.dll"]