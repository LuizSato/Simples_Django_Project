# Simple_Django_Project

curl -X POST -d "grant_type=password" \
-d "client_id={client_id}}" \
-d "client_secret={client_secret}" \
-d "username=admin" \
-d "password=password" \
"http://localhost:8000/o/token/"