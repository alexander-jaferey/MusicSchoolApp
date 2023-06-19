#!/bin/bash

dropdb musicschool-test
createdb musicschool-test
psql musicschool-test < ./.db-test.sql