-- phpMyAdmin SQL Dump
-- version 4.4.14
-- http://www.phpmyadmin.net
--
-- Host: 127.0.0.1
-- Generation Time: Jan 12, 2016 at 07:13 PM
-- Server version: 5.6.26
-- PHP Version: 5.6.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `tinder`
--

-- --------------------------------------------------------

--
-- Table structure for table `accounts`
--

CREATE TABLE IF NOT EXISTS `accounts` (
  `id` int(32) NOT NULL,
  `username` varchar(30) CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL,
  `password` varchar(30) CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL,
  `administrator` tinyint(1) NOT NULL DEFAULT '0',
  `timestamp` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=latin1;

--
-- Dumping data for table `accounts`
--

INSERT INTO `accounts` (`id`, `username`, `password`, `administrator`, `timestamp`) VALUES
(1, 'FlipskiZ', 'notreal', 1, '2015-10-02 16:20:49'),
(2, 'meh', 'mobil99', 1, '2015-10-02 16:20:49'),
(3, 'NewUser', 'yesplease', 0, '2015-10-02 16:20:49'),
(4, 'Sigurd1998', '12345', 1, '2015-10-02 16:20:49'),
(8, 'Oskar', 'oskoskosk', 1, '2015-10-05 13:28:49'),
(9, 'Heldiggris1', 'youtubemoney', 1, '2015-11-17 19:14:05'),
(10, 'slawek', 'slawek', 1, '2015-12-30 15:24:05'),
(11, 'Joachim', 'Filipkanlesedette', 0, '2016-01-06 20:44:14');

-- --------------------------------------------------------

--
-- Table structure for table `likes`
--

CREATE TABLE IF NOT EXISTS `likes` (
  `id` int(32) NOT NULL,
  `likerId` int(32) NOT NULL,
  `liked` tinyint(1) NOT NULL,
  `receiverId` int(32) NOT NULL,
  `timestamp` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB AUTO_INCREMENT=193 DEFAULT CHARSET=latin1;

--
-- Dumping data for table `likes`
--

INSERT INTO `likes` (`id`, `likerId`, `liked`, `receiverId`, `timestamp`) VALUES
(160, 8, 0, 7, '2015-10-05 14:02:22'),
(161, 8, 1, 8, '2015-10-05 14:02:23'),
(162, 8, 0, 2, '2015-10-05 14:02:24'),
(165, 8, 1, 3, '2015-10-05 14:02:28'),
(166, 8, 1, 6, '2015-10-05 14:02:30'),
(167, 8, 0, 9, '2015-10-05 14:02:31'),
(168, 8, 0, 11, '2015-10-05 14:02:35'),
(169, 8, 0, 4, '2015-10-05 14:02:36'),
(170, 8, 1, 5, '2015-10-05 14:02:37'),
(171, 8, 1, 1, '2015-10-05 14:02:39'),
(172, 9, 1, 8, '2015-11-17 19:14:44'),
(173, 9, 1, 11, '2015-11-17 19:14:51'),
(174, 9, 1, 2, '2015-11-17 19:14:53'),
(175, 9, 1, 3, '2015-11-17 19:14:56'),
(176, 9, 1, 9, '2015-11-17 19:14:58'),
(177, 9, 1, 4, '2015-11-17 19:15:02'),
(178, 9, 1, 5, '2015-11-17 19:15:06'),
(179, 9, 1, 1, '2015-11-17 19:15:08'),
(180, 9, 1, 6, '2015-11-17 19:15:11'),
(181, 9, 1, 7, '2015-11-17 19:15:13'),
(184, 9, 1, 12, '2015-11-17 19:25:55'),
(185, 10, 1, 12, '2015-12-30 15:24:52'),
(186, 10, 1, 2, '2015-12-30 15:24:54'),
(187, 10, 1, 3, '2015-12-30 15:24:56'),
(188, 10, 1, 9, '2015-12-30 15:24:57'),
(189, 10, 1, 5, '2015-12-30 15:25:09'),
(190, 10, 1, 6, '2015-12-30 15:25:15'),
(191, 10, 1, 4, '2015-12-30 15:25:18'),
(192, 10, 1, 7, '2015-12-30 15:38:41');

-- --------------------------------------------------------

--
-- Table structure for table `pictures`
--

CREATE TABLE IF NOT EXISTS `pictures` (
  `id` int(32) NOT NULL,
  `name` varchar(30) CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL,
  `imagePath` text NOT NULL,
  `timestamp` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=latin1;

--
-- Dumping data for table `pictures`
--

INSERT INTO `pictures` (`id`, `name`, `imagePath`, `timestamp`) VALUES
(1, 'SpaceX', '/images/1.jpg', '2015-10-02 16:07:37'),
(2, 'Mirror''s Edge', '/images/2.jpg', '2015-10-02 16:07:37'),
(3, 'Nuka Cola', '/images/3.jpg', '2015-10-02 16:07:37'),
(4, 'Green Steam Logo', '/images/4.jpg', '2015-10-02 16:07:37'),
(5, 'Rainbow Steam', '/images/5.jpg', '2015-10-02 16:07:37'),
(6, 'Provoking Bear', '/images/6.jpg', '2015-10-02 16:07:37'),
(7, 'New Vegas', '/images/7.jpg', '2015-10-02 16:07:37'),
(8, 'Fire/Water', '/images/8.jpg', '2015-10-02 16:07:37'),
(9, 'The Witcher 3', '/images/9.jpg', '2015-10-02 22:06:24'),
(11, 'L-L-Legend... wait for it.... ', '/images/11.jpg', '2015-10-03 22:17:43'),
(12, 'Galaxy', '/images/12.jpg', '2015-11-17 19:22:25'),
(13, 'Pixel Rag', '/images/13.jpg', '2016-01-06 20:32:07');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `accounts`
--
ALTER TABLE `accounts`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `username` (`username`);

--
-- Indexes for table `likes`
--
ALTER TABLE `likes`
  ADD PRIMARY KEY (`id`),
  ADD KEY `liker` (`likerId`),
  ADD KEY `receiver` (`receiverId`);

--
-- Indexes for table `pictures`
--
ALTER TABLE `pictures`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `name` (`name`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `accounts`
--
ALTER TABLE `accounts`
  MODIFY `id` int(32) NOT NULL AUTO_INCREMENT,AUTO_INCREMENT=12;
--
-- AUTO_INCREMENT for table `likes`
--
ALTER TABLE `likes`
  MODIFY `id` int(32) NOT NULL AUTO_INCREMENT,AUTO_INCREMENT=193;
--
-- AUTO_INCREMENT for table `pictures`
--
ALTER TABLE `pictures`
  MODIFY `id` int(32) NOT NULL AUTO_INCREMENT,AUTO_INCREMENT=14;
--
-- Constraints for dumped tables
--

--
-- Constraints for table `likes`
--
ALTER TABLE `likes`
  ADD CONSTRAINT `likes_ibfk_1` FOREIGN KEY (`likerId`) REFERENCES `accounts` (`id`),
  ADD CONSTRAINT `likes_ibfk_2` FOREIGN KEY (`receiverId`) REFERENCES `pictures` (`id`);

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
