BEGIN;
DROP TABLE "racerecordweb_lap";
DROP TABLE "racerecordweb_trialresult";
DROP TABLE "racerecordweb_trial";
DROP TABLE "racerecordweb_location";
DROP TABLE "racerecordweb_car";
DROP TABLE "racerecordweb_driver";
CREATE TABLE "racerecordweb_driver" (
    "id" serial NOT NULL PRIMARY KEY,
    "first_name" varchar(50) NOT NULL,
    "last_name" varchar(50) NOT NULL
)
;
CREATE TABLE "racerecordweb_car" (
    "id" serial NOT NULL PRIMARY KEY,
    "name" varchar(20) NOT NULL,
    "capacity" varchar(10) NOT NULL,
    "power" integer NOT NULL,
    "year" integer NOT NULL,
    "plate" varchar(10) NOT NULL,
    "driver_id" integer NOT NULL REFERENCES "racerecordweb_driver" ("id") DEFERRABLE INITIALLY DEFERRED
)
;
CREATE TABLE "racerecordweb_location" (
    "id" serial NOT NULL PRIMARY KEY,
    "city" varchar(20) NOT NULL
)
;
CREATE TABLE "racerecordweb_trial" (
    "id" serial NOT NULL PRIMARY KEY,
    "name" varchar(50) NOT NULL,
    "location_id" integer NOT NULL REFERENCES "racerecordweb_location" ("id") DEFERRABLE INITIALLY DEFERRED
)
;
CREATE TABLE "racerecordweb_trialresult" (
    "id" serial NOT NULL PRIMARY KEY,
    "trial_id" integer NOT NULL REFERENCES "racerecordweb_trial" ("id") DEFERRABLE INITIALLY DEFERRED,
    "besttime" time,
    "startnumber" integer NOT NULL,
    "driver_id" integer NULL REFERENCES "racerecordweb_driver" ("id") DEFERRABLE INITIALLY DEFERRED,
    "car_id" integer NULL REFERENCES "racerecordweb_car" ("id") DEFERRABLE INITIALLY DEFERRED
)
;
CREATE TABLE "racerecordweb_lap" (
    "id" serial NOT NULL PRIMARY KEY,
    "lap_nr" integer NOT NULL,
    "time" time NOT NULL,
    "penalty" time NOT NULL,
    "penalty_value" varchar(10) NOT NULL,
    "trial_result_id" integer NOT NULL REFERENCES "racerecordweb_trialresult" ("id") DEFERRABLE INITIALLY DEFERRED
)
;
CREATE INDEX "racerecordweb_car_driver_id" ON "racerecordweb_car" ("driver_id");
CREATE INDEX "racerecordweb_trial_location_id" ON "racerecordweb_trial" ("location_id");
CREATE INDEX "racerecordweb_trialresult_trial_id" ON "racerecordweb_trialresult" ("trial_id");
CREATE INDEX "racerecordweb_trialresult_driver_id" ON "racerecordweb_trialresult" ("driver_id");
CREATE INDEX "racerecordweb_trialresult_car_id" ON "racerecordweb_trialresult" ("car_id");
CREATE INDEX "racerecordweb_lap_trial_result_id" ON "racerecordweb_lap" ("trial_result_id");
COMMIT;