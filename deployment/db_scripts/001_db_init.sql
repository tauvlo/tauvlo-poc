CREATE TYPE transactionrecordtype AS ENUM ('OWNERSHIP', 'POSTING', 'BUY_TOKENS', 'SELL_TOKENS');

CREATE TABLE "user" (
	user_id VARCHAR NOT NULL,
	details JSON,
	PRIMARY KEY (user_id)
);

CREATE TABLE property (
	property_id VARCHAR NOT NULL,
	poster_id VARCHAR,
	details JSON,
	PRIMARY KEY (property_id),
	FOREIGN KEY(poster_id) REFERENCES "user" (user_id)
);

CREATE TABLE ownership (
	user_id VARCHAR NOT NULL,
	property_id VARCHAR NOT NULL,
	tokens_owned BIGINT NOT NULL,
	PRIMARY KEY (user_id, property_id),
	FOREIGN KEY(user_id) REFERENCES "user" (user_id),
	FOREIGN KEY(property_id) REFERENCES property (property_id)
);

CREATE TABLE transaction_record (
	transaction_id BIGSERIAL NOT NULL,
	user_id VARCHAR NOT NULL,
	transaction_type transactionrecordtype NOT NULL,
	property_id VARCHAR,
	details JSON,
	PRIMARY KEY (transaction_id),
	FOREIGN KEY(user_id) REFERENCES "user" (user_id),
	FOREIGN KEY(property_id) REFERENCES property (property_id)
);

CREATE TABLE unique_visit
(
    ip_address VARCHAR NOT NULL,
    page_name VARCHAR NOT NULL,
    view_counter BIGINT NOT NULL DEFAULT 1,
    first_visit TIMESTAMP WITH TIME ZONE NOT NULL,
    last_visit TIMESTAMP WITH TIME ZONE NOT NULL,
    PRIMARY KEY (ip_address, page_name)
);
