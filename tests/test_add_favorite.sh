echo "Spuštění testu přidání oblíbeného města..."


BASE_URL="http://127.0.0.1:5000"

CITY="Paris"
COUNTRY="France"

RESPONSE=$(curl -s -b cookies.txt -o /dev/null -w "%{http_code}" -X POST \
    -d "city=$CITY&country=$COUNTRY" \
    $BASE_URL/favorites)

echo "HTTP status kód: $RESPONSE"

if [ $RESPONSE -eq 200 ]; then
    echo "Přidání oblíbeného města bylo úspěšné."
else
    echo "Přidání oblíbeného města selhalo. HTTP status kód: $RESPONSE"
fi