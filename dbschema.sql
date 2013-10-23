BEGIN;
DROP TABLE "racerecordweb_lap";
DROP TABLE "racerecordweb_trialdriver";
DROP TABLE "racerecordweb_trial";
DROP TABLE "racerecordweb_car";
DROP TABLE "racerecordweb_event";
DROP TABLE "racerecordweb_driver";
CREATE TABLE "racerecordweb_driver" (
    "id" serial NOT NULL PRIMARY KEY,
    "first_name" varchar(50) NOT NULL,
    "last_name" varchar(50) NOT NULL
)
;
CREATE TABLE "racerecordweb_event" (
    "id" serial NOT NULL PRIMARY KEY,
    "name" varchar(20) NOT NULL
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
CREATE TABLE "racerecordweb_trial" (
    "id" serial NOT NULL PRIMARY KEY,
    "name" varchar(50) NOT NULL,
    "event_id" integer NOT NULL REFERENCES "racerecordweb_event" ("id") DEFERRABLE INITIALLY DEFERRED
)
;
CREATE TABLE "racerecordweb_trialdriver" (
    "id" serial NOT NULL PRIMARY KEY,
    "event_id" integer NOT NULL REFERENCES "racerecordweb_event" ("id") DEFERRABLE INITIALLY DEFERRED,
    "driver_id" integer NOT NULL REFERENCES "racerecordweb_driver" ("id") DEFERRABLE INITIALLY DEFERRED,
    "trial_id" integer NOT NULL REFERENCES "racerecordweb_trial" ("id") DEFERRABLE INITIALLY DEFERRED,
    "car_id" integer REFERENCES "racerecordweb_car" ("id") DEFERRABLE INITIALLY DEFERRED,
    "start_number" smallint NOT NULL
)
;
CREATE TABLE "racerecordweb_lap" (
    "id" serial NOT NULL PRIMARY KEY,
    "lap_nr" integer NOT NULL,
    "time" integer NOT NULL,
    "penalty" smallint,
    "penalty_value" bigint,
    "trial_id" integer NOT NULL REFERENCES "racerecordweb_trial" ("id") DEFERRABLE INITIALLY DEFERRED
)
;
CREATE INDEX "racerecordweb_car_driver_id" ON "racerecordweb_car" ("driver_id");
CREATE INDEX "racerecordweb_trial_event_id" ON "racerecordweb_trial" ("event_id");
CREATE INDEX "racerecordweb_trialdriver_event_id" ON "racerecordweb_trialdriver" ("event_id");
CREATE INDEX "racerecordweb_trialdriver_driver_id" ON "racerecordweb_trialdriver" ("driver_id");
CREATE INDEX "racerecordweb_trialdriver_trial_id" ON "racerecordweb_trialdriver" ("trial_id");
CREATE INDEX "racerecordweb_trialdriver_car_id" ON "racerecordweb_trialdriver" ("car_id");
CREATE INDEX "racerecordweb_lap_trial_id" ON "racerecordweb_lap" ("trial_id");
COMMIT;
