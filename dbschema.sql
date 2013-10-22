BEGIN;
DROP TABLE "racerecordweb_lap";
DROP TABLE "racerecordweb_trialresult";
DROP TABLE "racerecordweb_trial";
DROP TABLE "racerecordweb_car";
ALTER TABLE "racerecordweb_event_drivers" DROP CONSTRAINT "event_id_refs_id_8c5b9ac1";
DROP TABLE "racerecordweb_event";
DROP TABLE "racerecordweb_event_drivers";
DROP TABLE "racerecordweb_driver";
CREATE TABLE "racerecordweb_driver" (
    "id" serial NOT NULL PRIMARY KEY,
    "first_name" varchar(50) NOT NULL,
    "last_name" varchar(50) NOT NULL
)
;
CREATE TABLE "racerecordweb_event_drivers" (
    "id" serial NOT NULL PRIMARY KEY,
    "event_id" integer NOT NULL,
    "driver_id" integer NOT NULL REFERENCES "racerecordweb_driver" ("id") DEFERRABLE INITIALLY DEFERRED,
    UNIQUE ("event_id", "driver_id")
)
;
CREATE TABLE "racerecordweb_event" (
    "id" serial NOT NULL PRIMARY KEY,
    "city" varchar(20) NOT NULL
)
;
ALTER TABLE "racerecordweb_event_drivers" ADD CONSTRAINT "event_id_refs_id_8c5b9ac1" FOREIGN KEY ("event_id") REFERENCES "racerecordweb_event" ("id") DEFERRABLE INITIALLY DEFERRED;
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
CREATE TABLE "racerecordweb_trial" (
    "id" serial NOT NULL PRIMARY KEY,
    "name" varchar(50) NOT NULL,
    "event_id" integer NOT NULL REFERENCES "racerecordweb_event" ("id") DEFERRABLE INITIALLY DEFERRED
)
;
CREATE TABLE "racerecordweb_trialresult" (
    "id" serial NOT NULL PRIMARY KEY,
    "trial_id" integer NOT NULL REFERENCES "racerecordweb_trial" ("id") DEFERRABLE INITIALLY DEFERRED,
    "besttime" time,
    "startnumber" integer NOT NULL,
    "driver_id" integer REFERENCES "racerecordweb_driver" ("id") DEFERRABLE INITIALLY DEFERRED,
    "car_id" integer REFERENCES "racerecordweb_car" ("id") DEFERRABLE INITIALLY DEFERRED
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
CREATE INDEX "racerecordweb_trial_event_id" ON "racerecordweb_trial" ("event_id");
CREATE INDEX "racerecordweb_trialresult_trial_id" ON "racerecordweb_trialresult" ("trial_id");
CREATE INDEX "racerecordweb_trialresult_driver_id" ON "racerecordweb_trialresult" ("driver_id");
CREATE INDEX "racerecordweb_trialresult_car_id" ON "racerecordweb_trialresult" ("car_id");
CREATE INDEX "racerecordweb_lap_trial_result_id" ON "racerecordweb_lap" ("trial_result_id");
COMMIT;
