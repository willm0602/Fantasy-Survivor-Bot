docker compose down -v
git pull upstream main
docker compose build
docker compose up -d