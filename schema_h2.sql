-- MySQL dump 10.13  Distrib 8.0.25, for Win64 (x86_64)
--
-- Host: localhost    Database: bytecrunchers
-- ------------------------------------------------------
-- Server version	8.0.25







--
-- Current Database: "bytecrunchers"
--

drop schema bytecrunchers cascade;
create schema bytecrunchers;

set schema "bytecrunchers";

--
-- Table structure for table "account_types"
--

DROP TABLE IF EXISTS "account_types";

CREATE TABLE "account_types" (
  "id" varchar(45) NOT NULL,
  "savings_interest" decimal(5,5) unsigned NOT NULL,
  "annual_fee" decimal(6,2) unsigned NOT NULL,
  "foodie_pts" decimal(4,4) unsigned NOT NULL,
  "cashback" decimal(4,4) unsigned NOT NULL,
  "late_fee" decimal(5,2) unsigned NOT NULL);

--
-- Dumping data for table "account_types"
--


--
-- Table structure for table "accounts"
--

DROP TABLE IF EXISTS "accounts";

CREATE TABLE "accounts" (
  "id" int unsigned NOT NULL ,
  "users_id" int unsigned NOT NULL,
  "account_type" varchar(45) NOT NULL,
  "balance" decimal(10,2) NOT NULL,
  "payment_due" decimal(10,2) NOT NULL,
  "due_date" date DEFAULT NULL,
  "credit_limit" int DEFAULT NULL,
  "debt_interest" decimal(5,5) unsigned NOT NULL,
  "active" tinyint NOT NULL,
  "approved" tinyint NOT NULL,
  "confirmed" tinyint NOT NULL);

--
-- Dumping data for table "accounts"
--


--
-- Table structure for table "appointments"
--

DROP TABLE IF EXISTS "appointments";

CREATE TABLE "appointments" (
  "users_id_ap" int unsigned NOT NULL,
  "branches_id" int unsigned NOT NULL,
  "start_time" datetime NOT NULL,
  "end_time" datetime NOT NULL);

--
-- Dumping data for table "appointments"
--


--
-- Table structure for table "branches"
--

DROP TABLE IF EXISTS "branches";

CREATE TABLE "branches" (
  "id" int unsigned NOT NULL ,
  "street_address" varchar(95) NOT NULL,
  "city" varchar(35) NOT NULL,
  "state" char(2) NOT NULL,
  "zip" varchar(5) NOT NULL
);

--
-- Dumping data for table "branches"
--


--
-- Table structure for table "card_transactions"
--

DROP TABLE IF EXISTS "card_transactions";

CREATE TABLE "card_transactions" (
  "id" int unsigned NOT NULL ,
  "card_num" decimal(16,0) unsigned NOT NULL,
  "merchant_account_id" int unsigned NOT NULL,
  "memo" varchar(55) NOT NULL,
  "transfer_value" decimal(10,2) NOT NULL,
  "pin" smallint unsigned DEFAULT NULL,
  "cvc1" smallint unsigned DEFAULT NULL,
  "cvc2" smallint unsigned DEFAULT NULL,
  "location" char(2) DEFAULT NULL,
  "time_stamp" datetime NOT NULL,
  "status" tinyint NOT NULL);

--
-- Dumping data for table "card_transactions"
--


--
-- Table structure for table "cards"
--

DROP TABLE IF EXISTS "cards";

CREATE TABLE "cards" (
  "accounts_id" int unsigned NOT NULL,
  "card_num" decimal(16,0) unsigned NOT NULL,
  "pin" smallint unsigned DEFAULT NULL,
  "cvc1" smallint unsigned DEFAULT NULL,
  "cvc2" smallint unsigned DEFAULT NULL,
  "exp_date" date NOT NULL);

--
-- Dumping data for table "cards"
--


--
-- Table structure for table "confirmation"
--

DROP TABLE IF EXISTS "confirmation";

CREATE TABLE "confirmation" (
  "id" int unsigned NOT NULL ,
  "confirmed_at" datetime DEFAULT NULL,
  "created_at" datetime NOT NULL,
  "expires_at" datetime NOT NULL,
  "token" binary(16) NOT NULL,
  "user" int unsigned DEFAULT NULL,
  "loan" int unsigned DEFAULT NULL,
  "account" int unsigned DEFAULT NULL);

--
-- Dumping data for table "confirmation"
--


--
-- Table structure for table "loan_payments"
--

