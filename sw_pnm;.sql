DROP TABLE sw_pnm;

CREATE TABLE sw_pnm (
id serial PRIMARY KEY,
UTCDateTime TIMESTAMP,
region VARCHAR(30),
"coal(GW)" INTEGER,
"wind(GW)" INTEGER,
"solar(GW)" INTEGER,
"hydro(GW)" INTEGER,
"gas(GW)" INTEGER,
"total_consumption(GW)" INTEGER,
"breakdown estimated?" BOOLEAN,
"Carbon_Intensity(gCO2eq/kWh)" INTEGER,
"intensity estimated?" BOOLEAN
);


