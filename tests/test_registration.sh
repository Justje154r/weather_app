echo "Spuštění testu registrace..."

BASE_URL="http://127.0.0.1:5000"

USERNAME="testuser"
EMAIL="testuser@example.com"
PASSWORD="password"
IS_PREMIUM="on"

RESPONSE=$(curl -s -o /dev/null -w "%{http_code}" -X POST \
    -d "username=$USERNAME&email=$EMAIL&password=$PASSWORD&is_premium=$IS_PREMIUM" \
    $BASE_URL/register)

echo "HTTP status kód: $RESPONSE"

if [ $RESPONSE -eq 200 ]; then
    echo "Registrace byla úspěšná."
else
    echo "Registrace selhala. HTTP status kód: $RESPONSE"
fi