DROP TABLE IF EXISTS "loan_payments";

CREATE TABLE "loan_payments" (
  "id" int unsigned NOT NULL ,
  "loan_id" int unsigned NOT NULL,
  "account_id" int unsigned NOT NULL,
  "amount" decimal(10,2) NOT NULL,
  "time_stamp" datetime NOT NULL,
  "status" tinyint NOT NULL);

--
-- Dumping data for table "loan_payments"
--


--
-- Table structure for table "loan_types"
--

DROP TABLE IF EXISTS "loan_types";

CREATE TABLE "loan_types" (
  "id" varchar(45) NOT NULL,
  "upper_range" decimal(8,4) unsigned NOT NULL,
  "lower_range" decimal(8,4) unsigned NOT NULL,
  "late_fee" decimal(6,2) unsigned NOT NULL,
  "term_min" smallint NOT NULL,
  "term_max" smallint NOT NULL,
  "is_secured" tinyint NOT NULL);

--
-- Dumping data for table "loan_types"
--


--
-- Table structure for table "loans"
--

DROP TABLE IF EXISTS "loans";

CREATE TABLE "loans" (
  "id" int unsigned NOT NULL ,
  "users_id" int unsigned NOT NULL,
  "balance" decimal(10,2) NOT NULL,
  "interest_rate" decimal(5,5) NOT NULL,
  "due_date" datetime NOT NULL,
  "payment_due" decimal(8,2) unsigned NOT NULL,
  "loan_type" varchar(45) NOT NULL,
  "monthly_payment" decimal(7,2) unsigned NOT NULL,
  "active" tinyint NOT NULL,
  "approved" tinyint NOT NULL,
  "confirmed" tinyint NOT NULL);

--
-- Dumping data for table "loans"
--


--
-- Table structure for table "transactions"
--

DROP TABLE IF EXISTS "transactions";

CREATE TABLE "transactions" (
  "id" int unsigned NOT NULL ,
  "origin_account" int unsigned NOT NULL,
  "destination_account" int unsigned NOT NULL,
  "memo" varchar(55) NOT NULL,
  "transfer_value" decimal(10,2) NOT NULL,
  "time_stamp" datetime NOT NULL,
  "status" tinyint NOT NULL);

--
-- Dumping data for table "transactions"
--


--
-- Table structure for table "users"
--

DROP TABLE IF EXISTS "users";

CREATE TABLE "users" (
  "id" int unsigned NOT NULL ,
  "username" varchar(16) NOT NULL,
  "email" varchar(50) NOT NULL,
  "password" char(60) NOT NULL,
  "first_name" varchar(50) NOT NULL,
  "last_name" varchar(50) NOT NULL,
  "is_admin" tinyint NOT NULL,
  "ssn" decimal(9,0) DEFAULT NULL,
  "active" tinyint DEFAULT NULL,
  "confirmed" tinyint DEFAULT NULL,
  "phone" decimal(10,0) DEFAULT NULL,
  "dob" date DEFAULT NULL,
  "street_address" varchar(95) DEFAULT NULL,
  "city" varchar(35) DEFAULT NULL,
  "state" char(2) DEFAULT NULL,
  "zip" varchar(5) DEFAULT NULL);

--
-- Dumping data for table "users"
--

DROP TABLE IF EXISTS "stocks";
CREATE TABLE "stocks" (
  "id" int unsigned NOT NULL,
  "ticker" varchar(6) NOT NULL,
  "name" varchar(256) NOT NULL,
  "price" decimal(13,6) NOT NULL,
  "market_cap" decimal(15,2) NULL,
  "volume" bigint NOT NULL,
  "high" decimal(13,6) NOT NULL,
  "low" decimal(13,6) NOT NULL,
  "timestamp" datetime NOT NULL,
  "status" tinyint NOT NULL)






-- Dump completed on 2021-10-02 22:06:10;



