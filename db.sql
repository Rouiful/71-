-- --------------------------------------------------------
-- 主機:                           127.0.0.1
-- 伺服器版本:                        11.3.2-MariaDB - mariadb.org binary distribution
-- 伺服器作業系統:                      Win64
-- HeidiSQL 版本:                  12.6.0.6765
-- --------------------------------------------------------

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8 */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;


-- 傾印 114_system 的資料庫結構
CREATE DATABASE IF NOT EXISTS `114_system` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci */;
USE `114_system`;

-- 傾印  資料表 114_system.custom_ai_tests 結構
CREATE TABLE IF NOT EXISTS `custom_ai_tests` (
  `id` char(36) NOT NULL,
  `user_email` varchar(255) DEFAULT NULL,
  `topic` varchar(255) DEFAULT NULL,
  `difficulty` varchar(50) DEFAULT NULL,
  `points_cost` int(11) DEFAULT NULL,
  `status` varchar(50) DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT current_timestamp(),
  `title` varchar(255) DEFAULT NULL,
  `passage` text DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `user_email` (`user_email`),
  CONSTRAINT `custom_ai_tests_ibfk_1` FOREIGN KEY (`user_email`) REFERENCES `users` (`email`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- 取消選取資料匯出。

-- 傾印  資料表 114_system.custom_reading_questions 結構
CREATE TABLE IF NOT EXISTS `custom_reading_questions` (
  `id` char(36) NOT NULL,
  `ai_test_id` char(36) DEFAULT NULL,
  `question` text DEFAULT NULL,
  `option_a` varchar(255) DEFAULT NULL,
  `option_b` varchar(255) DEFAULT NULL,
  `option_c` varchar(255) DEFAULT NULL,
  `option_d` varchar(255) DEFAULT NULL,
  `correct_option` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `ai_test_id` (`ai_test_id`),
  CONSTRAINT `custom_reading_questions_ibfk_1` FOREIGN KEY (`ai_test_id`) REFERENCES `custom_ai_tests` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- 取消選取資料匯出。

-- 傾印  資料表 114_system.game_player 結構
CREATE TABLE IF NOT EXISTS `game_player` (
  `user_email` varchar(255) NOT NULL,
  `player_id` char(36) DEFAULT NULL,
  `session_id` char(36) DEFAULT NULL,
  `joined_at` timestamp NULL DEFAULT current_timestamp(),
  PRIMARY KEY (`user_email`),
  KEY `session_id` (`session_id`),
  CONSTRAINT `game_player_ibfk_1` FOREIGN KEY (`session_id`) REFERENCES `game_session` (`session_id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- 取消選取資料匯出。

-- 傾印  資料表 114_system.game_session 結構
CREATE TABLE IF NOT EXISTS `game_session` (
  `session_id` char(36) NOT NULL,
  `host_email` varchar(255) DEFAULT NULL,
  `game_type` varchar(255) DEFAULT NULL,
  `status` varchar(50) DEFAULT NULL,
  `is_private` tinyint(1) DEFAULT NULL,
  `password` varchar(255) DEFAULT NULL,
  `max_players` int(11) DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT current_timestamp(),
  `last_active_at` timestamp NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  PRIMARY KEY (`session_id`),
  KEY `host_email` (`host_email`),
  CONSTRAINT `game_session_ibfk_1` FOREIGN KEY (`host_email`) REFERENCES `users` (`email`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- 取消選取資料匯出。

-- 傾印  資料表 114_system.point_transactions 結構
CREATE TABLE IF NOT EXISTS `point_transactions` (
  `id` char(36) NOT NULL,
  `user_email` varchar(255) DEFAULT NULL,
  `change_amount` int(11) DEFAULT NULL,
  `reason` varchar(255) DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT current_timestamp(),
  PRIMARY KEY (`id`),
  KEY `user_email` (`user_email`),
  CONSTRAINT `point_transactions_ibfk_1` FOREIGN KEY (`user_email`) REFERENCES `users` (`email`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- 取消選取資料匯出。

-- 傾印  資料表 114_system.reading_questions 結構
CREATE TABLE IF NOT EXISTS `reading_questions` (
  `id` char(36) NOT NULL,
  `reading_test_id` char(36) DEFAULT NULL,
  `question` text DEFAULT NULL,
  `option_a` varchar(255) DEFAULT NULL,
  `option_b` varchar(255) DEFAULT NULL,
  `option_c` varchar(255) DEFAULT NULL,
  `option_d` varchar(255) DEFAULT NULL,
  `correct_option` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `reading_test_id` (`reading_test_id`),
  CONSTRAINT `reading_questions_ibfk_1` FOREIGN KEY (`reading_test_id`) REFERENCES `reading_tests` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- 取消選取資料匯出。

-- 傾印  資料表 114_system.reading_tests 結構
CREATE TABLE IF NOT EXISTS `reading_tests` (
  `id` char(36) NOT NULL,
  `title` varchar(255) DEFAULT NULL,
  `passage` text DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT current_timestamp(),
  `category` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- 取消選取資料匯出。

-- 傾印  資料表 114_system.test_results 結構
CREATE TABLE IF NOT EXISTS `test_results` (
  `id` char(36) NOT NULL,
  `user_email` varchar(255) DEFAULT NULL,
  `test_type_id` int(11) DEFAULT NULL,
  `score` int(11) DEFAULT NULL,
  `total_questions` int(11) DEFAULT NULL,
  `last_update` timestamp NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  PRIMARY KEY (`id`),
  KEY `user_email` (`user_email`),
  CONSTRAINT `test_results_ibfk_1` FOREIGN KEY (`user_email`) REFERENCES `users` (`email`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- 取消選取資料匯出。

-- 傾印  資料表 114_system.test_type 結構
CREATE TABLE IF NOT EXISTS `test_type` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `type` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- 取消選取資料匯出。

-- 傾印  資料表 114_system.users 結構
CREATE TABLE IF NOT EXISTS `users` (
  `email` varchar(255) NOT NULL,
  `password` varchar(255) NOT NULL,
  `nickname` varchar(255) DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT current_timestamp(),
  `point` int(11) DEFAULT 0,
  PRIMARY KEY (`email`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- 取消選取資料匯出。

-- 傾印  資料表 114_system.user_answers 結構
CREATE TABLE IF NOT EXISTS `user_answers` (
  `id` char(36) NOT NULL,
  `user_email` varchar(255) DEFAULT NULL,
  `question_id` char(36) DEFAULT NULL,
  `test_id` char(36) DEFAULT NULL,
  `question_type_id` int(11) DEFAULT NULL,
  `user_answer` varchar(255) DEFAULT NULL,
  `is_correct` tinyint(1) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `user_email` (`user_email`),
  KEY `test_id` (`test_id`),
  CONSTRAINT `user_answers_ibfk_1` FOREIGN KEY (`user_email`) REFERENCES `users` (`email`) ON DELETE CASCADE,
  CONSTRAINT `user_answers_ibfk_2` FOREIGN KEY (`test_id`) REFERENCES `test_results` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- 取消選取資料匯出。

-- 傾印  資料表 114_system.vocab_tests 結構
CREATE TABLE IF NOT EXISTS `vocab_tests` (
  `id` char(36) NOT NULL,
  `word` varchar(255) DEFAULT NULL,
  `definition` text DEFAULT NULL,
  `option_a` varchar(255) DEFAULT NULL,
  `option_b` varchar(255) DEFAULT NULL,
  `option_c` varchar(255) DEFAULT NULL,
  `option_d` varchar(255) DEFAULT NULL,
  `correct_option` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- 取消選取資料匯出。

/*!40103 SET TIME_ZONE=IFNULL(@OLD_TIME_ZONE, 'system') */;
/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IFNULL(@OLD_FOREIGN_KEY_CHECKS, 1) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40111 SET SQL_NOTES=IFNULL(@OLD_SQL_NOTES, 1) */;
