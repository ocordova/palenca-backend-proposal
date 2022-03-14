# Countries

```shell
# Setting of the country of the User
curl --location --request POST 'https://api.palenca.com/uber/create-user' \
--header 'x-api-key: your_api_key' \
--header 'Content-Type: application/json' \
--data-raw '{
   "country": "mx",
   "user_id": "user_id_from_your_db",
   "email": "jayroplascencia@gmail.com",
   "password": "mygreatpassword"
}'
```

When performing POST requests, you have to set the country code of the User in the post body.

Here is the list of available countries with their respective codes and the platforms supported in them:

Country | Code | Platforms |
------- | ---- | --------- |
Argentina|ar|Beat, Cabify, Didi, PedidosYa, Rapiboy, Rappi, Uber
Brazil|br|iFood, Uber, Noventa Nove
Bolivia|bo|PedidosYa, Uber
Chile|cl|Beat, Cabify, Cornershop, Didi, inDriver, PedidosYa, Rappi, Uber, Uber Eats
Costa Rica|cr|PedidosYa, Uber
Colombia|co|Cabify, Didi, Didi Food, iFood, inDriver, Mensajeros Urbanos, PedidosYa, Rappi, Uber
Ecuador|ec|Cabify, PedidosYa, Rappi, Uber, Uber Eats
México|mx|99minutos, Beat, Cabify, Cornershop, Didi, Didi Food, inDriver, Lalamove, Mensajeros Urbanos, Rappi, Uber, Uber Eats
Panamá|pa|PedidosYa, Uber, Uber Eats
Perú|pe|99minutos, Cabify, Cornershop, Didi, inDriver, PedidosYa, Rappi, Uber
Venezuela|ve|PedidosYa