ALTER TABLE account_types ADD PRIMARY KEY ("id");
ALTER TABLE account_types ADD UNIQUE KEY "account_types_account_type_id_UNIQUE" ("id");
ALTER TABLE accounts MODIFY "id" int unsigned NOT NULL AUTO_INCREMENT;
ALTER TABLE accounts ADD PRIMARY KEY ("id");
ALTER TABLE accounts ADD UNIQUE KEY "accounts_accounts_id_UNIQUE" ("id");
ALTER TABLE accounts ADD FOREIGN KEY ("account_type") REFERENCES "account_types" ("id") ON DELETE CASCADE ON UPDATE CASCADE;
ALTER TABLE accounts ADD FOREIGN KEY ("users_id") REFERENCES "users" ("id") ON DELETE CASCADE ON UPDATE CASCADE;
ALTER TABLE appointments ADD FOREIGN KEY ("branches_id") REFERENCES "branches" ("id") ON DELETE CASCADE ON UPDATE CASCADE;
ALTER TABLE appointments ADD FOREIGN KEY ("users_id_ap") REFERENCES "users" ("id") ON DELETE CASCADE ON UPDATE CASCADE;
ALTER TABLE branches MODIFY "id" int unsigned NOT NULL AUTO_INCREMENT;
ALTER TABLE branches ADD PRIMARY KEY ("id");
ALTER TABLE branches ADD UNIQUE KEY "branches_branches_id_UNIQUE" ("id");
ALTER TABLE branches ADD UNIQUE KEY "branches_location_UNIQUE" ("street_address");
ALTER TABLE card_transactions MODIFY "id" int unsigned NOT NULL AUTO_INCREMENT;
ALTER TABLE card_transactions ADD PRIMARY KEY ("id");
ALTER TABLE card_transactions ADD UNIQUE KEY "card_transactions_card_transactions_id_UNIQUE" ("id");
ALTER TABLE cards ADD PRIMARY KEY ("card_num");
ALTER TABLE cards ADD UNIQUE KEY "cards_cards_accounts_id_UNIQUE" ("accounts_id");
ALTER TABLE cards ADD FOREIGN KEY ("accounts_id") REFERENCES "accounts" ("id") ON DELETE CASCADE ON UPDATE CASCADE;
ALTER TABLE confirmation MODIFY "id" int unsigned NOT NULL AUTO_INCREMENT;
ALTER TABLE confirmation ADD PRIMARY KEY ("id");
ALTER TABLE confirmation ADD UNIQUE KEY "confirmation_id_UNIQUE" ("id");
ALTER TABLE confirmation ADD UNIQUE KEY "confirmation_token_UNIQUE" ("token");
ALTER TABLE confirmation ADD FOREIGN KEY ("account") REFERENCES "accounts" ("id");
ALTER TABLE confirmation ADD FOREIGN KEY ("loan") REFERENCES "loans" ("id");
ALTER TABLE confirmation ADD FOREIGN KEY ("user") REFERENCES "users" ("id");
ALTER TABLE loan_payments MODIFY "id" int unsigned NOT NULL AUTO_INCREMENT;
ALTER TABLE loan_payments ADD PRIMARY KEY ("id");
ALTER TABLE loan_payments ADD UNIQUE KEY "loan_payments_loan_pay_ID_UNIQUE" ("id");
ALTER TABLE loan_types ADD PRIMARY KEY ("id");
ALTER TABLE loan_types ADD UNIQUE KEY "loan_types_loan_type_id_UNIQUE" ("id");
ALTER TABLE loans MODIFY "id" int unsigned NOT NULL AUTO_INCREMENT;
ALTER TABLE loans ADD PRIMARY KEY ("id");
ALTER TABLE loans ADD UNIQUE KEY "loans_loans_id_UNIQUE" ("id");
ALTER TABLE loans ADD FOREIGN KEY ("loan_type") REFERENCES "loan_types" ("id");
ALTER TABLE loans ADD FOREIGN KEY ("users_id") REFERENCES "users" ("id") ON DELETE CASCADE ON UPDATE CASCADE;
ALTER TABLE transactions MODIFY "id" int unsigned NOT NULL AUTO_INCREMENT;
ALTER TABLE transactions ADD PRIMARY KEY ("id");
ALTER TABLE transactions ADD UNIQUE KEY "transactions_transactions_id_UNIQUE" ("id");
ALTER TABLE users MODIFY "id" int unsigned NOT NULL AUTO_INCREMENT;
ALTER TABLE users ADD PRIMARY KEY ("id");
ALTER TABLE users ADD UNIQUE KEY "users_username_UNIQUE" ("username");
ALTER TABLE users ADD UNIQUE KEY "users_users_id_UNIQUE" ("id");
ALTER TABLE users ADD UNIQUE KEY "users_email_UNIQUE" ("email");
ALTER TABLE stocks MODIFY "id" int unsigned NOT NULL AUTO_INCREMENT;
ALTER TABLE stocks ADD PRIMARY KEY ("id");
