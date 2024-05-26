echo "Spuštění testu získání počasí..."

BASE_URL="http://127.0.0.1:5000"

CITY="London"

RESPONSE=$(curl -s -b cookies.txt -o /dev/null -w "%{http_code}" -X POST \
    -d "city=$CITY" \
    $BASE_URL/)

echo "HTTP status kód: $RESPONSE"

if [ $RESPONSE -eq 200 ]; then
    echo "Získání počasí bylo úspěšné."
else
    echo "Získání počasí selhalo. HTTP status kód: $RESPONSE"
fi