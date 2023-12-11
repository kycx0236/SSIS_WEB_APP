-- --------------------------------------------------------
-- Host:                         127.0.0.1
-- Server version:               8.0.30 - MySQL Community Server - GPL
-- Server OS:                    Win64
-- HeidiSQL Version:             12.1.0.6537
-- --------------------------------------------------------

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8 */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;


-- Dumping database structure for ssis_v1
DROP DATABASE IF EXISTS 'ssis_v1';
CREATE DATABASE IF NOT EXISTS 'ssis_v1' /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE 'ssis_v1';

-- Dumping structure for table 'students'
DROP TABLE IF EXISTS 'students';
CREATE TABLE IF NOT EXISTS `students` (
	`id_number` VARCHAR(255) NOT NULL COLLATE 'utf8mb4_0900_ai_ci',
	`first_name` VARCHAR(255) NULL DEFAULT NULL COLLATE 'utf8mb4_0900_ai_ci',
	`last_name` VARCHAR(255) NULL DEFAULT NULL COLLATE 'utf8mb4_0900_ai_ci',
	`course_code` VARCHAR(255) NOT NULL COLLATE 'utf8mb4_0900_ai_ci',
	`year_` INT(10) NULL DEFAULT NULL,
	`gender` VARCHAR(255) NULL DEFAULT NULL COLLATE 'utf8mb4_0900_ai_ci',
	`profile_pic` TEXT NULL DEFAULT NULL COLLATE 'utf8mb4_0900_ai_ci',
	PRIMARY KEY (`id_number`) USING BTREE,
	UNIQUE INDEX `id_number` (`id_number`) USING BTREE,
	INDEX `course_code_idx` (`course_code`) USING BTREE,
	CONSTRAINT `course_code` FOREIGN KEY (`course_code`) REFERENCES `courses` (`course_code`) ON UPDATE NO ACTION ON DELETE NO ACTION
)
COLLATE='utf8mb4_0900_ai_ci'
ENGINE=InnoDB
;

-- Data exporting was unselected.

-- Dumping structure for table 'courses'
DROP TABLE IF EXISTS 'courses';
CREATE TABLE IF NOT EXISTS 'courses'(
  'course_code' varchar(255) NOT NULL PRIMARY KEY,
  'course_name' varchar(255) DEFAULT NULL,
  'college_code' varchar(255) NOT NULL,
  FOREIGN KEY 'college_code' references 'college'('college_code') ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Data exporting was unselected.

-- Dumping structure for table 'college'
DROP TABLE IF EXISTS 'college';
CREATE TABLE IF NOT EXISTS 'college'(
  'college_code' varchar(255) NOT NULL PRIMARY KEY,
  'college_name' varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Data exporting was unselected.

/*!40103 SET TIME_ZONE=IFNULL(@OLD_TIME_ZONE, 'system') */;
/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IFNULL(@OLD_FOREIGN_KEY_CHECKS, 1) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40111 SET SQL_NOTES=IFNULL(@OLD_SQL_NOTES, 1) */;
