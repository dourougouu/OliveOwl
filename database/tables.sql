CREATE TABLE producer(
	id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
	first_name VARCHAR(150) NOT NULL,
	last_name VARCHAR(150) NOT NULL,
	fathers_name VARCHAR(150),
	phone_number VARCHAR(10) NOT NULL,
	home_number VARCHAR(10),
	address VARCHAR(255),
	afm VARCHAR(9) NOT NULL UNIQUE
		CHECK(afm ~ '^[0-9]{9}$'),
	ADT VARCHAR(20) UNIQUE,
	tk VARCHAR(5) NOT NULL,
	dhmos VARCHAR(255) NOT NULL,
	doy VARCHAR(255) NOT NULL,
	notes TEXT, 
	created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);


CREATE TABLE olive_ProductDeliv(
	id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
	producer_id BIGINT NOT NULL
				REFERENCES producer(id),
	delivery_date DATE NOT NULL,
	olive_weight_kg NUMERIC(10,2) NOT NULL
					CHECK (olive_weight_kg > 0),
	olive_variety VARCHAR(50) NOT NULL
					CHECK (olive_variety IN ('koroneiki',
											 'manaki',
								 			 'athinolia',
								  			'tsounati',
								  			'kalamwn',
								  			'konservolia')
							),
	notes TEXT,
	created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);


CREATE INDEX indx_deliveryprod_producer_date
		ON olive_ProductDeliv(producer_id, delivery_date);
