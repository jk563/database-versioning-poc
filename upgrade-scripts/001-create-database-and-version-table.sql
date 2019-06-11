CREATE DATABASE IF NOT EXISTS `db`;

USE `db`;

CREATE TABLE IF NOT EXISTS `db_versioning` (`version` INT);

TRUNCATE TABLE db_versioning;
INSERT INTO `db_versioning` (`version`) VALUES (1);
