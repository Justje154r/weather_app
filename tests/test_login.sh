echo "Spuštění testu přihlášení..."

BASE_URL="http://127.0.0.1:5000"

USERNAME="testuser"
PASSWORD="password"

RESPONSE=$(curl -s -c cookies.txt -o /dev/null -w "%{http_code}" -X POST \
    -d "username=$USERNAME&password=$PASSWORD" \
    $BASE_URL/login)

echo "HTTP status kód: $RESPONSE"

if [ $RESPONSE -eq 200 ]; then
    echo "Přihlášení bylo úspěšné."
else
    echo "Přihlášení selhalo. HTTP status kód: $RESPONSE"
fi